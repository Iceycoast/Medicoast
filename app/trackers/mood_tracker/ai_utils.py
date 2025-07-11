from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def get_ai_sentiment_and_suggestion(mood: str | None, note: str | None) -> tuple[str, str]:
    content = f"Mood: {mood or ''}\nNote: {note or ''}".strip()

    if not content:
        return "neutral", "Try entering a mood or note for better suggestions."

    sentiment_prompt = f"""
Analyze the emotional sentiment in the following user journal entry.
Respond with only one word (no explanation): positive, negative, neutral, angry, sad, happy, anxious, tired, stressed, or excited.

Entry:
{content}
""".strip()

    suggestion_prompt = f"""
Based on the following mood or journal entry, give a short, helpful 1-line suggestion to the user.

{content}
""".strip()

    try:
        sentiment = _ask_chatgpt(sentiment_prompt, temperature=0.3, max_tokens=10)
        suggestion = _ask_chatgpt(suggestion_prompt, temperature=0.7, max_tokens=100)
        return sentiment, suggestion

    except Exception as e:
        raise RuntimeError(f"AI error: {e}")


def _ask_chatgpt(prompt: str, temperature: float, max_tokens: int) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens
    )

    if not response.choices:
        raise RuntimeError("AI did not return any choices.")

    message = response.choices[0].message
    content = getattr(message, "content", "").strip()

    if not content:
        raise RuntimeError("AI response was empty.")

    return content
