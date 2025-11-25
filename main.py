"""Main module for PDF summarization and Confluence upload."""

import argparse
import sys
from pathlib import Path

from src.config import Config
from src.confluence_client import ConfluenceClient, format_summary_as_html
from src.gemini_client import configure_gemini, summarize_text
from src.pdf_reader import extract_text_from_pdf


def process_pdf(
    pdf_path: str,
    page_title: str | None = None,
    parent_page_id: str | None = None,
) -> dict:
    """Process a PDF file: extract text, summarize, and upload to Confluence.

    Args:
        pdf_path: Path to the PDF file.
        page_title: Optional title for the Confluence page.
        parent_page_id: Optional parent page ID for hierarchy.

    Returns:
        dict: The created/updated Confluence page information.
    """
    # Load configuration
    config = Config.from_env()

    # Extract text from PDF
    pdf_path = Path(pdf_path)
    print(f"Extracting text from PDF: {pdf_path}")
    text_content = extract_text_from_pdf(pdf_path)

    if not text_content.strip():
        raise ValueError("No text content could be extracted from the PDF")

    print(f"Extracted {len(text_content)} characters from PDF")

    # Configure and use Gemini to summarize
    print("Summarizing content with Gemini AI...")
    configure_gemini(config.gemini_api_key)
    summary = summarize_text(text_content)
    print("Summary generated successfully")

    # Format summary as HTML for Confluence
    html_content = format_summary_as_html(summary, pdf_path.name)

    # Create page title if not provided
    if not page_title:
        page_title = f"PDF要約: {pdf_path.stem}"

    # Upload to Confluence
    print(f"Uploading to Confluence: {page_title}")
    confluence = ConfluenceClient(
        url=config.confluence_url,
        username=config.confluence_username,
        api_token=config.confluence_api_token,
        space_key=config.confluence_space_key,
    )

    # Check if page exists and update or create
    existing_page = confluence.get_page_by_title(page_title)
    if existing_page:
        print("Page exists, updating...")
        result = confluence.update_page(
            page_id=existing_page["id"],
            title=page_title,
            body=html_content,
        )
    else:
        print("Creating new page...")
        result = confluence.create_page(
            title=page_title,
            body=html_content,
            parent_id=parent_page_id,
        )

    # Build page URL from result links
    links = result.get("_links", {})
    page_url = f"{links.get('base', '')}{links.get('webui', '')}"
    print(f"Page uploaded successfully: {page_url}")
    return result


def main() -> int:
    """Main entry point for the CLI.

    Returns:
        int: Exit code (0 for success, 1 for failure).
    """
    parser = argparse.ArgumentParser(
        description="Summarize PDF content and upload to Confluence",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py document.pdf
  python main.py document.pdf --title "My Summary"
  python main.py document.pdf --parent-id 12345678
        """,
    )
    parser.add_argument(
        "pdf_path",
        help="Path to the PDF file to process",
    )
    parser.add_argument(
        "--title",
        "-t",
        help="Title for the Confluence page (default: PDF要約: <filename>)",
    )
    parser.add_argument(
        "--parent-id",
        "-p",
        help="Parent page ID for hierarchy in Confluence",
    )

    args = parser.parse_args()

    try:
        result = process_pdf(
            pdf_path=args.pdf_path,
            page_title=args.title,
            parent_page_id=args.parent_id,
        )
        print(f"\nSuccess! Page ID: {result.get('id')}")
        return 0
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
