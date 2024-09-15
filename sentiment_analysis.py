from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_sentiment(response):
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(response)
    return sentiment['compound']

def detect_emotion(response):
    # Placeholder for emotion detection
    emotions = {
        "happy": 0.5,
        "sad": 0.1,
        "angry": 0.1,
        "neutral": 0.3
    }
    return max(emotions, key=emotions.get)
