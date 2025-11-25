"""PDF Reader module for extracting text from PDF files."""

from pathlib import Path

from pypdf import PdfReader


def extract_text_from_pdf(pdf_path: str | Path) -> str:
    """Extract text content from a PDF file.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        str: Extracted text content from all pages.

    Raises:
        FileNotFoundError: If the PDF file does not exist.
        ValueError: If the file is not a valid PDF.
    """
    pdf_path = Path(pdf_path)

    if not pdf_path.suffix.lower() == ".pdf":
        raise ValueError(f"File is not a PDF: {pdf_path}")

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    reader = PdfReader(pdf_path)
    text_content = []

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text_content.append(page_text)

    return "\n\n".join(text_content)
