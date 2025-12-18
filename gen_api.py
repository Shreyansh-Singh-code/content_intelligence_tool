# app_generator.py (separate file from your Week 2 predictor)
from flask import Flask, request, jsonify
from generator import SimpleTweetGenerator

app = Flask(__name__)
generator = SimpleTweetGenerator()

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        
        # Get inputs (similar to how you got features in Week 2)
        company = data.get('company', 'Our Company')
        tweet_type = data.get('tweet_type', 'general')
        message = data.get('message', 'Something awesome!')
        topic = data.get('topic', 'innovation')
        
        # Generate tweet (similar to how you predicted likes)
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

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'Tweet Generator API is running!'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Different port from your Week 2 API