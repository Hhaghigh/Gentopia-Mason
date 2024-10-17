from pydantic import BaseModel
import requests
from PyPDF2 import PdfReader
from io import BytesIO
from gentopia.tools.basetool import BaseTool

class PDFReaderArgs(BaseTool):
    url: str  # URL to the PDF

class PDFReaderTool(BaseTool):
    """Tool that reads a PDF from a URL and returns its content."""

    name = "pdf_reader"
    description = "Reads a PDF from a given URL and returns its content."
    args_schema = PDFReaderArgs

    def _run(self, url: str) -> str:
        """Reads the PDF from the URL and extracts the text."""
        try:
            response = requests.get(url)
            if response.status_code != 200:
                return f"Failed to fetch the PDF: {response.status_code}"

            # Load the PDF file from the response content
            pdf_file = BytesIO(response.content)
            reader = PdfReader(pdf_file)

            # Extract text from all the pages
            pdf_text = ""
            for page_num in range(len(reader.pages)):
                pdf_text += reader.pages[page_num].extract_text()

            return pdf_text if pdf_text else "No text found in the PDF."

        except Exception as e:
            return f"An error occurred while reading the PDF: {str(e)}"
