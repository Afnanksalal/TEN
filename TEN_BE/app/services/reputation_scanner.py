import redis.asyncio as redis
from app.models.schemas import ReputationInput, ReputationOutput
import re
from typing import List, Dict, Any, Optional
from serpapi import GoogleSearch
from app.core.config import settings
import asyncio
import json
import hashlib
import google.generativeai as genai

class ReputationScannerService:
    def __init__(self, redis_client: redis.Redis, gemini_model: genai.GenerativeModel):
        self.redis_client = redis_client
        self.gemini_model = gemini_model
        self.serpapi_key = settings.SERPAPI_API_KEY
        print(f"DEBUG(SerpAPI): Key loaded status: {bool(self.serpapi_key)}")
        if self.serpapi_key:
            print(f"DEBUG(SerpAPI): Key prefix: {self.serpapi_key[:5]}...")


    async def _fetch_twitter_data(self, query: str) -> List[str]:
        if not self.serpapi_key:
            print("SerpAPI key not configured. Skipping Twitter data fetch.")
            return []

        print(f"DEBUG(SerpAPI): Attempting to fetch Twitter data for query: '{query}'")

        cache_key_serp = f"twitter_search:{hashlib.sha256(query.encode('utf-8')).hexdigest()}"
        cached_tweets_json = await self.redis_client.get(cache_key_serp)
        if cached_tweets_json:
            print(f"DEBUG(SerpAPI): Cache hit for Twitter search: '{query}'")
            return json.loads(cached_tweets_json)

        params = {
            "api_key": self.serpapi_key,
            "engine": "google",
            "q": f"{query} site:twitter.com OR site:x.com",
            "num": 20
        }
        tweets = []
        try:
            print(f"DEBUG(SerpAPI): Calling SerpAPI for query '{query}' with params: {params}")
            search = GoogleSearch(params)
            
            results = await asyncio.to_thread(search.get_dict)
            
            print(f"DEBUG(SerpAPI): Raw SerpAPI response for '{query}': {json.dumps(results, indent=2)[:1000]}{'...' if len(json.dumps(results)) > 1000 else ''}")

            if "error" in results:
                print(f"ERROR(SerpAPI): API returned an error for query '{query}': {results['error']}")
                return []

            if "latest_posts" in results:
                print(f"DEBUG(SerpAPI): Found 'latest_posts' key in response for '{query}'.")
                for post in results["latest_posts"]:
                    tweet_text = post.get("title", "").strip()
                    if tweet_text:
                        tweets.append(tweet_text)
            
            if "organic_results" in results:
                print(f"DEBUG(SerpAPI): Found 'organic_results' key in response for '{query}'.")
                for result_data in results["organic_results"]:
                    link = result_data.get("link", "")
                    snippet = result_data.get("snippet", "").strip()
                    if (link.startswith("https://twitter.com/") or link.startswith("https://x.com/")) and snippet:
                        if snippet not in tweets:
                            tweets.append(snippet)
            
            tweets = [t for t in tweets if t and t.lower() != "no information is available for this page."]

            if tweets:
                await self.redis_client.setex(cache_key_serp, 3600, json.dumps(tweets))
                print(f"DEBUG(SerpAPI): Cached {len(tweets)} tweets for '{query}'.")
            else:
                print(f"DEBUG(SerpAPI): No relevant tweets extracted for '{query}'. Not caching.")

        except Exception as e:
            print(f"ERROR(SerpAPI): Exception during SerpAPI call for query '{query}': {type(e).__name__}: {e}")
        return tweets


    async def scan_reputation(self, input_data: ReputationInput) -> ReputationOutput:
        input_hash = hashlib.sha256(input_data.json().encode('utf-8')).hexdigest()
        cache_key_reputation = f"reputation_analysis:{input_hash}"

        cached_reputation_json = await self.redis_client.get(cache_key_reputation)
        if cached_reputation_json:
            print(f"DEBUG(Reputation): Cache hit for reputation analysis: {cache_key_reputation}")
            return ReputationOutput.parse_raw(cached_reputation_json)

        all_text_sources: List[str] = [input_data.initial_pitch_text]

        if input_data.founder_twitter_handle:
            all_text_sources.append(f"Founder's Twitter handle: @{input_data.founder_twitter_handle}.")

        twitter_queries_to_fetch = []
        if input_data.founder_twitter_handle:
            twitter_queries_to_fetch.append(f"from:{input_data.founder_twitter_handle}")
            twitter_queries_to_fetch.append(f"@{input_data.founder_twitter_handle}")
        
        twitter_queries_to_fetch.append(f"{input_data.startup_name}")

        for query in twitter_queries_to_fetch:
            fetched_tweets = await self._fetch_twitter_data(query)
            all_text_sources.extend(fetched_tweets)
        
        combined_text = " ".join(all_text_sources).strip()

        if not combined_text:
            combined_text = "No substantial public data found for analysis. Analyzing only provided pitch text."

        prompt = f"""
        Analyze the overall sentiment and public reputation of the following text related to a startup and its public perception.
        Provide an overall sentiment score (from -1.0 for extremely negative to +1.0 for extremely positive, 0.0 for neutral).
        Identify key positive, negative, and neutral themes discussed.
        Suggest actionable insights for reputation management based on the sentiment.
        Finally, provide a concise (1-2 sentences) overall qualitative review of the startup's/person's reputation.

        Text to Analyze:
        ---
        {combined_text}
        ---

        Output in JSON format with the following structure:
        {{
            "overall_sentiment_score": <float -1.0 to 1.0>,
            "positive_themes": ["theme1", "theme2"],
            "negative_themes": ["theme1", "theme2"],
            "neutral_themes": ["theme1", "theme2"],
            "actionable_insights": ["insight1", "insight2"],
            "overall_reputation_review": "Concise review here."
        }}
        """
        
        sentiment_data = {}
        try:
            gemini_response = await asyncio.to_thread(self.gemini_model.generate_content, prompt)
            gemini_output_text = gemini_response.text.strip()
            if gemini_output_text.startswith("```json") and gemini_output_text.endswith("```"):
                gemini_output_text = gemini_output_text[len("```json"): -len("```")].strip()
            
            sentiment_data = json.loads(gemini_output_text)
            print(f"DEBUG(Gemini Sentiment): Raw Gemini Response: {sentiment_data}")

        except Exception as e:
            print(f"ERROR(Gemini Sentiment): Gemini sentiment analysis failed: {e}. Falling back to default/simplified output.")
            sentiment_data = {
                "overall_sentiment_score": 0.0,
                "positive_themes": ["AI service unavailable"],
                "negative_themes": [],
                "neutral_themes": [],
                "actionable_insights": [f"Gemini sentiment analysis failed: {e}. Check API key or service."],
                "overall_reputation_review": "Reputation review unavailable due to AI service error."
            }

        result = ReputationOutput(
            startup_name=input_data.startup_name,
            overall_sentiment_score=float(sentiment_data.get("overall_sentiment_score", 0.0)),
            positive_themes=sentiment_data.get("positive_themes", []),
            negative_themes=sentiment_data.get("negative_themes", []),
            neutral_themes=sentiment_data.get("neutral_themes", []),
            actionable_insights=sentiment_data.get("actionable_insights", []),
            overall_reputation_review=sentiment_data.get("overall_reputation_review", "Review not generated.")
        )
        await self.redis_client.setex(cache_key_reputation, 3600, result.json())
        print(f"DEBUG(Reputation): Cached final reputation analysis result: {cache_key_reputation}")

        return result
