from agents import BaseAgent
from typing import List, Dict, Optional
import json
import os

SEED_TOPIC_PATH = "storage/topic_store/seed_topics.json"


class TopicDiscoveryAgent(BaseAgent):
    def __init__(self):
        if not os.path.exists(SEED_TOPIC_PATH):
            raise FileNotFoundError("Seed topics file missing")

        with open(SEED_TOPIC_PATH, "r") as f:
            self.seed_topics = json.load(f)

        # Canonical keyword topics (no semantic duplication)
        self.keyword_topics = [
            
            ("App stability & performance issues",
             ["app", "application"],
             ["crash", "freeze", "hang", "lag", "slow", "bug", "glitch"]),

            ("Login / authentication issue",
             ["login", "signin", "otp", "verification"],
             ["fail", "error", "issue"]),

            ("Issue after app update",
             ["update"],
             ["issue", "problem", "broke", "worse"]),

            # Payments
            ("Payment failure",
             ["payment", "upi", "card", "netbanking"],
             ["fail", "error", "declined"]),

            ("Refund not received",
             ["refund", "money"],
             ["not received", "pending", "delay"]),

            ("Incorrect charges",
             ["charged", "deducted", "double", "extra charge", "hidden fee"],
             []),

            # Pricing
            ("High pricing concerns",
             ["price", "cost", "expensive", "costly"],
             []),

            # Customer Support (not delivery partner behavior)
            ("Customer support issue",
             ["support", "customer care", "helpdesk"],
             ["rude", "bad", "unhelpful", "no response", "ignored"]),

            # Account & Policy
            ("Account suspension issue",
             ["account", "profile"],
             ["blocked", "suspended"]),

            ("Unfair policy concern",
             ["policy", "rules", "terms"],
             ["unfair", "bad"]),

            # Feature Requests 
            ("Feature request",
             ["add", "feature", "should have", "wish", "bring back", "old version", "remove"],
             [])
        ]

    def run(self, reviews: List[Dict]) -> List[Dict]:
        """
        Discovers topics from reviews.
        Only returns seed or valid evolved topics.
        Unmatched reviews are ignored.
        """

        discovered: Dict[str, List[str]] = {}

        for review in reviews:
            text = review.get("text", "")
            if not text:
                continue

            topic = self._match_seed_topic(text) or self._match_keyword_topic(text)
            if not topic:
                continue

            discovered.setdefault(topic, []).append(text)

        return [
            {"topic": topic, "evidence": evidence}
            for topic, evidence in discovered.items()
        ]

    def _match_seed_topic(self, text: str) -> Optional[str]:
        """
        Canonical matching for seed topics
        """
        text_lower = text.lower()

        for topic in self.seed_topics:
            keywords = topic.lower().split()
            if any(k in text_lower for k in keywords):
                return topic

        return None

    def _match_keyword_topic(self, text: str) -> Optional[str]:
        """
        Keyword-based evolving topic detection
        (guaranteed non-overlapping with seed topics)
        """
        text_lower = text.lower()

        for topic, primary_keys, secondary_keys in self.keyword_topics:
            if any(p in text_lower for p in primary_keys):
                if not secondary_keys or any(s in text_lower for s in secondary_keys):
                    return topic

        return None
