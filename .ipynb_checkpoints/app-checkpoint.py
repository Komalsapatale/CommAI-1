from flask import Flask, render_template, request, jsonify
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import json
# from evaluation_parameters import evaluate_clarity, evaluate_conciseness, evaluate_sentiment, evaluate_engagement, evaluate_grammarm, evaluate_vocabulary_usage, evaluate_response_appropriateness, evaluate_politeness

app = Flask(__name__)

# Chatbot setup
template = """
You are now conversational assistent for CommAI Project, make conversation with the user and answer the questions below in less words.
Here is the conversation history: {context}
Question: {question}
Answer:
"""
model = OllamaLLM(model='llama3')
prompt = ChatPromptTemplate.from_template(template)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/text')
def text_interface():
    return render_template('text_interface.html')

@app.route('/speech')
def speech_interface():
    return render_template('speech_interface.html')

@app.route('/results')
def results():
    data = request.args.get('data')
    try:
        conversation = json.loads(data)
    except json.JSONDecodeError:
        conversation = []
    return render_template('results.html', conversation=conversation)

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get('message')
    conversation = request.json.get('conversation', '')

    user_input = user_input.capitalize()

    # Append the user input to the conversation history
    conversation += f"\nUser: {user_input}"

    # Generate AI response using the model
    result = prompt | model
    ai_response = result.invoke({"context": conversation, "question": user_input})

    # Append the AI response to the conversation
    conversation += f"\nAI: {ai_response}"

    # Return the conversation and AI response as JSON
    return jsonify({'response': ai_response, 'conversation': conversation})

@app.route('/submit', methods=['POST'])
def submit():
    conversation = request.json.get('conversation')

    # Overwrite the previous conversation in the JSON file
    try:
        with open('conversations.json', 'w') as file:  # Use 'w' to overwrite
            json.dump(conversation, file)
        
        # Redirect to the results page with the conversation as a JSON string
        conversation_data = json.dumps(conversation)
        return jsonify({'status': 'success', 'redirect': f'/results?data={conversation_data}'})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
