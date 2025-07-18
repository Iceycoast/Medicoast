from app.summary.weekly_summary.controller import get_weekly_summary
from .graphs_generator import generate_weekly_graphs
from app.summary.weekly_summary.controller import get_weekly_summary
from fpdf import FPDF
from typing import Any
from io import BytesIO
import os 



class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "MediCoast - Weekly Health Report", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def generate_weekly_pdf(user_id: int, user_full_name: str, start_date: str) -> bytes:
    # Fetch data
    data = get_weekly_summary(user_id, start_date)
    summary_data = data["summary"]
    stats = data["weekly_stats"]
    start_str = data["start_date"]
    end_str = data["end_date"]

    # Generate graphs
    graph_paths = generate_weekly_graphs(summary_data)

    # Setup PDF
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Title and user info
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"User: {user_full_name}", ln=True)
    pdf.cell(0, 10, f"Week: {start_str} to {end_str}", ln=True)
    pdf.ln(5)

    # Summary Table
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Weekly Averages:", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.cell(50, 10, "Average BMI:", border=1)
    pdf.cell(50, 10, str(stats.get("average_bmi", 0)), border=1, ln=True)
    pdf.cell(50, 10, "Avg Water Intake (ml):", border=1)
    pdf.cell(50, 10, str(stats.get("average_water_ml", 0)), border=1, ln=True)
    pdf.cell(50, 10, "Avg Calories:", border=1)
    pdf.cell(50, 10, str(stats.get("average_calories", 0)), border=1, ln=True)
    pdf.cell(50, 10, "Avg Sleep Duration (hrs):", border=1)
    pdf.cell(50, 10, str(stats.get("average_sleep_duration", 0)), border=1, ln=True)
    pdf.ln(10)

    # Insert Graphs
    for path in graph_paths:
        if os.path.exists(path):
            pdf.image(path, w=180)
            pdf.ln(10)

    # Daily Logs Table
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Daily Logs", ln=True)
    pdf.set_font("Arial", size=9)

    # Table Headers
    headers = [
        "Date", "Water (ml)", "Meals", "Total Cal",
        "BMI", "Sleep (Time)", "Duration (hrs)",
        "Moods", "Medications"
    ]
    for header in headers:
        pdf.cell(23, 8, header, border=1)
    pdf.ln()

    # Table Rows
    for date in sorted({log["date"] for log in summary_data.get("water_logs", [])} |
                       {log["date"] for log in summary_data.get("meals_logs", [])} |
                       {log["date"] for log in summary_data.get("sleep_logs", [])} |
                       {log["date"] for log in summary_data.get("mood_logs", [])} |
                       {log["date"] for log in summary_data.get("medication_logs", [])} |
                       {log["date"] for log in summary_data.get("bmi_logs", [])}):
        
        water = sum(log["amount_ml"] for log in summary_data.get("water_logs", []) if log["date"] == date)
        meals = ", ".join(f"{log['meal_name']} ({log['calories']} cal)" for log in summary_data.get("meals_logs", []) if log["date"] == date)
        total_cal = sum(log["calories"] for log in summary_data.get("meals_logs", []) if log["date"] == date)
        bmi = ", ".join(str(log["bmi"]) for log in summary_data.get("bmi_logs", []) if log["date"] == date)
        sleep_time = next((f"{log['sleep_time']} – {log['wake_time']}" for log in summary_data.get("sleep_logs", []) if log["date"] == date), "")
        duration = next((str(log["duration"]) for log in summary_data.get("sleep_logs", []) if log["date"] == date), "")
        moods = ", ".join(log["mood"] for log in summary_data.get("mood_logs", []) if log["date"] == date)
        meds = ", ".join(f"{log['medication_name']} ({log['dosage']})" for log in summary_data.get("medication_logs", []) if log["date"] == date)

        row = [date, str(water), meals, str(total_cal), bmi, sleep_time, duration, moods, meds]
        for item in row:
            pdf.cell(23, 8, item[:18], border=1)  # truncate if too long
        pdf.ln()

    # Write to BytesIO instead of .encode
    output_stream = BytesIO()
    pdf_bytes = pdf.output(dest='S')
    if isinstance(pdf_bytes, str):
        pdf_bytes = pdf_bytes.encode('latin1')
    output_stream.write(pdf_bytes)
    output_stream.seek(0)
    return output_stream.getvalue()