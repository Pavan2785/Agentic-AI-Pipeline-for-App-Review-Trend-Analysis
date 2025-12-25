from agents import BaseAgent
from typing import List, Dict
import re


class CleanerMemoryAgent(BaseAgent):
    def run(self, reviews: List[Dict], date: str) -> List[Dict]:
        """
        Input:
            reviews = [
                {"text": "...", "rating": 1},
                ...
            ]

        Output:
            cleaned_reviews = [
                {"text": "cleaned text", "rating": 1},
                ...
            ]
        """

        cleaned_reviews = []

        for review in reviews:
            text = review.get("text", "")
            rating = review.get("rating", None)

            cleaned_text = self._clean_text(text)

            if cleaned_text:
                cleaned_reviews.append({
                    "text": cleaned_text,
                    "rating": rating
                })

        return cleaned_reviews

    def _clean_text(self, text: str) -> str:
        """
        Basic normalization:
        - lowercase
        - remove extra spaces
        - remove special characters
        """

        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()
