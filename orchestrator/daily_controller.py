from agents.review_ingestor import ReviewIngestorAgent
from agents.cleaner_memory import CleanerMemoryAgent
from agents.topic_discovery import TopicDiscoveryAgent
from agents.topic_deduplicator import TopicDeduplicatorAgent
from agents.topic_counter import TopicCounterAgent
from agents.report_generator import ReportGeneratorAgent


class DailyController:
    def __init__(self):
        self.ingestor = ReviewIngestorAgent()
        self.cleaner = CleanerMemoryAgent()
        self.discovery = TopicDiscoveryAgent()
        self.deduplicator = TopicDeduplicatorAgent()
        self.counter = TopicCounterAgent()
        self.reporter = ReportGeneratorAgent()

    def run_for_date(self, app_link: str, date: str, day_index: int):
        print("[Controller] Starting pipeline")

        raw_reviews = self.ingestor.run(
            app_id=app_link,
            date=date,
            day_index=day_index
        )
        print("[Controller] Raw reviews:", raw_reviews)

        cleaned_reviews = self.cleaner.run(
            reviews=raw_reviews,
            date=date
        )
        
        print("[Controller] Cleaned reviews:", cleaned_reviews)

        candidate_topics = self.discovery.run(
            reviews=cleaned_reviews
        )
        print("[Controller] Candidate topics:", candidate_topics)

        canonical_topics = self.deduplicator.run(
            candidate_topics=candidate_topics
        )
        print("[Controller] Canonical topics:", canonical_topics)

        self.counter.run(
            reviews=cleaned_reviews,
            topics=canonical_topics,
            date=date
        )

        self.reporter.run(target_date=date)
        print("[Controller] Pipeline finished")
