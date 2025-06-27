from typing import List
import redis.asyncio as redis
from app.models.schemas import ReputationInput, ReputationOutput
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import re

# Ensure VADER lexicon is downloaded (run `nltk.download('vader_lexicon')` once)
# This block will attempt to download it if not found, but it's best to pre-download
# via 'python -c "import nltk; nltk.download(\"vader_lexicon\")"' in your Dockerfile or setup.
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except nltk.downloader.DownloadError:
    print("Downloading NLTK 'vader_lexicon' for sentiment analysis...")
    nltk.download('vader_lexicon', quiet=True) # Use quiet=True to suppress stdout
    print("Download complete.")


class ReputationScannerService:
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client
        self.analyzer = SentimentIntensityAnalyzer()

    async def scan_reputation(self, input_data: ReputationInput) -> ReputationOutput:
        """
        Analyzes the sentiment of provided text (e.g., initial pitch) and
        generates insights. Simulates scanning for public perception.
        """
        all_text = input_data.initial_pitch_text
        if input_data.founder_twitter_handle:
            all_text += f" Founder is @{input_data.founder_twitter_handle}."
        if input_data.founder_linkedin_url:
            all_text += f" Founder LinkedIn: {input_data.founder_linkedin_url}."

        # Perform sentiment analysis using VADER
        vs = self.analyzer.polarity_scores(all_text)
        overall_sentiment_score = vs['compound'] # Compound score is normalized between -1 (most negative) and +1 (most positive)

        positive_themes: List[str] = []
        negative_themes: List[str] = []
        neutral_themes: List[str] = []
        actionable_insights: List[str] = []

        # Simple keyword spotting for themes based on sentiment
        if overall_sentiment_score > 0.2: # Threshold for positive
            positive_keywords = ["innovative", "scalable", "breakthrough", "efficient", "growth", "disruptive", "strong", "promising", "unique"]
            for keyword in positive_keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', all_text, re.IGNORECASE):
                    positive_themes.append(keyword)
            if not positive_themes: positive_themes.append("general positive tone")
            actionable_insights.append("Capitalize on strong positive sentiment. Highlight these strengths in your messaging.")
        elif overall_sentiment_score < -0.2: # Threshold for negative
            negative_keywords = ["challenge", "risk", "expensive", "complex", "unproven", "slow", "weak", "uncertain", "doubt"]
            for keyword in negative_keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', all_text, re.IGNORECASE):
                    negative_themes.append(keyword)
            if not negative_themes: negative_themes.append("general negative tone")
            actionable_insights.append("Address negative sentiment directly. Develop a communication strategy to mitigate concerns and build trust.")
        else:
            neutral_themes.append("neutral sentiment or mixed signals")
            actionable_insights.append("Focus on clearly articulating your value proposition to move sentiment from neutral to positive.")
            actionable_insights.append("Seek early feedback to identify areas of confusion or potential concerns.")


        return ReputationOutput(
            startup_name=input_data.startup_name,
            overall_sentiment_score=round(overall_sentiment_score, 2),
            positive_themes=positive_themes,
            negative_themes=negative_themes,
            neutral_themes=neutral_themes,
            actionable_insights=actionable_insights
        )