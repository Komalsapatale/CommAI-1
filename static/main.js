let conversation = [];

function sendMessage() {
    const userInput = document.getElementById('userInput').value;
    appendMessage(userInput, 'user');
    conversation.push({ sender: 'user', message: userInput });
    document.getElementById('userInput').value = '';

    // Send user input to the backend
    fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        const aiResponse = data.response;
        appendMessage(aiResponse, 'ai');
        conversation.push({ sender: 'ai', message: aiResponse });
    });
}

function appendMessage(message, sender) {
    const chatBox = document.getElementById('chatBox');
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${sender}`;
    messageDiv.innerText = message;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function submitConversation() {
    const conversationData = JSON.stringify(conversation);

    fetch('/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ conversation: conversationData })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            window.location.href = `/results?data=${encodeURIComponent(conversationData)}`;
        } else {
            alert('Error saving conversation: ' + data.message);
        }
    });
}

function adjustInputHeight() {
    const textarea = document.getElementById('userInput');
    textarea.style.height = 'auto';
    textarea.style.height = (textarea.scrollHeight) + 'px';
}

function checkEnter(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        sendMessage();
    }
}

function startRecognition() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onresult = (event) => {
        const speechResult = event.results[0][0].transcript;
        appendMessage(speechResult, 'user');
        conversation.push({ sender: 'user', message: speechResult });

        // Send speech result to the backend
        fetch('/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: speechResult })
        })
        .then(response => response.json())
        .then(data => {
            const aiResponse = data.response;
            appendMessage(aiResponse, 'ai');
            conversation.push({ sender: 'ai', message: aiResponse });
        });
    };

    recognition.start();
}

