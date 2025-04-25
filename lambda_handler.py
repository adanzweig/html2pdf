import json
import base64
import subprocess
import tempfile

def lambda_handler(event, context=None):
    html = event.get("body", "")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as html_file:
        html_file.write(html.encode("utf-8"))
        html_path = html_file.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:
        pdf_path = pdf_file.name

    try:
        subprocess.run(
            ["wkhtmltopdf", html_path, pdf_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    except subprocess.CalledProcessError as e:
        print("Error:", e.stderr.decode())
        return {"statusCode": 500, "body": json.dumps({"error": e.stderr.decode()})}

    with open(pdf_path, "rb") as f:
        pdf_base64 = base64.b64encode(f.read()).decode("utf-8")

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/pdf",
            "Content-Disposition": "attachment; filename=document.pdf"
        },
        "isBase64Encoded": True,
        "body": pdf_base64
    }

# Local test
if __name__ == "__main__":
    html_input = """
    <html>
      <head><style>body { font-family: Arial; }</style></head>
      <body><h1>Hello PDF</h1><p>This is a test.</p></body>
    </html>
    """
    response = lambda_handler({"body": html_input})
    print("Status:", response["statusCode"])

    if response["statusCode"] == 200:
        with open("test_output.pdf", "wb") as f:
            f.write(base64.b64decode(response["body"]))
        print("✅ PDF written to test_output.pdf")
    else:
        print(response["body"])
