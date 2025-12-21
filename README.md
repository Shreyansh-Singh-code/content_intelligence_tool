# 🚀 Tweet Intelligence Engine

A comprehensive machine learning-powered system for generating tweets and predicting their engagement (likes) using advanced AI techniques and Random Forest regression.

## 🌟 Features

- **Multiple Tweet Generation Methods**:
  - **Template-based Generator**: Simple, sentiment-enhanced template generation
  - **Advanced Generator**: Brand voice and industry-specific tweet generation
  - **Smart/Optimized Generator**: ML-optimized tweets based on engagement patterns
  - **AI Generator**: GPT-2 based neural tweet generation

- **Like Prediction**: Predict tweet engagement using a trained Random Forest model
- **Interactive Streamlit UI**: User-friendly interface for generating and predicting in one click
- **RESTful APIs**: Flask-based APIs for programmatic access
- **Feature Extraction**: Automatic extraction of word count, character count, sentiment, and metadata

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Flask
- **Machine Learning**: Scikit-learn (Random Forest Regressor)
- **NLP**: TextBlob, Transformers (GPT-2)
- **Data Processing**: Pandas, NumPy
- **Model Persistence**: Joblib

## 📁 Project Structure

```
base/
├── README.md
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
│
├── /model&data
│   ├── initialize.ipynb      # Model training notebook
│   ├── like_predictor.pkl    # Trained Random Forest model
│   └── data.csv              # Training dataset
│
├── /tweet_generators
│   ├── generator_ai.py       # GPT-2 based AI generator
│   ├── advanced_generator.py # Brand voice & smart generator
│   └── generator_simple.py   # Template-based generator 
│
├── /api
│   ├── like_predictor_api.py # Like prediction API 
│   └── generator_api.py      # Tweet generation API 
│
└── /testing
    ├── test.py               # Basic API tests
    └── test_advanced.py      # Advanced generator tests
```

## 📊 How It Works

### 1. Tweet Generation

The system offers four generation methods:

#### Template-based Generator (`generator_simple.py`)
- Uses predefined templates with sentiment logic
- Supports announcement, question, and general tweet types
- Automatically adjusts sentiment based on input

#### Advanced Generator (`advanced_generator.py`)
- **Brand Voice Generation**: Creates tweets with specific brand voices (casual, professional, playful)
- **Industry-specific**: Tailored templates for tech, food, fashion, fitness, finance
- **Smart Generation**: ML-optimized tweets based on:
  - Target word count (optimal: 15-20 words)
  - Target sentiment (positive performs better)
  - Media presence (increases engagement)
  - Optimal posting hour (12-15 PM peak)

#### AI Generator (`generator_ai.py`)
- Uses GPT-2 language model for creative tweet generation
- Generates context-aware tweets from prompts
- Requires transformers and torch libraries

### 2. Like Prediction

The prediction model (`like_predictor.pkl`) uses a Random Forest Regressor trained on:
- **Word Count**: Number of words in the tweet
- **Character Count**: Total characters
- **Has Media**: Binary indicator (0/1) for media presence
- **Hour**: Posting hour (0-23)
- **Sentiment**: Sentiment polarity score (-1 to 1) from TextBlob

### 3. Model Training

The model is trained in `initialize.ipynb`:
- Dataset: 17,331 tweets with engagement metrics
- Features extracted: word count, char count, sentiment, media presence, posting hour
- Algorithm: Random Forest Regressor
- Performance: RMSE ~3698 (varies based on data distribution)

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/tweet-intelligence-engine
   cd tweet-intelligence-engine
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK data** (required for TextBlob)
   ```python
   python -c "import nltk; nltk.download('punkt'); nltk.download('brown')"
   ```

### Running the Streamlit App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Using the APIs

#### Start the Like Predictor API
```bash
python api/like_predictor_api.py
```
Runs on `http://localhost:5000`

#### Start the Generator API
```bash
python api/generator_api.py
```
Runs on `http://localhost:5001`

## 📖 Usage Guide

### Streamlit UI

1. **Select Generator Type**: Choose from Template, Advanced (brand voice), Advanced (smart), or AI generator
2. **Enter Metadata**:
   - Company name
   - Topic/hashtag context
   - Message/update content
   - Additional parameters based on generator type
3. **Set Prediction Parameters**:
   - Has media (checkbox)
   - Posting hour (slider)
   - Optional feature overrides
