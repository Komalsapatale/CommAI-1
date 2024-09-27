from textstat import flesch_reading_ease
from textblob import TextBlob
import re
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Function to evaluate clarity based on Flesch Reading Ease
def evaluate_clarity(text):
    return flesch_reading_ease(text)

# Function to evaluate conciseness (average sentence length)
def evaluate_conciseness(text):
    words = len(text.split())
    sentences = len(text.split('.'))
    avg_sentence_length = words / sentences if sentences != 0 else words
    return avg_sentence_length

# Function to evaluate sentiment (polarity and subjectivity)
def evaluate_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment
    return sentiment.polarity, sentiment.subjectivity

# Function to evaluate engagement (ratio of questions to sentences)
def evaluate_engagement(text):
    questions = len(re.findall(r'\?', text))
    sentences = len(text.split('.'))
    return questions / sentences if sentences != 0 else 0

# Function to evaluate grammar using LanguageTool API
def evaluate_grammar(text):
    url = "https://api.languagetool.org/v2/check"
    data = {'text': text, 'language': 'en-US'}
    response = requests.post(url, data=data)
    result = response.json()
    return len(result.get('matches', []))  # Number of grammar issues

# Function to evaluate vocabulary usage (lexical diversity)
def evaluate_vocabulary_usage(text):
    words = text.split()
    unique_words = set(words)
    return len(unique_words) / len(words) if len(words) != 0 else 0

# Function to evaluate response appropriateness based on cosine similarity
def evaluate_response_appropriateness(response, previous_text=None):
    if not previous_text:
        return 0
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([response, previous_text])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return similarity[0][0]

# Function to evaluate politeness based on keyword occurrence
def evaluate_politeness(text):
    polite_keywords = ["please", "thank you", "kindly", "would you mind", "could you", "appreciate", "grateful", "sorry", "excuse me"]
    text_lower = text.lower()
    polite_count = sum(keyword in text_lower for keyword in polite_keywords)
    return polite_count / len(polite_keywords)

# Function to calculate a composite score based on all metrics
def calculate_composite_score(text, previous_text=None):
    clarity = evaluate_clarity(text)
    conciseness = evaluate_conciseness(text)
    sentiment_polarity, sentiment_subjectivity = evaluate_sentiment(text)
    engagement = evaluate_engagement(text)
    grammar_issues = evaluate_grammar(text)
    vocabulary_usage = evaluate_vocabulary_usage(text)
    response_appropriateness = evaluate_response_appropriateness(text, previous_text)
    politeness = evaluate_politeness(text)
    
    score = 6

    # Weighted sum of all scores, adjust weights as necessary
    # score = (
    #     0.1 * clarity +               # Clarity contributes 20%
    #     0.1 * (50 / conciseness) +     # Conciseness is inversely related (avg sentence length)
    #     0.1 * sentiment_polarity +     # Sentiment polarity contributes 10%
    #     0.1 * engagement +             # Engagement contributes 10%
    #     0.1 * (1 - grammar_issues/10) +# Grammar errors, lower is better
    #     0.1 * vocabulary_usage +       # Vocabulary usage contributes 10%
    #     #0.2 * response_appropriateness + # Appropriateness contributes 20%
    #     0.1 * politeness               # Politeness contributes 10%
    # )
    # print(f"Your score is: {score}")
    
    return score

# Function to select level based on composite score
def select_level(text):
    score = calculate_composite_score(text, previous_text = None)

    if score < 4 or text == '':
        return "Poor"
    elif 4 <= score < 7:
        return "Intermediate"
    else:
        return "Expert"

# Example usage
# if __name__ == "__main__":
#     text_input = "Your sample input text goes here."
#     previous_input = "Previous conversation context if available."
    
#     level = select_level(text_input)
#     print(f"Your conversation level is: {level}")
