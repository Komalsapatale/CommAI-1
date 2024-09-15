from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Load the JSON file for predefined responses
try:
    with open('responses.json', 'r') as file:
        responses = json.load(file)
except FileNotFoundError:
    responses = {}

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
    response = responses.get(user_input, "I don't know the  to that. Could you please provide more details?")
    return jsonify({'response': response})

@app.route('/submit', methods=['POST'])
def submit():
    conversation = request.json.get('conversation')
    
    # Append the new conversation to the JSON file
    try:
        with open('conversations.json', 'a') as file:
            json.dump(conversation, file)
            file.write('\n')
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