4. **Generate & Predict**: Click the button to generate a tweet and get like predictions

### API Endpoints

#### Like Predictor API (`/predict`)
```python
POST http://localhost:5000/predict
Content-Type: application/json

{
    "word_count": 15,
    "char_count": 120,
    "has_media": 1,
    "hour": 14,
    "sentiment": 0.8
}
```

#### Generator API Endpoints

**Template Generation** (`/generate`)
```python
POST http://localhost:5001/generate
Content-Type: application/json

{
    "company": "Nike",
    "tweet_type": "announcement",
    "message": "launching new product",
    "topic": "sports"
}
```

**AI Generation** (`/generate_ai`)
```python
POST http://localhost:5001/generate_ai
Content-Type: application/json

{
    "company": "Tesla",
    "topic": "electric vehicles",
    "message": "revolutionary battery technology"
}
```

**Branded Generation** (`/generate_branded`)
```python
POST http://localhost:5001/generate_branded
Content-Type: application/json

{
    "company": "Apple",
    "industry": "tech",
    "brand_voice": "professional",
    "message": "new product launch",
    "topic": "innovation"
}
```

**Smart Generation** (`/generate_smart`)
```python
POST http://localhost:5001/generate_smart
Content-Type: application/json

{
    "company": "Starbucks",
    "message": "new seasonal drink",
    "topic": "coffee",
    "word_count_target": 18,
    "sentiment_target": 0.7,
    "has_media": true,
    "optimal_hour": 14
}
```

**Generate and Predict** (`/generate_and_predict`)
```python
POST http://localhost:5001/generate_and_predict
Content-Type: application/json

{
    "company": "Adidas",
    "tweet_type": "announcement",
    "message": "new running shoe",
    "topic": "marathons",
    "has_media": true,
    "hour": 14
}
```

## 🔧 Configuration

### Model Configuration

The Random Forest model can be retrained by:
1. Updating `data.csv` with new training data
2. Running `initialize.ipynb` to retrain the model
3. The new model will be saved as `like_predictor.pkl`

### Generator Configuration

- **Template Generator**: Modify templates in `generator_simple.py`
- **Advanced Generator**: Adjust brand voices and industry templates in `advanced_generator.py`
- **AI Generator**: Change GPT-2 model parameters in `generator_ai.py`

## 📈 Model Performance

- **Algorithm**: Random Forest Regressor
- **Training Data**: 17,331 tweets
- **Features**: 5 (has_media, char_count, word_count, hour, sentiment)
- **RMSE**: ~3698 (varies with dataset)
- **Key Insights**:
  - Optimal word count: 15-20 words
  - Positive sentiment (0.5-0.8) performs best
  - Media presence increases engagement by 30-50%
  - Peak posting hours: 12-15 PM

## 🧪 Testing

Run the test scripts to verify API functionality:

```bash
# Basic API tests
python testing/test.py

# Advanced generator tests
python testing/test_advanced.py
```

Ensure both APIs are running before executing tests.

## 📝 File Descriptions

### Core Application
- **`app.py`**: Main Streamlit application with UI for generation and prediction

### Generators
- **`generator_simple.py`**: Template-based tweet generator with sentiment logic
- **`advanced_generator.py`**: Advanced generator with brand voice, industry-specific, and ML-optimized modes
- **`generator_ai.py`**: GPT-2 based neural tweet generator

### APIs
- **`like_predictor_api.py`**: Flask API for like prediction
- **`generator_api.py`**: Flask API for tweet generation with multiple endpoints

### Model & Data
- **`initialize.ipynb`**: Jupyter notebook for model training and data exploration
- **`like_predictor.pkl`**: Serialized trained model
- **`data.csv`**: Training dataset with tweet content and engagement metrics

### Testing
- **`test.py`**: Basic API integration tests
- **`test_advanced.py`**: Advanced generator functionality tests

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- TextBlob for sentiment analysis
- Hugging Face Transformers for GPT-2 model
- Scikit-learn for machine learning algorithms
- Streamlit and Flask for web frameworks

## 📧 Contact

For questions, issues, or contributions, please open an issue on GitHub.

## Author
Shreyansh Singh
Btech, IITD

**Note**: The AI generator requires significant computational resources. For production use, consider using GPU acceleration or cloud-based inference services.
