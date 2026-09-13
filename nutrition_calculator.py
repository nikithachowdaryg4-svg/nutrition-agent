def calculate_bmi(weight, height):
    """
    Calculate BMI.
    Weight is in kg.
    Height is in cm.
    """

    height_m = height / 100

    bmi = weight / (height_m * height_m)

    return round(bmi, 2)


def bmi_category(bmi):
    """Return BMI category."""

    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def calculate_bmr(age, weight, height, gender):
    """
    Calculate BMR using Mifflin-St Jeor equation.
    """

    if gender.lower() == "male":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

    return round(bmr, 2)


def calculate_daily_calories(bmr, activity_level):
    """Estimate daily calorie requirement."""

    activity_factors = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725
    }

    factor = activity_factors.get(activity_level.lower(), 1.2)

    calories = bmr * factor

    return round(calories, 2)


def calculate_macros(calories):
    """
    Basic educational macro estimate.
    """

    protein_calories = calories * 0.25
    carbohydrate_calories = calories * 0.45
    fat_calories = calories * 0.30

    protein = protein_calories / 4
    carbohydrates = carbohydrate_calories / 4
    fat = fat_calories / 9

    return {
        "protein": round(protein, 2),
        "carbohydrates": round(carbohydrates, 2),
        "fat": round(fat, 2)
    }