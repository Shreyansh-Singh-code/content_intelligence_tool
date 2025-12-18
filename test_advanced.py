import requests
import json

print("=" * 60)
print("TESTING ADVANCED TWEET GENERATION API")
print("=" * 60)

# Test 1: Branded Tweet Generation
print("\n1. Testing Branded Tweet Generation (Tech + Professional)")
print("-" * 60)
branded_response = requests.post('http://localhost:5001/generate_branded', json={
    'company': 'Microsoft',
    'industry': 'tech',
    'brand_voice': 'professional',
    'message': 'launching new AI features',
    'topic': 'Artificial Intelligence'
})
print(json.dumps(branded_response.json(), indent=2))

# Test 2: Branded Tweet - Food + Playful
print("\n2. Testing Branded Tweet (Food + Playful)")
print("-" * 60)
branded_food = requests.post('http://localhost:5001/generate_branded', json={
    'company': 'Starbucks',
    'industry': 'food',
    'brand_voice': 'playful',
    'message': 'new seasonal drink',
    'topic': 'Pumpkin Spice'
})
print(json.dumps(branded_food.json(), indent=2))

# Test 3: Smart Tweet Generation
print("\n3. Testing Smart Tweet Generation (ML-Optimized)")
print("-" * 60)
smart_response = requests.post('http://localhost:5001/generate_smart', json={
    'company': 'Tesla',
    'message': 'breakthrough in battery technology',
    'topic': 'electric vehicles',
    'word_count_target': 18,
    'sentiment_target': 0.7,
    'has_media': True,
    'optimal_hour': 14
})
result = smart_response.json()
print(json.dumps(result, indent=2))
if 'predicted_likes' in result:
    print(f"\n💡 Predicted Likes: {result['predicted_likes']}")

# Test 4: Smart Tweet - Negative Sentiment
print("\n4. Testing Smart Tweet (Negative Sentiment)")
print("-" * 60)
smart_negative = requests.post('http://localhost:5001/generate_smart', json={
    'company': 'TechCorp',
    'message': 'addressing security concerns',
    'topic': 'data privacy',
    'word_count_target': 15,
    'sentiment_target': -0.3,
    'has_media': False,
    'optimal_hour': 10
})
print(json.dumps(smart_negative.json(), indent=2))

# Test 5: Optimized Tweet (Auto-Optimized for Maximum Likes)
print("\n5. Testing Auto-Optimized Tweet")
print("-" * 60)
optimized_response = requests.post('http://localhost:5001/optimize_tweet', json={
    'company': 'SpaceX',
    'message': 'successful rocket landing',
    'topic': 'space exploration'
})
result = optimized_response.json()
print(json.dumps(result, indent=2))
if 'predicted_likes' in result:
    print(f"\n🎯 Optimized Predicted Likes: {result['predicted_likes']}")

# Test 6: Compare Multiple Approaches
print("\n6. Comparison: Template vs Smart vs Optimized")
print("-" * 60)

# Template-based
template_resp = requests.post('http://localhost:5001/generate', json={
    'company': 'Apple',
    'tweet_type': 'announcement',
    'message': 'new iPhone features',
    'topic': 'technology'
})

# Smart generation
smart_resp = requests.post('http://localhost:5001/generate_smart', json={
    'company': 'Apple',
    'message': 'new iPhone features',
    'topic': 'technology',
    'has_media': True,
    'sentiment_target': 0.8
})

# Optimized
optimized_resp = requests.post('http://localhost:5001/optimize_tweet', json={
    'company': 'Apple',
    'message': 'new iPhone features',
    'topic': 'technology'
})

print("\nTemplate-based:")
print(f"  Tweet: {template_resp.json().get('generated_tweet')}")

print("\nSmart (ML-Optimized):")
smart_result = smart_resp.json()
print(f"  Tweet: {smart_result.get('tweet')}")
if 'predicted_likes' in smart_result:
    print(f"  Predicted Likes: {smart_result['predicted_likes']}")

print("\nAuto-Optimized:")
opt_result = optimized_resp.json()
print(f"  Tweet: {opt_result.get('tweet')}")
if 'predicted_likes' in opt_result:
    print(f"  Predicted Likes: {opt_result['predicted_likes']}")

print("\n" + "=" * 60)
print("TESTING COMPLETE")
print("=" * 60)
