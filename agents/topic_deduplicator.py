import json
import os
from agents import BaseAgent
from typing import List, Dict


TOPIC_STORE_PATH = "storage/topic_store/topics.json"


class TopicDeduplicatorAgent(BaseAgent):
    def __init__(self):
        seed_path = "storage/topic_store/seed_topics.json"
        if os.path.exists(seed_path):
            with open(seed_path, "r") as f:
                seed_topics = json.load(f)

            topic_store = self._load_topic_store()

            for topic in seed_topics:
                if topic not in topic_store:
                    topic_store[topic] = {
                        "aliases": [],
                        "created_on": self._today(),
                        "last_updated": self._today()
                    }

            self._save_topic_store(topic_store)


    def run(self, candidate_topics: List[Dict]) -> Dict:
        """
        Input:
            candidate_topics = [
                {
                    "topic": "delivery guy shouted",
                    "evidence": [...]
                }
            ]

        Output:
            canonical_topics = {
                "Delivery partner rude": {
                    "aliases": [...],
                    "created_on": "...",
                    "last_updated": "..."
                }
            }
        """

        topic_store = self._load_topic_store()

        for candidate in candidate_topics:
            candidate_topic = candidate["topic"]

            matched_topic = self._find_match(candidate_topic, topic_store)

            if matched_topic:
                # Merge into existing topic
                self._merge_alias(
                    topic_store,
                    matched_topic,
                    candidate_topic
                )
            else:
                # Create new canonical topic
                self._create_new_topic(topic_store, candidate_topic)

        self._save_topic_store(topic_store)
        return topic_store

    def _load_topic_store(self) -> Dict:
        try:
            with open(TOPIC_STORE_PATH, "r") as f:
                content = f.read().strip()
                if not content:
                    return {}
                return json.loads(content)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}


    def _save_topic_store(self, topic_store: Dict):
        with open(TOPIC_STORE_PATH, "w") as f:
            json.dump(topic_store, f, indent=2)

    def _find_match(self, candidate_topic: str, topic_store: Dict) -> str:
        """
        Decide if candidate_topic matches any existing canonical topic.
        Returns canonical topic name or None.
        """

        for canonical_topic, data in topic_store.items():
            if self._is_semantically_same(candidate_topic, canonical_topic, data["aliases"]):
                return canonical_topic

        return None

    def _is_semantically_same(
        self,
        candidate: str,
        canonical: str,
        aliases: List[str]
    ) -> bool:
        """
        Placeholder semantic matcher.
        Replace with LLM reasoning later.
        """

        # Very simple normalization for now
        candidate_norm = candidate.lower()
        canonical_norm = canonical.lower()

        if candidate_norm == canonical_norm:
            return True

        for alias in aliases:
            if candidate_norm == alias.lower():
                return True
        return False

    def _merge_alias(
        self,
        topic_store: Dict,
        canonical_topic: str,
        new_alias: str
    ):
        aliases = topic_store[canonical_topic]["aliases"]

        if new_alias not in aliases:
            aliases.append(new_alias)

        topic_store[canonical_topic]["last_updated"] = self._today()

    def _create_new_topic(self, topic_store: Dict, topic: str):
        topic_store[topic] = {
            "aliases": [],
            "created_on": self._today(),
            "last_updated": self._today()
        }

    def _today(self) -> str:
        from datetime import date
        return date.today().isoformat()
