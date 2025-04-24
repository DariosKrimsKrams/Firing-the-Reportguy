# pip install pdfkit
# brew install wkhtmltopdf
import pdfkit
import os
def html_to_pdf(input_html_path: str, output_pdf_path: str):
    if not os.path.exists(input_html_path):
        raise FileNotFoundError(f"HTML file not found: {input_html_path}")
    try:
        pdfkit.from_file(input_html_path, output_pdf_path)
        print(f"PDF successfully created at: {output_pdf_path}")
    except Exception as e:
        print(f"Error during PDF generation: {e}")
# Example usage:
html_to_pdf("./report/report-template.html", "./output.pdf")
