import json
import os
import hashlib
from agents import BaseAgent
from typing import List, Dict
from datetime import datetime, timedelta

TREND_STORE_PATH = "storage/trend_store/trends.json"
SEEN_REVIEWS_PATH = "storage/review_store/seen_reviews.json"
WINDOW_DAYS = 30


class TopicCounterAgent(BaseAgent):
    def __init__(self):
        os.makedirs("storage/trend_store", exist_ok=True)
        os.makedirs("storage/review_store", exist_ok=True)

        if not os.path.exists(TREND_STORE_PATH):
            with open(TREND_STORE_PATH, "w") as f:
                json.dump({}, f)

        if not os.path.exists(SEEN_REVIEWS_PATH):
            with open(SEEN_REVIEWS_PATH, "w") as f:
                json.dump([], f)

    def run(self, reviews: List[Dict], topics: Dict, date: str):
        trend_store = self._safe_load(TREND_STORE_PATH)
        seen_reviews = set(self._safe_load(SEEN_REVIEWS_PATH))

        for topic in topics:
            trend_store.setdefault(topic, {})
            trend_store[topic][date] = 0

        new_seen = set()

        for review in reviews:
            review_hash = self._hash_review(review)

            # DEDUPLICATION
            if review_hash in seen_reviews:
                continue

            matched_topic = self._match_review_to_topic(
                review["text"], topics
            )

            if matched_topic:
                trend_store[matched_topic][date] += 1

            new_seen.add(review_hash)

        # Update seen reviews
        seen_reviews.update(new_seen)

        self._apply_sliding_window(trend_store, date)

        self._safe_write(TREND_STORE_PATH, trend_store)
        self._safe_write(SEEN_REVIEWS_PATH, list(seen_reviews))

    # ---------- helpers ----------

    def _hash_review(self, review: Dict) -> str:
        text = review.get("text", "")
        rating = str(review.get("rating", ""))
        raw = (text + rating).encode("utf-8")
        return hashlib.md5(raw).hexdigest()

    def _match_review_to_topic(self, text: str, topics: Dict) -> str | None:
        text_lower = text.lower()

        for topic in topics:
            if any(word in text_lower for word in topic.lower().split()):
                return topic

        return None

    def _apply_sliding_window(self, trend_store: Dict, date: str):
        current = datetime.strptime(date, "%Y-%m-%d").date()
        cutoff = current - timedelta(days=WINDOW_DAYS)

        for topic in trend_store:
            for d in list(trend_store[topic].keys()):
                if datetime.strptime(d, "%Y-%m-%d").date() < cutoff:
                    del trend_store[topic][d]

    def _safe_load(self, path: str):
        try:
            with open(path, "r") as f:
                content = f.read().strip()
                return json.loads(content) if content else {}
        except:
            return {}

    def _safe_write(self, path: str, data):
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
