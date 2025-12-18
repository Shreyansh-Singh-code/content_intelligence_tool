# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview
This is a machine learning project for content intelligence and tweet analytics. It includes:
- A like prediction model (RandomForestRegressor) trained on tweet data
- A Flask API for predicting likes on content
- A Flask API for generating tweets (both template-based and AI-powered)
- A simple HTML frontend for testing predictions

## Project Structure
- **api.py** - Like prediction API (port 5000)
- **gen_api.py** - Tweet generation API (port 5001) with multiple endpoints
- **generator.py** - SimpleTweetGenerator class for template-based tweet generation
- **genenerator_ai.py** - AITweetGenerator class using GPT-2 for AI-powered tweet generation
- **advanced_generator.py** - AdvancedTweetGenerator with ML-optimized smart generation
- **test.py** - Basic API testing script
- **test_advanced.py** - Comprehensive testing for advanced features
- **initialize.ipynb** - Jupyter notebook containing model training pipeline
- **data.csv** - Training dataset with tweet data (id, date, likes, content, username, media, inferred company)
- **like_predictor.pkl** - Trained RandomForest model (gitignored)
- **index.html** - Simple frontend UI for testing predictions

## Development Commands

### Environment Setup
```pwsh
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Install Dependencies
The project requires:
- Flask & flask-cors
- scikit-learn
- pandas
- numpy
- joblib
- textblob
- transformers (for GPT-2)
- torch
- seaborn & matplotlib (for notebooks)

### Run APIs
```pwsh
# Like Prediction API (port 5000)
python api.py

# Tweet Generation API (port 5001)
python gen_api.py
```

### Test APIs
```pwsh
# Basic tests
python test.py

# Advanced features (branded, smart, optimized)
python test_advanced.py
```

### View Frontend
Open `index.html` in a browser (requires api.py running on port 5000)

## Model Details

### Like Prediction Model
**Features used:**
- `word_count` - Number of words in content
- `char_count` - Character count
- `has_media` - Boolean (0/1) indicating media presence
- `hour` - Hour of posting (0-23)
- `sentiment` - Sentiment polarity score from TextBlob

**Model:** RandomForestRegressor
**Training:** See `initialize.ipynb` for full pipeline including data cleaning, feature engineering, and model training

### Tweet Generation
**Template-based:** Uses predefined templates with placeholders for company, message, topic, and tweet_type (announcement, question, general)

**AI-based:** Uses GPT-2 model from Hugging Face transformers with temperature=0.8, max_length=60, enforces 280 character limit

## API Endpoints

### Like Prediction API (api.py)
- **POST /predict** - Predicts likes for given features
  - Request body: `{word_count, char_count, has_media, hour, sentiment}`
  - Response: `{predicted_likes: int}`

### Tweet Generation API (gen_api.py)
- **POST /generate** - Template-based generation
  - Request body: `{company, tweet_type, message, topic}`
  - Response: `{generated_tweet, success, company, type}`

- **POST /generate_ai** - AI-powered generation (GPT-2)
  - Request body: `{company, topic, message}`
  - Response: `{generated_tweet, success, method, company}`

- **POST /generate_branded** - Brand voice + industry-specific generation
  - Request body: `{company, industry, brand_voice, message, topic}`
  - Industries: tech, food, fashion, fitness, finance
  - Brand voices: casual, professional, playful
  - Response: `{generated_tweet, success, method, brand_voice, industry}`

- **POST /generate_smart** - ML-optimized generation with like prediction
  - Request body: `{company, message, topic, word_count_target, sentiment_target, has_media, optimal_hour}`
  - Uses like predictor model features to optimize engagement
  - Response: `{tweet, predicted_features, optimization_tips, predicted_likes, success, method}`

- **POST /optimize_tweet** - Auto-optimized for maximum likes
  - Request body: `{company, message, topic}`
  - Generates multiple variations and returns the best one
  - Response: `{tweet, predicted_features, optimization_tips, predicted_likes, success, method}`

- **GET /health** - Health check
  - Response: `{status, model_loaded}`

## Advanced Features

### Smart Tweet Generation
The `AdvancedTweetGenerator` class uses ML model insights to optimize tweets for maximum engagement:

**Key optimization factors:**
- **Word count:** 15-20 words optimal for engagement
- **Sentiment:** Positive sentiment (0.5-0.8) correlates with higher likes
- **Media:** Including media increases likes by 30-50%
- **Timing:** Peak hours are 12-15 (lunch/afternoon)

**Three generation modes:**
1. **Branded** - Industry and brand voice specific templates
2. **Smart** - Manual control over ML features (word count, sentiment, media, hour)
3. **Optimized** - Automatic generation of multiple variations, returns best one

### Brand Voices
- **Casual:** Friendly tone with emojis, 2 hashtags
- **Professional:** Formal tone without emojis, 1 hashtag
- **Playful:** Fun tone with emojis, 3 hashtags

### Supported Industries
Tech, Food, Fashion, Fitness, Finance (each with custom templates)

## Known Issues
- No requirements.txt file present - dependencies must be manually installed
