from rag.knowledge_base import NutritionKnowledgeBase


class NutritionAgent:

    def __init__(self):
        self.knowledge_base = NutritionKnowledgeBase()

    def find_food(self, query):
        results = self.knowledge_base.search_food(query, top_k=5)

        return results

    def get_food_details(self, food_name):
        food = self.knowledge_base.get_food_info(food_name)

        if food is None:
            return "Food not found."

        return {
            "Food": food["Food"],
            "Serving": food["Serving"],
            "Calories": food["Calories"],
            "Protein": food["Protein"],
            "Carbohydrates": food["Carbohydrates"],
            "Fat": food["Fat"],
            "Fiber": food["Fiber"],
            "Sugar": food["Sugar"]
        }