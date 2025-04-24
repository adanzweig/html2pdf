from flask import Flask, request, send_file
from xhtml2pdf import pisa
import io
import os

app = Flask(__name__)

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    html = request.data.decode('utf-8')
    result = io.BytesIO()

    pisa_status = pisa.CreatePDF(io.StringIO(html), dest=result)
    result.seek(0)

    if pisa_status.err:
        return {'error': 'Error generating PDF'}, 500

    return send_file(result, mimetype='application/pdf', as_attachment=True, download_name='documento.pdf')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

