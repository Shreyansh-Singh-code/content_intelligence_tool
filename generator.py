
import random

class SimpleTweetGenerator:
    def __init__(self):
        
        self.templates = {
            'announcement': [
                "🚀 Exciting news from {company}! {message}",
                "Big announcement: {company} is {message} 🎉",
                "Hey everyone! {company} has {message} ✨"
            ],
            'question': [
                "What do you think about {topic}? Let us know! 💬",
                "Quick question: How do you feel about {topic}? 🤔",
                "{company} wants to know: What's your take on {topic}? 🗣️"
            ],
            'general': [
                "Check out what {company} is up to! {message} 🌟",
                "{company} update: {message} 💯",
                "From the {company} team: {message} 🔥"
            ]
        }
        
        # Sentiment-based templates for smart generation
        self.positive_templates = [
            "🎉 {company} is thrilled to share: {message} about {topic}! This is amazing!",
            "Incredible news! {company} {message} 🚀 {topic} #Excited",
            "We're so proud! {company} {message} ✨ {topic}",
            "Amazing progress on {topic}! {company} {message} 🌟",
            "Celebrating a milestone! {company} {message} 🎊 {topic}"
        ]
        
        self.negative_templates = [
            "{company} addresses concerns about {topic}: {message}",
            "Important update from {company} regarding {topic}. {message}",
            "{company} is working on {topic}. {message}",
            "Transparency matters. {company} {message} about {topic}."
        ]
        
        self.neutral_templates = [
            "{company} update: {message} regarding {topic}",
            "Latest from {company}: {message} on {topic}",
            "{company} shares insights on {topic}. {message}",
            "Industry update: {company} {message} about {topic}",
            "{company} announces {message} for {topic}"
        ]
    
    def generate_tweet(self, company, tweet_type="general", message="Something awesome!", topic="innovation"):
        
        template_list = self.templates.get(tweet_type, self.templates['general'])
        template = random.choice(template_list)
        
        
        tweet = template.format(
            company=company,
            message=message,
            topic=topic
        )
        
    
        if len(tweet) > 280:
            tweet = tweet[:277] + "..."
        
        return tweet