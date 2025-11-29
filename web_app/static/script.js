// The Conch - Frontend with Murf TTS Backend

const chatContainer = document.getElementById('chatContainer');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const voiceButton = document.getElementById('voiceButton');
const typingIndicatorTemplate = document.getElementById('typingIndicatorTemplate');

let isProcessing = false;
let recognition = null;
let isRecording = false;
let currentAudio = null;
let countdownInterval = null;
let isConchSpeaking = false;

// Initialize speech recognition for microphone
function initSpeechRecognition() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            messageInput.value = transcript;
            stopRecording();
            // Do NOT auto-send - user must press Enter/Send manually
            messageInput.focus();
        };

        recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            stopRecording();
        };

        recognition.onend = () => {
            stopRecording();
        };

        voiceButton.disabled = false;
        voiceButton.style.opacity = '1';
    } else {
        voiceButton.disabled = true;
        voiceButton.style.opacity = '0.3';
        voiceButton.textContent = 'N/A';
    }
}

// Play audio from URL (Murf-generated audio)
function playAudio(audioUrl) {
    // Skip if no audio URL provided
    if (!audioUrl) {
        return;
    }

    // Stop any currently playing audio
    if (currentAudio) {
        currentAudio.pause();
        currentAudio = null;
    }

    // Disable SPEAK button while Conch is speaking
    isConchSpeaking = true;
    voiceButton.disabled = true;

    // Create and play new audio
    currentAudio = new Audio(audioUrl);

    // Re-enable SPEAK button when audio finishes
    currentAudio.onended = () => {
        isConchSpeaking = false;
        if (recognition !== null && !messageInput.disabled) {
            voiceButton.disabled = false;
        }
    };

    currentAudio.play().catch(err => {
        console.log('Audio autoplay blocked - will play after user interaction');
        // Re-enable on error too
        isConchSpeaking = false;
        if (recognition !== null && !messageInput.disabled) {
            voiceButton.disabled = false;
        }
    });
}

function stopRecording() {
    isRecording = false;
    voiceButton.classList.remove('recording');
    voiceButton.textContent = 'SPEAK';

    // Clear countdown interval if exists
    if (countdownInterval) {
        clearInterval(countdownInterval);
        countdownInterval = null;
    }
}

// Initialize the app
async function init() {
    // Initialize speech recognition
    initSpeechRecognition();

    // Setup start button
    const startButton = document.getElementById('startButton');
    const startOverlay = document.getElementById('startOverlay');

    startButton.addEventListener('click', async () => {
        // Hide overlay
        startOverlay.classList.add('hidden');

        // Load welcome message after user interaction (enables audio autoplay)
        await loadWelcomeMessage();

        // Focus on input
        messageInput.focus();
    });
}

// Load welcome message from server
async function loadWelcomeMessage() {
    try {
        const response = await fetch('/api/welcome');
        const data = await response.json();

        if (data.success) {
            addConchMessage(data.message, data.audio_url, true); // Include audio for welcome
        }
    } catch (error) {
        console.error('Error loading welcome message:', error);
        addConchMessage('Welcome to The Conch. The archive is ready.', null, true);
    }
}

// Add a conch (system) message to the chat
function addConchMessage(message, audioUrl = null, isWelcome = false, isGoodbye = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message conch-message ${isWelcome ? 'welcome-message' : ''} ${isGoodbye ? 'goodbye-message' : ''}`;

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    // Start typing effect
    typeMessage(contentDiv, message);

    // Play audio immediately (simultaneously with typing)
    if (audioUrl) {
        playAudio(audioUrl);
    }

    messageDiv.appendChild(contentDiv);
    chatContainer.appendChild(messageDiv);

    scrollToBottom();
}

// Add a user message to the chat
function addUserMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = message;

    messageDiv.appendChild(contentDiv);
    chatContainer.appendChild(messageDiv);

    scrollToBottom();
}

// Typing effect for messages
function typeMessage(element, text, callback, speed = 25) {
    let index = 0;

    function type() {
        if (index < text.length) {
            element.textContent += text.charAt(index);
            index++;
            scrollToBottom();
            setTimeout(type, speed);
        } else if (callback) {
            callback();
        }
    }

    type();
}

// Show typing indicator
function showTypingIndicator() {
    const indicator = typingIndicatorTemplate.content.cloneNode(true);
    const indicatorDiv = indicator.querySelector('.typing-indicator');
    indicatorDiv.id = 'typingIndicator';
    chatContainer.appendChild(indicatorDiv);
    scrollToBottom();
}

// Hide typing indicator
function hideTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.remove();
    }
}

// Send message to server
async function sendMessage() {
    const message = messageInput.value.trim();

    if (!message || isProcessing) {
        return;
    }

    // Add user message to chat
    addUserMessage(message);

    // Clear input IMMEDIATELY
    messageInput.value = '';

    // Set processing state
    isProcessing = true;
    sendButton.disabled = true;
    voiceButton.disabled = true;

    // Show typing indicator
    showTypingIndicator();

    try {
        // Send to server
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        // Hide typing indicator
        hideTypingIndicator();

        if (data.success) {
            // Add conch response with Murf audio
            addConchMessage(data.message, data.audio_url, false, data.is_goodbye);

            // If goodbye, disable input
            if (data.is_goodbye) {
                messageInput.disabled = true;
                sendButton.disabled = true;
                voiceButton.disabled = true;
                messageInput.placeholder = "> Conversation ended. Reload to start again.";
            }
        } else {
            addConchMessage('The conch is silent... Please try again.', null, false);
        }

    } catch (error) {
        console.error('Error sending message:', error);
        hideTypingIndicator();
        addConchMessage('Connection error. Please try again.', null, false);
    } finally {
        // Reset processing state
        isProcessing = false;
        if (!messageInput.disabled) {
            sendButton.disabled = false;
            // Only re-enable voice button if not speaking and recognition available
            voiceButton.disabled = (recognition === null || isConchSpeaking);
            messageInput.focus();
        }
    }
}

// Toggle voice recording
function toggleVoiceRecording() {
    if (!recognition) {
        return;
    }

    // Don't allow recording if Conch is speaking
    if (isConchSpeaking) {
        return;
    }

    if (isRecording) {
        recognition.stop();
        stopRecording();
    } else {
        try {
            recognition.start();
            isRecording = true;
            voiceButton.classList.add('recording');

            // Start 5-second countdown
            let timeLeft = 5;
            voiceButton.textContent = `RECORDING... ${timeLeft}s`;

            countdownInterval = setInterval(() => {
                timeLeft--;
                if (timeLeft > 0) {
                    voiceButton.textContent = `RECORDING... ${timeLeft}s`;
                } else {
                    // Stop recording after 5 seconds
                    recognition.stop();
                    stopRecording();
                }
            }, 1000);

        } catch (error) {
            console.error('Failed to start recognition:', error);
            stopRecording();
        }
    }
}

// Scroll to bottom of chat
function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Event listeners
sendButton.addEventListener('click', sendMessage);
voiceButton.addEventListener('click', toggleVoiceRecording);

messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Initialize on page load
window.addEventListener('DOMContentLoaded', init);
