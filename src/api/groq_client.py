# filepath: src/api/groq_client.py
"""
Groq API Client
Handles all LLM communication with robust error handling for free-tier rate limits.
Returns a validated list of flashcard dicts: [{"question": str, "answer": str}]
"""

import json
import re
import time
import streamlit as st

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False


# ── Card counts per depth level ────────────────────────────────────────────────
DEPTH_CARD_COUNT = {
    "Basic": 15,
    "Intermediate": 20,
    "Advanced": 25,
    "Deep Dive": 30,
}

# ── System prompt template ─────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are FlashLearn AI, an expert educational content creator.
Your task is to generate flashcards that are PERFECTLY tailored to the learner's profile.

STRICT OUTPUT RULES:
1. Respond with ONLY a valid JSON array. No markdown, no explanation, no preamble.
2. Each element must be an object with exactly two keys: "question" and "answer".
3. Answers must be 1-3 concise sentences, adapted to the learner's age and profession.
4. Arrange cards in logical pedagogical order (foundational to advanced).
5. The very first character of your response must be '[' and the last must be ']'.

ADAPTATION RULES:
- For young students (age 6-14): Use simple analogies, relatable examples, avoid jargon.
- For teenagers (age 15-18): Use slightly technical language, pop-culture references are fine.
- For adults (age 19-30): Balance theory and practical application.
- For professionals (age 31+): Be concise, focus on implications and real-world use.
- Always match the vocabulary to their profession/specialty when possible.
"""


def _build_user_prompt(
    name: str,
    age: int,
    profession: str,
    sub_profession: str,
    topic: str,
    depth_level: str,
) -> str:
    card_count = DEPTH_CARD_COUNT.get(depth_level, 15)
    return (
        f"Learner Profile:\n"
        f"  Name: {name}\n"
        f"  Age: {age} years old\n"
        f"  Profession: {profession} ({sub_profession})\n\n"
        f"Task: Generate exactly {card_count} flashcards about '{topic}'.\n"
        f"Depth Level: {depth_level}\n"
        f"Return ONLY the JSON array with {card_count} objects."
    )


def _parse_flashcards(raw_text: str) -> list[dict]:
    """
    Extract and validate the JSON array from the LLM response.
    Handles minor formatting issues gracefully.
    """
    text = raw_text.strip()

    # Try direct parse first
    try:
        data = json.loads(text)
        if isinstance(data, list):
            return _validate_cards(data)
    except json.JSONDecodeError:
        pass

    # Attempt to extract JSON array via regex
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group())
            if isinstance(data, list):
                return _validate_cards(data)
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Could not parse flashcard JSON from response:\n{text[:300]}")


def _validate_cards(raw_list: list) -> list[dict]:
    """Ensure every card has 'question' and 'answer' keys with non-empty strings."""
    validated = []
    for item in raw_list:
        if not isinstance(item, dict):
            continue
        q = str(item.get("question", "")).strip()
        a = str(item.get("answer", "")).strip()
        if q and a:
            validated.append({"question": q, "answer": a})
    if not validated:
        raise ValueError("No valid flashcards found in LLM response.")
    return validated


def generate_flashcards(
    api_key: str,
    name: str,
    age: int,
    profession: str,
    sub_profession: str,
    topic: str,
    depth_level: str,
    max_retries: int = 3,
) -> list[dict]:
    """
    Main public function. Calls Groq API and returns validated flashcards.
    Implements exponential back-off for free-tier rate limits.

    Returns:
        list of {"question": str, "answer": str}

    Raises:
        RuntimeError: with a user-friendly message on unrecoverable failure.
    """
    if not GROQ_AVAILABLE:
        raise RuntimeError(
            "The `groq` package is not installed. Run: pip install groq"
        )

    if not api_key or api_key.strip() == "":
        raise RuntimeError(
            "No Groq API key provided. Please enter your free API key in the sidebar."
        )

    client = Groq(api_key=api_key.strip())
    user_prompt = _build_user_prompt(
        name, age, profession, sub_profession, topic, depth_level
    )

    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            response = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.7,
                max_tokens=8192,
            )
            raw = response.choices[0].message.content
            return _parse_flashcards(raw)

        except Exception as e:
            last_error = e
            err_str = str(e).lower()

            # Rate limit → exponential back-off
            if "rate" in err_str or "429" in err_str or "limit" in err_str:
                wait = 2 ** attempt  # 2, 4, 8 seconds
                st.toast(
                    f"⏳ Free-tier rate limit hit. Retrying in {wait}s "
                    f"(attempt {attempt}/{max_retries})…",
                    icon="⏳",
                )
                time.sleep(wait)
                continue

            # Authentication error
            if "auth" in err_str or "401" in err_str or "api_key" in err_str:
                raise RuntimeError(
                    "❌ Invalid Groq API key. Please check your key and try again."
                ) from e

            # Unexpected error
            raise RuntimeError(f"❌ Groq API error: {e}") from e

    raise RuntimeError(
        f"❌ Failed after {max_retries} attempts due to rate limiting. "
        "Please wait a minute and try again (free tier limit)."
    ) from last_error
