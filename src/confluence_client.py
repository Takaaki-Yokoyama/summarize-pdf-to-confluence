"""Confluence API module for uploading content to Confluence pages."""

import re

from atlassian import Confluence


class ConfluenceClient:
    """Client for interacting with Confluence API."""

    def __init__(
        self, url: str, username: str, api_token: str, space_key: str
    ) -> None:
        """Initialize the Confluence client.

        Args:
            url: The Confluence instance URL.
            username: The Confluence username (email).
            api_token: The Confluence API token.
            space_key: The Confluence space key.
        """
        self.confluence = Confluence(
            url=url,
            username=username,
            password=api_token,
            cloud=True,
        )
        self.space_key = space_key

    def create_page(
        self, title: str, body: str, parent_id: str | None = None
    ) -> dict:
        """Create a new Confluence page with the given content.

        Args:
            title: The title of the page.
            body: The body content of the page (HTML or wiki markup).
            parent_id: Optional parent page ID for hierarchy.

        Returns:
            dict: The created page information.
        """
        return self.confluence.create_page(
            space=self.space_key,
            title=title,
            body=body,
            parent_id=parent_id,
            type="page",
            representation="storage",
        )

    def update_page(self, page_id: str, title: str, body: str) -> dict:
        """Update an existing Confluence page.

        Args:
            page_id: The ID of the page to update.
            title: The new title of the page.
            body: The new body content of the page.

        Returns:
            dict: The updated page information.
        """
        return self.confluence.update_page(
            page_id=page_id,
            title=title,
            body=body,
            type="page",
            representation="storage",
        )

    def page_exists(self, title: str) -> bool:
        """Check if a page with the given title exists.

        Args:
            title: The title of the page to check.

        Returns:
            bool: True if the page exists, False otherwise.
        """
        return self.confluence.page_exists(space=self.space_key, title=title)

    def get_page_by_title(self, title: str) -> dict | None:
        """Get a page by its title.

        Args:
            title: The title of the page.

        Returns:
            dict | None: The page information if found, None otherwise.
        """
        return self.confluence.get_page_by_title(
            space=self.space_key, title=title
        )


def format_summary_as_html(summary: str, pdf_filename: str) -> str:
    """Format the summary text as HTML for Confluence.

    Args:
        summary: The summary text from Gemini.
        pdf_filename: The name of the original PDF file.

    Returns:
        str: HTML formatted content for Confluence.
    """
    lines = summary.split("\n")
    html_parts = []
    list_items = []

    def flush_list() -> None:
        """Flush accumulated list items as a ul block."""
        if list_items:
            html_parts.append("<ul>")
            html_parts.extend(list_items)
            html_parts.append("</ul>")
            list_items.clear()

    for line in lines:
        stripped = line.strip()
        if not stripped:
            flush_list()
            continue

        # Check for list items
        list_match = re.match(r"^[-*•]\s+(.+)$", stripped)
        if list_match:
            list_items.append(f"<li>{list_match.group(1)}</li>")
            continue

        # Flush any pending list items before other content
        flush_list()

        # Handle headers (order matters: check longer prefixes first)
        if stripped.startswith("### "):
            html_parts.append(f"<h3>{stripped[4:]}</h3>")
        elif stripped.startswith("## "):
            html_parts.append(f"<h2>{stripped[3:]}</h2>")
        elif stripped.startswith("# "):
            html_parts.append(f"<h1>{stripped[2:]}</h1>")
        else:
            html_parts.append(f"<p>{stripped}</p>")

    # Flush any remaining list items
    flush_list()

    content = "\n".join(html_parts)

    return f"""<h1>PDF要約: {pdf_filename}</h1>
<ac:structured-macro ac:name="info">
  <ac:rich-text-body>
    <p>このページは、PDFファイル「{pdf_filename}」をGemini AIで要約した内容です。</p>
  </ac:rich-text-body>
</ac:structured-macro>
<h2>要約内容</h2>
{content}
"""
