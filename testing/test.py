import requests
import json


def pretty_print(label, response):
    """Helper to pretty-print JSON with emojis instead of escape codes."""
    print(label)
    try:
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"  [Error decoding JSON: {e}]")
        print("  Raw text:", response.text)


print("=" * 60)
print("TESTING PREDICT / GENERATE / GENERATE_AND_PREDICT APIs")
print("=" * 60)

# Test prediction API (from Week 2)
prediction_response = requests.post('http://localhost:5000/predict', json={
    'word_count': 15,
    'char_count': 120,
    'has_media': True,
    'hour': 14,
    'sentiment': 0.8
})
pretty_print("\n1. Testing /predict (Week 2 model)", prediction_response)

# Test generation API (from Week 3)
generation_response = requests.post('http://localhost:5001/generate', json={
    'company': 'Nike',
    'tweet_type': 'announcement',
    'message': 'launching new product',
    'topic': 'sports'
})
pretty_print("\n2. Testing /generate (template-based tweet)", generation_response)

# Test AI-based generation API
ai_generation_response = requests.post('http://localhost:5001/generate_ai', json={
    'company': 'Tesla',
    'topic': 'electric vehicles',
    'message': 'revolutionary battery technology'
})
pretty_print("\n3. Testing /generate_ai (GPT-2 based)", ai_generation_response)

# Test new generate_and_predict API
gap_response = requests.post('http://localhost:5001/generate_and_predict', json={
    'company': 'Adidas',
    'tweet_type': 'announcement',
    'message': 'launching a new running shoe',
    'topic': 'marathons',
    'has_media': True
})
pretty_print("\n4. Testing /generate_and_predict (template + like prediction)", gap_response)

print("\n" + "=" * 60)
print("BASIC TESTING COMPLETE")
print("=" * 60)
