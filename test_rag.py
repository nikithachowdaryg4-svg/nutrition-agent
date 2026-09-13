from rag.retriever import NutritionRetriever

retriever = NutritionRetriever()

query = "high protein foods"

results = retriever.search(query, top_k=5)

print("\nNutrition RAG Results")
print("--------------------")

for _, row in results.iterrows():
    print(
        f"{row['Food']} | "
        f"Calories: {row['Calories']} | "
        f"Protein: {row['Protein']}g | "
        f"Fiber: {row['Fiber']}g"
    )