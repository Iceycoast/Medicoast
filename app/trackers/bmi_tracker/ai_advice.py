from fastapi import HTTPException
from app.db.database import get_connection
import sqlite3
from openai import OpenAI
from app.config import OPENAI_API_KEY


client = OpenAI(api_key= OPENAI_API_KEY)

def generate_bmi_advice(bmi: float, category: str, weight: float, height : float) -> str:
    prompt = (
        f"My BMI is {bmi}, which falls under the '{category}' category. "
        f"My weight is {weight} kg and height is {height} cm.\n"
        "Give me a short, clear health advice in 3 sentences — tell me if I'm healthy, "
        "and what I should do to improve or maintain my health. Be respectful but realistic."
    )

    try:
        response = client.chat.completions.create(
            model= 'gpt-4o',
            messages=[
                {'role': 'system', 'content': 'you are fitness and health advisor'},
                {'role': 'user', 'content': prompt}
            ],
            max_tokens= 150,
            temperature= 0.7
        )
        message = response.choices[0].message
        content = getattr(message, "content", None)

        if content is None:
            raise HTTPException(status_code=500, detail= "AI response did not contain a valid content.")
        return content.strip()

    except Exception as e:
        raise HTTPException(status_code=500, detail= f"AI generation failed:{e}")
    

def get_ai_advice_for_bmi_log(log_id :int, user_id: int) ->str:
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT bmi, category , weight_kg, height_cm FROM bmi_logs WHERE log_id= ? AND user_id = ?",
                       (log_id, user_id))
        row = cursor.fetchone()

        if row is None:
            raise HTTPException(status_code=404, detail="BMI Log not found for this user.")
        
        return generate_bmi_advice(
                bmi = row['bmi'],
                category= row['category'],
                weight= row['weight_kg'],
                height= row['height_cm']
        )
    finally:
        conn.close()