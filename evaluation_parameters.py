from textstat import flesch_reading_ease
def evaluate_clarity(text):
    return flesch_reading_ease(text)


def evaluate_conciseness(text):
    words = len(text.split())
    sentences = len(text.split('.'))
    avg_sentence_length = words / sentences
    return avg_sentence_length


from textblob import TextBlob
def evaluate_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment
    return sentiment.polarity, sentiment.subjectivity


import re
def evaluate_engagement(text):
    questions = len(re.findall(r'\?', text))
    sentences = len(text.split('.'))
    return questions / sentences

import requests
def evaluate_grammar(text):
    # Set up the LanguageTool API endpoint
    url = "https://api.languagetool.org/v2/check"

    # Prepare the data to be sent in the request
    data = {
        'text': text,
        'language': 'en-US',
    }

    # Make the request to the LanguageTool API
    response = requests.post(url, data=data)
    result = response.json()

    # Format the corrections
    corrections = []
    for match in result.get('matches', []):
        correction = {
            'error': match['context']['text'],
            'suggestion': match['replacements'],
            'message': match['message'],
            'offset': match['offset'],
            'length': match['length']
        }
        corrections.append(correction)

    return corrections


def evaluate_vocabulary_usage(text):
    words = text.split()
    
    if len(words) == 0:
        return 0  # Return 0 or another appropriate value for empty input
    
    unique_words = set(words)
    diversity = len(unique_words) / len(words)
    return diversity



from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
def evaluate_response_appropriateness(response, previous_text = None):
    # Create a TF-IDF vectorizer
    vectorizer = TfidfVectorizer()
    # Fit and transform the texts into TF-IDF vectors
    tfidf_matrix = vectorizer.fit_transform([response, previous_text])
    # Calculate cosine similarity between the two vectors
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return similarity[0][0]


def evaluate_politeness(text):
    polite_keywords = [
        "please", "thank you", "kindly", "would you mind", 
        "could you", "appreciate", "grateful", "sorry", "excuse me"
    ]
    # Normalize text to lower case for comparison
    text_lower = text.lower()
    # Count polite keywords in the text
    polite_count = sum(keyword in text_lower for keyword in polite_keywords)
    # Calculate politeness score (0 to 1)
    total_keywords = len(polite_keywords)
    politeness_score = polite_count / total_keywords
    return politeness_score


def evaluate_text(text):
    results = {
        "Clarity": evaluate_clarity(text),
        "Conciseness": evaluate_conciseness(text),
        "Sentiment": evaluate_sentiment(text),
        "Engagement": evaluate_engagement(text),
        "Grammar and Spelling": evaluate_grammar(text),
        "Vocabulary Usage": evaluate_vocabulary_usage(text),
        "Responce Appropriateness" : "evaluate_response_appropriateness(text, previous_text=text)",
        "Politeness": evaluate_politeness(text)
    }
    
    return results
