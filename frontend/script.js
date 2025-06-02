document.addEventListener('DOMContentLoaded', () => {
    const messageHistory = document.getElementById('message-history');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    
    // Connect to WebSocket
    const socket = new WebSocket(`ws://${window.location.host}/ws/chat`);
    
    // Handle incoming messages
    socket.onmessage = (event) => {
        addMessage(event.data, 'bot');
    };
    
    // Handle errors
    socket.onerror = (error) => {
        addMessage('Connection error. Please refresh the page.', 'bot');
    };
    
    // Send message function
    function sendMessage() {
        const message = userInput.value.trim();
        if (message) {
            addMessage(message, 'user');
            socket.send(message);
            userInput.value = '';
        }
    }
    
    // Add message to chat
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${sender}-message`);
        messageDiv.textContent = text;
        messageHistory.appendChild(messageDiv);
        messageHistory.scrollTop = messageHistory.scrollHeight;
    }
    
    // Event listeners
    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
});