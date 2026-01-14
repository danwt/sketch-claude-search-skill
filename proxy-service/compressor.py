"""
Compression module using OpenRouter API to summarize large text responses.
"""

import os
from openai import AsyncOpenAI

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-lite-001")
COMPRESSION_PROMPT = os.getenv(
    "COMPRESSION_PROMPT",
    "Process the following content according to the user's instruction. Preserve key facts, names, numbers, and actionable information. Output only the result, no preamble."
)


def get_client() -> AsyncOpenAI:
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY environment variable not set")
    return AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )


async def compress(content: str, instruction: str = "summarize briefly") -> str:
    """
    Compress/transform content using a cheap LLM via OpenRouter.

    Args:
        content: The raw text to process
        instruction: Natural language instruction for how to process (e.g.,
                     "brief summary", "detailed with all facts", "just urls and titles")

    Returns:
        Processed text

    Raises:
        Exception if compression fails
    """
    client = get_client()

    response = await client.chat.completions.create(
        model=OPENROUTER_MODEL,
        messages=[
            {
                "role": "system",
                "content": COMPRESSION_PROMPT
            },
            {
                "role": "user",
                "content": f"Instruction: {instruction}\n\nContent:\n{content}"
            }
        ],
    )

    return response.choices[0].message.content
