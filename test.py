import requests

# Test prediction API (from Week 2)
prediction_response = requests.post('http://localhost:5000/predict', json={
    'word_count': 15,
    'char_count': 120,
    'has_media': True,
    'hour': 14,
    'sentiment': 0.8
})

# Test generation API (from Week 3)  
generation_response = requests.post('http://localhost:5001/generate', json={
    'company': 'Nike',
    'tweet_type': 'announcement',
    'message': 'launching new product',
    'topic': 'sports'
})

print("Predicted Likes:", prediction_response.json())
print("Generated Tweet:", generation_response.json())