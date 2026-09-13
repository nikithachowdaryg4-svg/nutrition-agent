import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class NutritionRetriever:

    def __init__(self, data_path="nutrition_data.csv"):
        self.data = pd.read_csv(data_path)

        # Create searchable text from each food record
        self.data["search_text"] = (
            self.data["Food"].astype(str)
            + " "
            + self.data["Category"].astype(str)
            + " "
            + self.data["Serving"].astype(str)
        )

        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2)
        )

        self.vectors = self.vectorizer.fit_transform(
            self.data["search_text"]
        )

    def search(self, query, top_k=5, min_similarity=0.20):
        """
        Search the nutrition database.

        Important:
        Low-confidence matches are rejected instead of returning
        an unrelated food just because it is the closest row.
        """

        if query is None:
            return self.data.iloc[0:0].drop(
                columns=["search_text"], errors="ignore"
            )

        query = str(query).strip()

        if not query:
            return self.data.iloc[0:0].drop(
                columns=["search_text"], errors="ignore"
            )

        query_vector = self.vectorizer.transform([query])

        # If none of the query words exist in the vocabulary,
        # there is definitely no reliable match.
        if query_vector.nnz == 0:
            return self.data.iloc[0:0].drop(
                columns=["search_text"], errors="ignore"
            )

        similarity_scores = cosine_similarity(
            query_vector,
            self.vectors
        ).flatten()

        # Sort by similarity, but reject weak matches.
        top_indices = similarity_scores.argsort()[::-1]

        valid_indices = [
            index
            for index in top_indices
            if similarity_scores[index] >= min_similarity
        ][:top_k]

        if not valid_indices:
            return self.data.iloc[0:0].drop(
                columns=["search_text"], errors="ignore"
            )

        results = self.data.iloc[valid_indices].copy()
        results["similarity"] = similarity_scores[valid_indices]

        return results.drop(
            columns=["search_text"],
            errors="ignore"
        )
