from rag.retriever import NutritionRetriever


class NutritionKnowledgeBase:

    def __init__(self):
        self.retriever = NutritionRetriever()

    def search_food(self, query, top_k=5):
        return self.retriever.search(query, top_k)

    def get_food_info(self, food_name):
        results = self.retriever.search(food_name, top_k=1)

        if len(results) == 0:
            return None

        return results.iloc[0]