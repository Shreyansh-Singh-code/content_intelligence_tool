import datetime
import joblib
import numpy as np
import streamlit as st
from textblob import TextBlob

from advanced_generator import AdvancedTweetGenerator
from generator import SimpleTweetGenerator

# The AI generator is optional because loading GPT-2 is heavy.
try:
    from genenerator_ai import AITweetGenerator
except Exception:
    AITweetGenerator = None


@st.cache_resource
def load_like_model():
    """Load the trained like prediction model once."""
    try:
        return joblib.load("like_predictor.pkl")
    except Exception as exc:  # pragma: no cover - defensive UI warning
        st.warning(f"Could not load like predictor model: {exc}")
        return None


@st.cache_resource
def get_simple_generator():
    return SimpleTweetGenerator()


@st.cache_resource
def get_advanced_generator():
    return AdvancedTweetGenerator()


@st.cache_resource
def get_ai_generator():
    if AITweetGenerator is None:
        return None
    try:
        return AITweetGenerator()
    except Exception as exc:  # pragma: no cover - GPU/CPU env dependent
        st.error(f"AI generator failed to initialize: {exc}")
        return None


def extract_features(tweet_text: str, has_media: bool, hour: int | None):
    """Derive model features from tweet text and metadata."""
    if hour is None:
        hour = datetime.datetime.now().hour

    word_count = len(tweet_text.split())
    char_count = len(tweet_text)
    sentiment = TextBlob(tweet_text).sentiment.polarity

    return {
        "word_count": word_count,
        "char_count": char_count,
        "has_media": int(has_media),
        "hour": hour,
        "sentiment": round(sentiment, 3),
    }


def predict_likes(model, features: dict[str, float]) -> int | None:
    """Run the like predictor model with consistent feature ordering."""
    if model is None:
        return None

    vector = np.array(
        [
            features["word_count"],
            features["char_count"],
            features["has_media"],
            features["hour"],
            features["sentiment"],
        ]
    ).reshape(1, -1)

    try:
        return int(model.predict(vector)[0])
    except Exception as exc:
        st.error(f"Prediction failed: {exc}")
        return None


def main():
    st.set_page_config(page_title="Tweet Generator + Like Predictor", page_icon="🐦")
    st.title("Tweet Generator + Like Predictor")
    st.caption(
        "Generate a tweet using one of the available generators and predict "
        "the likes it might get with the trained Random Forest model."
    )

    generator_type = st.sidebar.selectbox(
        "Generator type",
        [
            "Template (simple)",
            "Advanced (brand voice)",
            "Advanced (smart/optimized)",
            "AI (GPT-2)",
        ],
    )

    st.sidebar.markdown("### Prediction metadata")
    has_media = st.sidebar.checkbox("Has media", value=True)
    posting_hour = st.sidebar.slider("Posting hour (0-23)", 0, 23, 14)

    override_word = st.sidebar.text_input("Override word count (optional)")
    override_char = st.sidebar.text_input("Override char count (optional)")
    override_sent = st.sidebar.text_input("Override sentiment (optional)")

    st.subheader("Tweet inputs")
    company = st.text_input("Company name", value="Acme Corp")
    topic = st.text_input("Topic / hashtag context", value="innovation")
    message = st.text_area("Message / update", value="Launching something new today!")

    tweet_type = "general"
    industry = "tech"
    brand_voice = "casual"
    sentiment_target = 0.6
    word_count_target = 18

    if generator_type.startswith("Template"):
        tweet_type = st.selectbox(
            "Template style", ["general", "announcement", "question"]
        )
    elif "brand voice" in generator_type:
        industry = st.selectbox(
            "Industry",
            ["tech", "food", "fashion", "fitness", "finance"],
            index=0,
        )
        brand_voice = st.selectbox(
            "Brand voice", ["casual", "professional", "playful"], index=0
        )
    elif "smart" in generator_type:
        sentiment_target = st.slider(
            "Target sentiment", -1.0, 1.0, 0.6, help="Positive tweets usually perform better"
        )
        word_count_target = st.slider("Target word count", 5, 40, 18)
        has_media = st.checkbox("Include media (for optimized gen)", value=has_media)
        posting_hour = st.slider("Optimized posting hour", 0, 23, posting_hour)

    model = load_like_model()

    if st.button("Generate & Predict", type="primary"):
        generated_tweet = None
        features_from_generator = None
        smart_result = None

        if generator_type.startswith("Template"):
            generator = get_simple_generator()
            generated_tweet = generator.generate_tweet(
                company=company,
                tweet_type=tweet_type,
                message=message,
                topic=topic,
            )
        elif "brand voice" in generator_type:
            generator = get_advanced_generator()
            generated_tweet = generator.generate_branded_tweet(
                company=company,
                industry=industry,
                brand_voice=brand_voice,
                message=message,
                topic=topic,
            )
        elif "smart" in generator_type:
            generator = get_advanced_generator()
            smart_result = generator.generate_smart_tweet(
                company=company,
                message=message,
                topic=topic,
                word_count_target=word_count_target,
                sentiment_target=sentiment_target,
                has_media=has_media,
                optimal_hour=posting_hour,
            )
            generated_tweet = smart_result["tweet"]
            features_from_generator = smart_result.get("predicted_features", {})
        else:
            ai_gen = get_ai_generator()
            if ai_gen is None:
                st.error("AI generator is unavailable. Check transformers/GPT-2 setup.")
            else:
                prompt = (
                    f"A professional social media post from {company}: "
                    f"{message} about {topic}."
                )
                generated_tweet = ai_gen.generate_ai_tweet(prompt)

        if not generated_tweet:
            st.stop()

        st.success("Generated tweet")
        st.write(generated_tweet)

        # Use features returned by smart generator when available, else derive.
        if features_from_generator:
            features = {
                "word_count": features_from_generator.get("word_count"),
                "char_count": features_from_generator.get("char_count"),
                "has_media": int(features_from_generator.get("has_media", has_media)),
                "hour": features_from_generator.get("hour", posting_hour),
                "sentiment": features_from_generator.get("sentiment"),
            }
        else:
            features = extract_features(generated_tweet, has_media, posting_hour)

        # Apply optional manual overrides if provided.
        if override_word.strip():
            try:
                features["word_count"] = int(override_word)
            except ValueError:
                st.warning("Word count override ignored (must be an integer).")

        if override_char.strip():
            try:
                features["char_count"] = int(override_char)
            except ValueError:
                st.warning("Char count override ignored (must be an integer).")

        if override_sent.strip():
            try:
                features["sentiment"] = float(override_sent)
            except ValueError:
                st.warning("Sentiment override ignored (must be a number).")

        features["has_media"] = int(has_media)
        features["hour"] = posting_hour

        prediction = predict_likes(model, features)

        st.subheader("Prediction")
        if prediction is None:
            st.info("Prediction unavailable. Load the model to enable like estimates.")
        else:
            st.metric("Estimated likes", prediction)

        st.subheader("Features used")
        st.json(features)

        if (
            generator_type.startswith("Advanced (smart")
            and smart_result
            and smart_result.get("optimization_tips")
        ):
            st.subheader("Optimization tips")
            for tip in smart_result["optimization_tips"]:
                st.write(f"- {tip}")

if __name__ == "__main__":
    main()
