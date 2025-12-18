# app_generator.py (separate file from your Week 2 predictor)
from flask import Flask, request, jsonify
from generator import SimpleTweetGenerator
from genenerator_ai import AITweetGenerator
from advanced_generator import AdvancedTweetGenerator
import joblib
import numpy as np
from textblob import TextBlob
from datetime import datetime

app = Flask(__name__)
generator = SimpleTweetGenerator()
generator_ai = AITweetGenerator()
advanced_generator = AdvancedTweetGenerator()

# Load the like predictor model
try:
    like_predictor = joblib.load("like_predictor.pkl")
except:
    like_predictor = None


def extract_features_from_tweet(tweet_text, has_media=False, hour=None):
    """
    Extract features from a generated tweet so we can feed them
    into the Week 2 like prediction model.
    """
    if hour is None:
        hour = datetime.now().hour

    word_count = len(tweet_text.split())
    char_count = len(tweet_text)
    sentiment = TextBlob(tweet_text).sentiment.polarity

    return {
        'word_count': word_count,
        'char_count': char_count,
        'has_media': 1 if has_media else 0,
        'hour': hour,
        'sentiment': round(sentiment, 2)
    }


@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        company = data.get('company', 'Our Company')
        tweet_type = data.get('tweet_type', 'general')
        message = data.get('message', 'Something awesome!')
        topic = data.get('topic', 'innovation')
        
        generated_tweet = generator.generate_tweet(company, tweet_type, message, topic)
        
        return jsonify({
            'generated_tweet': generated_tweet,
            'success': True,
            'company': company,
            'type': tweet_type
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500


@app.route('/generate_and_predict', methods=['POST'])
def generate_and_predict():
    """Generate a tweet AND predict how many likes it will get."""
    try:
        if like_predictor is None:
            return jsonify({
                'error': 'Like prediction model is not loaded.',
                'success': False
            }), 500

        data = request.get_json() or {}

        company = data.get('company', 'Our Company')
        tweet_type = data.get('tweet_type', 'general')
        message = data.get('message', 'Something awesome!')
        topic = data.get('topic', 'innovation')
        has_media = data.get('has_media', False)
        hour = data.get('hour')  # optional override

        # 1. Generate tweet using the simple template-based generator
        generated_tweet = generator.generate_tweet(
            company=company,
            tweet_type=tweet_type,
            message=message,
            topic=topic
        )

        # 2. Extract features from the generated tweet
        features = extract_features_from_tweet(
            generated_tweet,
            has_media=has_media,
            hour=hour
        )

        # 3. Predict likes using the same feature ordering used elsewhere
        #    in this file (has_media, char_count, word_count, hour, sentiment)
        feature_vector = [[
            features['has_media'],
            features['char_count'],
            features['word_count'],
            features['hour'],
            features['sentiment']
        ]]

        predicted_likes = like_predictor.predict(feature_vector)[0]

        return jsonify({
            'generated_tweet': generated_tweet,
            'predicted_likes': int(predicted_likes),
            'predicted_features': features,
            'success': True
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/generate_ai', methods=['POST'])
def generate_ai():
    try:
        data = request.get_json()
        
        # 1. Extract inputs
        company = data.get('company', 'Our Company')
        topic = data.get('topic', 'tech')
        message = data.get('message', 'something new')
        
        # 2. Create a prompt for GPT-2
        # This gives the AI context on what to write about
        prompt = f"A professional social media post from {company}: {message} about {topic}."
        
        # 3. Call the AI generator
        ai_tweet = generator_ai.generate_ai_tweet(prompt)
        
        return jsonify({
            'generated_tweet': ai_tweet,
            'success': True,
            'method': 'AI (GPT-2)',
            'company': company
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500


@app.route('/generate_branded', methods=['POST'])
def generate_branded():
    try:
        data = request.get_json()
        company = data.get('company', 'Our Company')
        industry = data.get('industry', 'tech')
        brand_voice = data.get('brand_voice', 'casual')
        message = data.get('message', 'something new')
        topic = data.get('topic', '')
        
        branded_tweet = advanced_generator.generate_branded_tweet(
            company, industry, brand_voice, message, topic
        )
        
        return jsonify({
            'generated_tweet': branded_tweet,
            'success': True,
            'method': 'Branded',
            'brand_voice': brand_voice,
            'industry': industry
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/generate_smart', methods=['POST'])
def generate_smart():
    try:
        data = request.get_json()
        company = data.get('company', 'Our Company')
        message = data.get('message', 'something amazing')
        topic = data.get('topic', 'innovation')
        word_count = data.get('word_count_target', 15)
        sentiment = data.get('sentiment_target', 0.5)
        has_media = data.get('has_media', False)
        hour = data.get('optimal_hour', 14)
        
        result = advanced_generator.generate_smart_tweet(
            company, message, topic, word_count, sentiment, has_media, hour
        )
        
        # Predict likes if model is available
        if like_predictor:
            features = result['predicted_features']
            prediction = like_predictor.predict([[
                features['has_media'],
                features['char_count'],
                features['word_count'],
                features['hour'],
                features['sentiment']
            ]])[0]
            result['predicted_likes'] = int(prediction)
        
        result['success'] = True
        result['method'] = 'Smart (ML-Optimized)'
        
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/optimize_tweet', methods=['POST'])
def optimize_tweet():
    try:
        data = request.get_json()
        company = data.get('company', 'Our Company')
        message = data.get('message', 'something amazing')
        topic = data.get('topic', 'innovation')
        
        result = advanced_generator.optimize_for_likes(company, message, topic)
        
        # Predict likes for the optimized tweet
        if like_predictor:
            features = result['predicted_features']
            prediction = like_predictor.predict([[
                features['has_media'],
                features['char_count'],
                features['word_count'],
                features['hour'],
                features['sentiment']
            ]])[0]
            result['predicted_likes'] = int(prediction)
        
        result['success'] = True
        result['method'] = 'Auto-Optimized for Maximum Likes'
        
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'Tweet Generator API is running!',
        'model_loaded': like_predictor is not None
    })



if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Different port from your Week 2 API
