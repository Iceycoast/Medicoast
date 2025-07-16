from typing import Optional
from app.config import OPENAI_API_KEY, AI_MODEL
from openai import OpenAI
from app.aggregator.models import DailySummary  

client = OpenAI(api_key=OPENAI_API_KEY)


def format_section(summary: DailySummary) -> str:
    """
    Format the cleaned summary fields into readable sections.
    This is all the AI will see.
    """
    parts = []

    if summary.water_ml is not None:
        parts.append(f"Water intake: {summary.water_ml} ml")

    if summary.calories is not None:
        parts.append(f"Calories consumed: {summary.calories} kcal")

    if summary.sleep_hours is not None:
        parts.append(f"Sleep duration: {summary.sleep_hours:.1f} hours")

    if summary.latest_bmi is not None:
        parts.append(f"BMI: {summary.latest_bmi:.1f}")

    if summary.mood:
        parts.append(f"Mood entries: {', '.join(summary.mood)}")

    if summary.medications:
        parts.append(f"Medications taken: {', '.join(summary.medications)}")

    return "\n".join(parts)


def generate_daily_summary(summary: DailySummary) -> Optional[str]:
    """
    Generate a short, friendly AI summary using cleaned `DailySummary` data.
    """
    try:
        formatted_data = format_section(summary)

        if not formatted_data:
            return None

        prompt = f"""
Here is the user's daily health summary for {summary.date}:

{formatted_data}

Write a short (2-4 sentence) friendly summary in a warm tone, highlighting their hydration, meals, sleep, mood, BMI, and medications.
"""

        response = client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful health assistant who summarizes daily wellness logs."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=120,
            temperature=0.7,
        )

        content = response.choices[0].message.content
        return content.strip() if content else None

    except Exception:
        return None
