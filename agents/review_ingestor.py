from agents import BaseAgent
from google_play_scraper import reviews, Sort


class ReviewIngestorAgent(BaseAgent):
    def run(self, app_id: str, date: str, day_index: int = 0):
        print(f"[Ingestor] Fetching REAL reviews for batch {date}")

        collected = []
        continuation_token = None

        pages_to_skip = day_index 

        for i in range(pages_to_skip + 1):
            result, continuation_token = reviews(
                app_id,
                lang="en",
                country="in",
                sort=Sort.NEWEST,
                count=100,
                continuation_token=continuation_token
            )

            if not continuation_token:
                break

        # Collect only this batch's page
        for r in result:
            collected.append({
                "text": r["content"],
                "rating": r["score"]
            })

        return collected
