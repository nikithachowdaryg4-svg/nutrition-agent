from rag.knowledge_base import NutritionKnowledgeBase


class FoodLogAgent:

    def __init__(self):
        self.knowledge_base = NutritionKnowledgeBase()

    def analyze_meal(self, meal_text):

        # Split foods entered by the user
        foods = [
            food.strip()
            for food in meal_text.split(",")
            if food.strip()
        ]

        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_fat = 0
        total_fiber = 0

        food_results = []
        unrecognized_foods = []

        for food in foods:

            results = self.knowledge_base.search_food(food)

            if len(results) == 0:
                unrecognized_foods.append(food)
                continue

            row = results.iloc[0]

            total_calories += float(row["Calories"])
            total_protein += float(row["Protein"])
            total_carbs += float(row["Carbohydrates"])
            total_fat += float(row["Fat"])
            total_fiber += float(row["Fiber"])

            food_results.append(str(row["Food"]))

        return {
            "Foods": food_results,
            "Unrecognized Foods": unrecognized_foods,
            "Calories": round(total_calories, 2),
            "Protein": round(total_protein, 2),
            "Carbohydrates": round(total_carbs, 2),
            "Fat": round(total_fat, 2),
            "Fiber": round(total_fiber, 2)
        }

    def analyze_voice_text(self, voice_text):
        """
        Voice transcription is passed through the same safe
        food-matching pipeline.
        """
        return self.analyze_meal(voice_text)
