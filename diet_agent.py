from nutrition_calculator import ( (
    calculate_bmi,
    bmi_category,
    calculate_bmr,
    calculate_daily_calories,
    calculate_macros
)


class DietRecommendationAgent:

    def generate_plan(
        self,
        age,
        gender,
        weight,
        height,
        activity_level,
        goal,
        diet_type,
        cultural_preference="Any"
    ):

        # ==================================================
        # BMI
        # ==================================================

        bmi = calculate_bmi(
            weight,
            height
        )

        category = bmi_category(
            bmi
        )


        # ==================================================
        # BMR
        # ==================================================

        bmr = calculate_bmr(
            age,
            weight,
            height,
            gender
        )


        # ==================================================
        # DAILY CALORIES
        # ==================================================

        calories = calculate_daily_calories(
            bmr,
            activity_level
        )


        # ==================================================
        # GOAL BASED CALORIE ADJUSTMENT
        # ==================================================

        if goal.lower() == "weight loss":

            target_calories = calories - 300

        elif goal.lower() == "weight gain":

            target_calories = calories + 300

        else:

            target_calories = calories


        # ==================================================
        # MACROS
        # ==================================================

        macros = calculate_macros(
            target_calories
        )


        # ==================================================
        # CULTURAL FOOD PREFERENCE
        # ==================================================

        culture = cultural_preference.lower()


        # ==================================================
        # INDIAN
        # ==================================================

        if "indian" in culture:

            if diet_type.lower() == "vegetarian":

                meals = {
                    "Breakfast":
                        "Idli with sambar and fruit",

                    "Lunch":
                        "Brown rice, dal, mixed vegetables and curd",

                    "Snack":
                        "Fruit with almonds",

                    "Dinner":
                        "Chapati, paneer and vegetable curry"
                }

            else:

                meals = {
                    "Breakfast":
                        "Eggs with oats and banana",

                    "Lunch":
                        "Rice, chicken curry and vegetables",

                    "Snack":
                        "Greek yogurt and fruit",

                    "Dinner":
                        "Chapati, fish curry and vegetables"
                }


        # ==================================================
        # MEDITERRANEAN
        # ==================================================

        elif "mediterranean" in culture:

            if diet_type.lower() == "vegetarian":

                meals = {
                    "Breakfast":
                        "Greek yogurt, oats, berries and nuts",

                    "Lunch":
                        "Quinoa, chickpeas, vegetables and olive oil",

                    "Snack":
                        "Apple with almonds",

                    "Dinner":
                        "Whole grain bread, hummus and roasted vegetables"
                }

            else:

                meals = {
                    "Breakfast":
                        "Eggs, whole grain toast and fruit",

                    "Lunch":
                        "Grilled chicken, quinoa and Mediterranean salad",

                    "Snack":
                        "Greek yogurt and berries",

                    "Dinner":
                        "Grilled fish, vegetables and whole grains"
                }


        # ==================================================
        # ASIAN
        # ==================================================

        elif "asian" in culture:

            if diet_type.lower() == "vegetarian":

                meals = {
                    "Breakfast":
                        "Rice porridge with vegetables and tofu",

                    "Lunch":
                        "Vegetable rice bowl with tofu",

                    "Snack":
                        "Edamame and fruit",

                    "Dinner":
                        "Tofu stir-fry with brown rice and vegetables"
                }

            else:

                meals = {
                    "Breakfast":
                        "Eggs, rice and fresh fruit",

                    "Lunch":
                        "Chicken rice bowl with vegetables",

                    "Snack":
                        "Edamame and fruit",

                    "Dinner":
                        "Fish stir-fry with brown rice and vegetables"
                }


        # ==================================================
        # WESTERN
        # ==================================================

        elif "western" in culture:

            if diet_type.lower() == "vegetarian":

                meals = {
                    "Breakfast":
                        "Oatmeal with berries and nuts",

                    "Lunch":
                        "Whole grain sandwich with vegetables and cheese",

                    "Snack":
                        "Apple with peanut butter",

                    "Dinner":
                        "Vegetable pasta with salad"
                }

            else:

                meals = {
                    "Breakfast":
                        "Eggs, whole grain toast and fruit",

                    "Lunch":
                        "Grilled chicken sandwich with salad",

                    "Snack":
                        "Greek yogurt and berries",

                    "Dinner":
                        "Grilled fish, potatoes and vegetables"
                }


        # ==================================================
        # DEFAULT
        # ==================================================

        else:

            if diet_type.lower() == "vegetarian":

                meals = {
                    "Breakfast":
                        "Oats with milk and banana",

                    "Lunch":
                        "Brown rice, dal, vegetables and curd",

                    "Snack":
                        "Fruit and almonds",

                    "Dinner":
                        "Chapati, paneer and vegetables"
                }

            else:

                meals = {
                    "Breakfast":
                        "Eggs with oats and fruit",

                    "Lunch":
                        "Rice, chicken and vegetables",

                    "Snack":
                        "Greek yogurt and fruit",

                    "Dinner":
                        "Chapati, fish and vegetables"
                }


        # ==================================================
        # FINAL RESULT
        # ==================================================

        return {
            "BMI": bmi,

            "BMI Category": category,

            "BMR": bmr,

            "Daily Calories": target_calories,

            "Protein": macros["protein"],

            "Carbohydrates": macros["carbohydrates"],

            "Fat": macros["fat"],

            "Meals": meals,

            "Cultural Preference": cultural_preference
        }
