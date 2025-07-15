def calculate_bmi(weight_kg: float, height_cm: float) -> tuple[float, str]:
    if height_cm <= 0 or weight_kg <= 0:
        raise ValueError("Height or Weight cannot be 0. Please enter valid data.")
    height_m = height_cm / 100
    bmi = round(weight_kg / (height_m ** 2), 2)
    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 25:
        category = "Normal"
    elif 25 <= bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"
    return bmi, category 