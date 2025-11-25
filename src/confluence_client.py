"""Confluence API module for uploading content to Confluence pages."""

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
    # Convert markdown-style content to basic HTML
    lines = summary.split("\n")
    html_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Handle bullet points
        if line.startswith("- ") or line.startswith("* "):
            html_lines.append(f"<li>{line[2:]}</li>")
        elif line.startswith("• "):
            html_lines.append(f"<li>{line[2:]}</li>")
        # Handle headers
        elif line.startswith("## "):
            html_lines.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("# "):
            html_lines.append(f"<h1>{line[2:]}</h1>")
        elif line.startswith("### "):
            html_lines.append(f"<h3>{line[4:]}</h3>")
        else:
            html_lines.append(f"<p>{line}</p>")

    # Wrap consecutive list items in ul tags
    content = "\n".join(html_lines)

    # Simple approach: wrap consecutive li elements in ul
    content = content.replace("</li>\n<li>", "</li><li>")
    content = content.replace("<li>", "<ul><li>", 1) if "<li>" in content else content

    # Close all ul tags properly
    li_count = content.count("<li>")
    ul_count = content.count("<ul>")
    if li_count > 0 and ul_count > 0:
        # Find groups of consecutive li elements and wrap them
        import re

        content = re.sub(
            r"(<li>.*?</li>)+",
            lambda m: f"<ul>{m.group(0)}</ul>",
            content,
            flags=re.DOTALL,
        )
        # Remove duplicate ul tags
        content = content.replace("<ul><ul>", "<ul>")
        content = content.replace("</ul></ul>", "</ul>")

    html_content = f"""
<h1>PDF要約: {pdf_filename}</h1>
<ac:structured-macro ac:name="info">
  <ac:rich-text-body>
    <p>このページは、PDFファイル「{pdf_filename}」をGemini AIで要約した内容です。</p>
  </ac:rich-text-body>
</ac:structured-macro>
<h2>要約内容</h2>
{content}
"""
    return html_content
