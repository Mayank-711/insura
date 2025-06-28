document.addEventListener('DOMContentLoaded', function() {
    const chatbotBtn = document.getElementById('chatbotBtn');
    const chatbot = document.getElementById('chatbot');
    const closeChatbot = document.getElementById('closeChatbot');
    const chatBody = document.getElementById('chatBody');
    const userInput = document.getElementById('userInput');
    const sendMessageBtn = document.getElementById('sendMessage');
    
    // Toggle chatbot visibility
    chatbotBtn.addEventListener('click', function() {
        chatbot.classList.toggle('active');
    });
    
    closeChatbot.addEventListener('click', function() {
        chatbot.classList.remove('active');
    });
    
    // Add message to chat
    function addMessage(text, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${isUser ? 'user-message' : 'bot-message'}`;
        
        const messageContent = document.createElement('p');
        messageContent.innerHTML = text;
        messageDiv.appendChild(messageContent);
        
        chatBody.appendChild(messageDiv);
        chatBody.scrollTop = chatBody.scrollHeight;
    }
    
    // Show typing indicator
    function showTyping() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'chat-message bot-message typing-indicator';
        typingDiv.innerHTML = `
            <p>Insurance Advisor is typing <span class="typing-dots">
                <span></span><span></span><span></span>
            </span></p>
        `;
        chatBody.appendChild(typingDiv);
        chatBody.scrollTop = chatBody.scrollHeight;
        return typingDiv;
    }
    
    // Get CSRF token
    function getCSRFToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return cookieValue;
    }
    
    // Send message to backend
    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;
        
        addMessage(message, true);
        userInput.value = '';
        
        const typingElement = showTyping();
        
        try {
            const response = await fetch('/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({ message })
            });
            
            typingElement.remove();
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.error) {
                addMessage(`Error: ${data.error}`);
            } else {
                if (data.level === 'general') {
                    addMessage(data.response);
                } else if (data.level === 'full_analysis') {
                    const resp = data.response;
                    
                    let profileText = "<strong>Your Profile:</strong><br>";
                    profileText += `Age: ${resp.profile.age || 'Not specified'}<br>`;
                    profileText += `Occupation: ${resp.profile.occupation || 'Not specified'}<br>`;
                    profileText += `Income: ${resp.profile.income_bracket || 'Not specified'}<br>`;
                    profileText += `Risk Appetite: ${resp.profile.risk_appetite || 'Not specified'}`;
                    addMessage(profileText);
                    
                    addMessage("<strong>Recommended Plans:</strong><br>" + resp.recommendations.replace(/\n/g, '<br>'));
                    
                    if (resp.comparison && !resp.comparison.includes("None")) {
                        addMessage("<strong>Plan Comparison:</strong><br>" + resp.comparison.replace(/\n/g, '<br>'));
                    }
                    
                    addMessage("<strong>Summary:</strong><br>" + resp.summary.replace(/\n/g, '<br>'));
                } else {
                    addMessage("I'm not sure how to respond to that. Could you rephrase?");
                }
            }
        } catch (error) {
            typingElement.remove();
            addMessage("Sorry, there was an error processing your request. Please try again.");
            console.error('Error:', error);
        }
    }
    
    // Event listeners
    sendMessageBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') sendMessage();
    });
});