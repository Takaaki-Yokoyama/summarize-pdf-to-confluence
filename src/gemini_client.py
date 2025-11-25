"""Gemini API module for summarizing text content."""

import google.generativeai as genai


def configure_gemini(api_key: str) -> None:
    """Configure the Gemini API with the provided API key.

    Args:
        api_key: The Gemini API key.
    """
    genai.configure(api_key=api_key)


def summarize_text(text: str, model_name: str = "gemini-1.5-flash") -> str:
    """Summarize the provided text using Gemini AI.

    Args:
        text: The text content to summarize.
        model_name: The Gemini model to use for summarization.

    Returns:
        str: The summarized text.

    Raises:
        ValueError: If the text is empty.
    """
    if not text or not text.strip():
        raise ValueError("Cannot summarize empty text")

    model = genai.GenerativeModel(model_name)

    prompt = f"""以下のテキストを日本語で要約してください。
重要なポイントを箇条書きで整理し、わかりやすくまとめてください。

テキスト:
{text}
"""

    response = model.generate_content(prompt)
    return response.text
