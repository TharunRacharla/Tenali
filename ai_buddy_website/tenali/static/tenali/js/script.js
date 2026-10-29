function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (const cookie of cookies) {
            const trimmedCookie = cookie.trim();
            if (trimmedCookie.substring(0, name.length + 1) === `${name}=`) {
                cookieValue = decodeURIComponent(trimmedCookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function appendMessage(speaker, message) {
    const paragraph = document.createElement('p');
    const label = document.createElement('strong');
    label.textContent = `${speaker}: `;
    paragraph.append(label, document.createTextNode(message));
    document.getElementById('conversation').appendChild(paragraph);
    scrollToBottom();
}

function appendConfirmation(token) {
    const controls = document.createElement('div');
    const confirmButton = document.createElement('button');
    const cancelButton = document.createElement('button');
    confirmButton.type = cancelButton.type = 'button';
    confirmButton.textContent = 'Confirm';
    cancelButton.textContent = 'Cancel';

    const resolve = async (confirmed) => {
        confirmButton.disabled = cancelButton.disabled = true;
        try {
            const result = await postPayload({
                confirmation_token: token,
                confirm: confirmed
            });
            appendMessage('AI Buddy', result.response || result.error);
        } catch (error) {
            appendMessage('Error', error.message);
        }
    };

    confirmButton.addEventListener('click', () => resolve(true));
    cancelButton.addEventListener('click', () => resolve(false));
    controls.append(confirmButton, cancelButton);
    document.getElementById('conversation').appendChild(controls);
    scrollToBottom();
}

async function postPayload(payload) {
    const response = await fetch('/home/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(payload)
    });
    const result = await response.json();
    if (!response.ok) {
        throw new Error(result.error || 'The request could not be processed.');
    }
    return result;
}

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('message-form');
    const input = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const speakButton = document.getElementById('speak-button');
    const status = document.getElementById('input-status');
    const processingIndicator = document.getElementById('recognizing-animation');

    const submitMessage = async (text) => {
        sendButton.disabled = true;
        processingIndicator.style.display = 'block';
        status.textContent = '';
        appendMessage('User', text);
        try {
            const result = await postPayload({ text });
            appendMessage('AI Buddy', result.response || '');
            if (result.confirmation_required) {
                appendConfirmation(result.confirmation_token);
            }
        } catch (error) {
            appendMessage('Error', error.message);
        } finally {
            processingIndicator.style.display = 'none';
            sendButton.disabled = false;
        }
    };

    form.addEventListener('submit', (event) => {
        event.preventDefault();
        const text = input.value.trim();
        if (!text) {
            return;
        }
        input.value = '';
        submitMessage(text);
    });

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        speakButton.disabled = true;
        speakButton.title = 'Speech recognition is not supported by this browser.';
    } else {
        const recognition = new SpeechRecognition();
        recognition.lang = 'en-IN';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;
        speakButton.addEventListener('click', () => {
            status.textContent = 'Listening in your browser...';
            speakButton.disabled = true;
            recognition.start();
        });
        recognition.addEventListener('result', (event) => {
            input.value = event.results[0][0].transcript;
            status.textContent = '';
            form.requestSubmit();
        });
        recognition.addEventListener('error', (event) => {
            status.textContent = `Speech recognition failed: ${event.error}. You can type your message instead.`;
        });
        recognition.addEventListener('end', () => {
            speakButton.disabled = false;
        });
    }
});

const bubbleContainer = document.getElementById('bubble-container');
function createBubbles() {
    for (let i = 0; i < 50; i++) {
        const bubble = document.createElement('div');
        bubble.classList.add('bubble');
        bubble.style.width = bubble.style.height = `${getRandomInt(10, 60)}px`;
        bubble.style.left = `${getRandomInt(0, window.innerWidth)}px`;
        bubble.style.animationDuration = `${getRandomInt(10, 20)}s`;
        bubbleContainer.appendChild(bubble);
    }
}

function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min)) + min;
}

function scrollToBottom() {
    const conversationDiv = document.getElementById('conversation');
    conversationDiv.scrollTop = conversationDiv.scrollHeight;
}

createBubbles();
scrollToBottom();
