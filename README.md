# Agentic-AI-Pipeline-for-App-Review-Trend-Analysis

PROJECT OVERVIEW

PulseGen.io is an agent-based analytics system that analyzes real user reviews from Google Play Store apps (Swiggy and Zomato).
The system automatically identifies user issues, tracks how these issues evolve over time, and generates a 30-day trend report that is displayed in a web browser.

The goal of this project is to simulate how real-world product analytics pipelines work, using modular agents instead of a monolithic script.

---

KEY FEATURES

• Uses real Google Play Store reviews
• Agent-based (modular) architecture
• Dynamic topic discovery (not hardcoded output)
• Deduplication of reviews to prevent double counting
• 30-day sliding window trend analysis
• Browser-based HTML dashboard output
• Clean, reproducible execution for demos

---

TECHNOLOGY STACK

• Python 3
• google-play-scraper
• HTML + CSS (for UI output)
• File-based storage (JSON)

No database, no OpenAI API, no external services required.

---

PROJECT STRUCTURE

main.py
Entry point of the application.
Handles user input, resets system state, runs the pipeline for 30 days, and opens the final report in a browser.

config.py
Stores configuration such as app IDs and window size.

orchestrator/daily_controller.py
Coordinates the execution of all agents for a single day.

agents/review_ingestor.py
Fetches real Google Play reviews in non-overlapping batches.

agents/cleaner.py
Normalizes and cleans review text.

agents/topic_discovery.py
Maps reviews to known issues and creates new issues when needed.

agents/topic_deduplicator.py
Ensures similar issues are merged into a single canonical topic.

agents/topic_counter.py
Counts occurrences of each issue per day and builds trends.

agents/report_generator.py
Generates HTML, CSV, and JSON reports.
This file controls the UI (dashboard).

storage/topic_store/seed_topics.json
Contains initial known issues.

storage/topic_store/topics.json
Stores all discovered canonical topics.

storage/trend_store/trends.json
Stores topic-wise daily counts.

storage/review_store/seen_reviews.json
Tracks already processed reviews to avoid duplicates.

output/trend_report.html
Final browser-based dashboard.

---

AGENTIC PIPELINE FLOW

User Input
↓
Review Ingestor Agent
↓
Cleaner Agent
↓
Topic Discovery Agent
↓
Topic Deduplicator Agent
↓
Topic Counter Agent
↓
Report Generator Agent
↓
Browser Dashboard

Each agent has one responsibility and does not overlap with others.

---

SEED TOPICS

The system starts with the following known issues:
• Delivery Issue
• Food quality issues
• Delivery partner rude
• Maps not working properly

If a review does not match these, the system creates a new topic automatically.

---

HOW TREND ANALYSIS WORKS

• Reviews are fetched in non-overlapping batches using pagination
• Each review is counted only once
• Each batch represents one day
• Trends are built over a 30-day window
• Topics with zero occurrences are excluded from the final report

---

WHY OUTPUT MAY CHANGE SLIGHTLY BETWEEN RUNS

The system uses live Google Play data.
Google Play does not guarantee deterministic ordering of reviews.

Even within a few seconds:
• Review order may shift
• Pagination boundaries may change

This causes small, expected variations in output.

---

SETUP INSTRUCTIONS

1. Download the File
2. Open it using Visual Studio Code
3. Create a virtual environment
4. Activate the environment
5. Install google-play-scraper
6. Run main.py

No API keys required.

---

HOW TO RUN

python main.py

You will be prompted to:
• Select an app (Swiggy or Zomato)
• Enter a start date (YYYY-MM-DD)

The system processes 30 days and opens the report in your browser.

---

OUTPUT FILES

trend_report.html – Browser dashboard
trend_report.csv – Spreadsheet format
trend_report.json – Programmatic format

---



Just tell me.
