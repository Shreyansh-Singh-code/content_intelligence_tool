import random
from textblob import TextBlob

class AdvancedTweetGenerator:
    def __init__(self):
        self.brand_voices = {
            'casual': {'emojis': True, 'tone': 'friendly', 'hashtags': 2},
            'professional': {'emojis': False, 'tone': 'formal', 'hashtags': 1},
            'playful': {'emojis': True, 'tone': 'fun', 'hashtags': 3},
        }
        
        self.industry_templates = {
            'tech': [
                "🚀 Innovation alert: {message}",
                "Tech news: {message}",
                "Breaking: {company} unveils {message}",
                "The future is here: {message}"
            ],
            'food': [
                "🍕 Delicious update: {message}",
                "Tasty news: {message}",
                "Craving something special? {message}",
                "Fresh from our kitchen: {message}"
            ],
            'fashion': [
                "✨ Style update: {message}",
                "Fashion alert: {message}",
                "Runway ready: {message}",
                "Trending now: {message}"
            ],
            'fitness': [
                "💪 Fitness goals: {message}",
                "Get moving: {message}",
                "Your wellness journey: {message}",
                "Strong together: {message}"
            ],
            'finance': [
                "📊 Market insights: {message}",
                "Financial update: {message}",
                "Smart money moves: {message}",
                "Your financial future: {message}"
            ]
        }
        
        # Sentiment-based templates for smart generation
        self.positive_templates = [
            "🎉 {company} is thrilled to share: {message}!",
            "Incredible news! {company} {message} 🚀",
            "We're so proud! {company} {message} ✨",
            "Amazing progress! {company} {message} 🌟",
            "Celebrating: {company} {message} 🎊"
        ]
        
        self.negative_templates = [
            "{company} addresses: {message}",
            "Important update from {company}: {message}",
            "{company} is working on: {message}",
            "Transparency matters. {company}: {message}"
        ]
        
        self.neutral_templates = [
            "{company} update: {message}",
            "Latest from {company}: {message}",
            "{company} shares: {message}",
            "Industry update: {company} {message}",
            "{company} announces: {message}"
        ]
        
        self.emojis = {
            'positive': ['🎉', '🚀', '✨', '🌟', '💪', '🔥', '👏', '🎊'],
            'neutral': ['📊', '📢', '💡', '🔔', '📣', '🎯'],
            'negative': ['⚠️', '📉', '🔧', '⏰'],
            'question': ['🤔', '💭', '❓', '🗣️']
        }
    
    def generate_branded_tweet(self, company, industry, brand_voice, message, topic=""):
        """
        Generate a tweet with specific brand voice and industry style.
        
        Args:
            company: Company name
            industry: Industry type (tech, food, fashion, fitness, finance)
            brand_voice: Voice type (casual, professional, playful)
            message: Main message
            topic: Optional topic
        
        Returns:
            Branded tweet string
        """
        # Get industry template
        industry = industry.lower()
        if industry in self.industry_templates:
            template = random.choice(self.industry_templates[industry])
        else:
            template = "{message}"
        
        # Format with company and message
        tweet = template.format(company=company, message=message)
        
        # Apply brand voice
        voice_config = self.brand_voices.get(brand_voice, self.brand_voices['casual'])
        
        # Remove emojis if professional
        if not voice_config['emojis']:
            tweet = ''.join(char for char in tweet if ord(char) < 0x1F300 or ord(char) > 0x1F9FF)
            tweet = tweet.strip()
        
        # Add hashtags based on voice
        if voice_config['hashtags'] > 0 and topic:
            hashtag = f"#{topic.replace(' ', '')}"
            if len(tweet + " " + hashtag) <= 280:
                tweet += " " + hashtag
        
        # Ensure length limit
        if len(tweet) > 280:
            tweet = tweet[:277] + "..."
        
        return tweet
    
    def generate_smart_tweet(self, company, message, topic, word_count_target=15, 
                           sentiment_target=0.5, has_media=False, optimal_hour=14):
        """
        Generate a tweet optimized for maximum engagement using ML model insights.
        
        Args:
            company: Company name
            message: Main message
            topic: Topic of the tweet
            word_count_target: Target word count (10-20 optimal)
            sentiment_target: Target sentiment (-1 to 1, positive performs better)
            has_media: Whether media is included (increases engagement)
            optimal_hour: Suggested posting hour (14 = 2 PM, high engagement)
        
        Returns:
            dict with 'tweet', 'predicted_features', 'tips'
        """
        # Select templates based on sentiment target
        if sentiment_target > 0.3:
            templates = self.positive_templates
            emoji_set = self.emojis['positive']
        elif sentiment_target < -0.3:
            templates = self.negative_templates
            emoji_set = self.emojis['negative']
        else:
            templates = self.neutral_templates
            emoji_set = self.emojis['neutral']
        
        # Generate initial tweet
        template = random.choice(templates)
        tweet = template.format(company=company, message=message)
        
        # Add topic if relevant
        if topic and len(tweet) < 240:
            tweet += f" regarding {topic}"
        
        # Adjust length to match word_count_target
        current_words = len(tweet.split())
        
        if current_words < word_count_target - 3:
            # Tweet is too short, add engaging elements
            additions = [
                "Join us!",
                "Learn more!",
                "Stay tuned.",
                "What do you think?",
                "Share your thoughts!",
                "Exciting times ahead!"
            ]
            if len(tweet) < 260:
                tweet += " " + random.choice(additions)
        elif current_words > word_count_target + 5:
            # Tweet is too long, trim it intelligently
            words = tweet.split()
            # Keep up to target, try to end at punctuation
            truncated = " ".join(words[:word_count_target])
            if not truncated[-1] in '.!?':
                truncated += "..."
            tweet = truncated
        
        # Add media indicators if has_media is True
        if has_media and len(tweet) < 270:
            media_hints = random.choice(['📸', '🎥', '👀'])
            tweet += " " + media_hints
        
        # Add strategic emoji if sentiment is positive and not already present
        if sentiment_target > 0.5 and len(tweet) < 278:
            if not any(emoji in tweet for emoji in self.emojis['positive']):
                tweet += " " + random.choice(emoji_set)
        
        # Calculate actual features
        actual_word_count = len(tweet.split())
        actual_char_count = len(tweet)
        actual_sentiment = TextBlob(tweet).sentiment.polarity
        
        # Generate tips for optimization
        tips = []
        if actual_word_count < 10:
            tips.append("Tweet is short. Consider adding more detail for engagement.")
        if actual_sentiment < 0.2 and sentiment_target > 0.5:
            tips.append("Sentiment is lower than target. Use more positive language.")
        if not has_media:
            tips.append("Adding media (image/video) typically increases likes by 30-50%.")
        if optimal_hour < 9 or optimal_hour > 17:
            tips.append(f"Consider posting at {optimal_hour}:00. Peak hours are 12-15 for engagement.")
        
        # Ensure tweet doesn't exceed Twitter limit
        if len(tweet) > 280:
            tweet = tweet[:277] + "..."
        
        return {
            'tweet': tweet,
            'predicted_features': {
                'word_count': actual_word_count,
                'char_count': actual_char_count,
                'has_media': 1 if has_media else 0,
                'hour': optimal_hour,
                'sentiment': round(actual_sentiment, 2)
            },
            'optimization_tips': tips
        }
    
    def optimize_for_likes(self, company, message, topic):
        """
        Generate multiple tweet variations and return the one optimized for maximum likes.
        
        Uses known patterns from ML model:
        - Word count: 15-20 words optimal
        - Positive sentiment (0.5-0.8) performs best
        - Media presence increases engagement
        - Posting hour: 12-15 (lunch/afternoon) is peak
        
        Returns:
            Best optimized tweet with prediction features
        """
        # Generate variations with different strategies
        variations = []
        
        # Variation 1: High sentiment, medium length
        var1 = self.generate_smart_tweet(
            company, message, topic,
            word_count_target=18,
            sentiment_target=0.7,
            has_media=True,
            optimal_hour=14
        )
        variations.append(var1)
        
        # Variation 2: Neutral sentiment, shorter
        var2 = self.generate_smart_tweet(
            company, message, topic,
            word_count_target=15,
            sentiment_target=0.3,
            has_media=True,
            optimal_hour=13
        )
        variations.append(var2)
        
        # Variation 3: Very positive, longer
        var3 = self.generate_smart_tweet(
            company, message, topic,
            word_count_target=20,
            sentiment_target=0.8,
            has_media=False,
            optimal_hour=12
        )
        variations.append(var3)
        
        # Score each variation based on known good features
        best_variation = max(variations, key=lambda v: self._score_tweet(v['predicted_features']))
        
        return best_variation
    
    def _score_tweet(self, features):
        """
        Score a tweet based on features that correlate with high engagement.
        Based on typical ML model insights.
        """
        score = 0
        
        # Optimal word count: 15-20
        if 15 <= features['word_count'] <= 20:
            score += 30
        elif 10 <= features['word_count'] <= 25:
            score += 15
        
        # Positive sentiment boost
        if features['sentiment'] > 0.5:
            score += 25
        elif features['sentiment'] > 0.2:
            score += 10
        
        # Media presence is strong signal
        if features['has_media']:
            score += 35
        
        # Peak hours (12-15)
        if 12 <= features['hour'] <= 15:
            score += 20
        elif 9 <= features['hour'] <= 17:
            score += 10
        
        return score
