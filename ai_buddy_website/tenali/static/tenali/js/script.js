function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

$(document).ready(function () {
    let greeted = false; // Track if the user has been greeted
    let stopConversation = false; // Track if the conversation should stop

    function startConversation() {
        if (stopConversation) return; // End the function if conversation is stopped

        // Greet the user only once
        if (!greeted) {
            greeted = true;
            $.ajax({
                url: '/wish-me/', // Endpoint for greeting
                type: 'GET',
                success: function (data) {
                    $('#conversation').append(
                        `<p><strong>AI Buddy:</strong> ${data.greeting}</p>`
                    );
                },
                error: function (xhr, status, error) {
                    console.error('Error fetching greeting:', error);
                    $('#conversation').append(
                        `<p><strong>Error:</strong> Could not load greeting. Please refresh the page.</p>`
                    );
                },
            });
        }
        $.ajaxSetup({
            headers: {
                'X-CSRFToken': csrftoken
            }
        });
        // Start listening animation
        $('#listening-animation').show();
        $('#recognizing-animation').hide();

        // Simulate delay for conversation
        setTimeout(function () {
            // Hide listening animation and show recognizing animation
            $('#listening-animation').hide();
            $('#recognizing-animation').show();
            
            // Send POST request to recognize user input
            $.ajax({
                url: '/recognize/', // Endpoint for command recognition
                type: 'POST',
                // contentType: 'application/json', // Send JSON payload
                data: {
                    //
                },
                success: function (data) {
                    // Hide recognizing animation
                    $('#recognizing-animation').hide();

                    if (data.stop) {
                        // End conversation if stop flag is received
                        $('#conversation').append(
                            `<p><strong>AI Buddy:</strong> ${data.response}</p>`
                        );
                        stopConversation = true;
                        return;
                    }

                    // Append user input and AI Buddy's response
                    $('#conversation').append(
                        `<p><strong>User:</strong> ${data.user_input}</p>
                         <p><strong>AI Buddy:</strong> ${data.response}</p>`
                    );

                    // Scroll to the bottom of the conversation
                    scrollToBottom();

                    // Continue conversation
                    startConversation();
                },
                error: function (xhr, status, error) {
                    // Hide recognizing animation
                    $('#recognizing-animation').hide();

                    // Display error message
                    $('#conversation').append(
                        `<p><strong>Error:</strong> ${error}</p>`
                    );
                },
            });
        }, 2000); // Simulated processing delay
    }
    // Initialize the conversation
    startConversation();
});
// Bubble Animation
const bubbleContainer = document.getElementById('bubble-container');
function createBubbles() {
    for (let i = 0; i < 50; i++) {
        const bubble = document.createElement('div');
        bubble.classList.add('bubble');
        bubble.style.width = bubble.style.height = `${getRandomInt(
            10,
            60
        )}px`;
        bubble.style.left = `${getRandomInt(0, window.innerWidth)}px`;
        bubble.style.animationDuration = `${getRandomInt(10, 20)}s`;
        bubbleContainer.appendChild(bubble);
    }
}
function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min)) + min;
}
createBubbles();
// Function to scroll to the bottom of the conversation
function scrollToBottom() {
    const conversationDiv = document.getElementById('conversation');
    conversationDiv.scrollTop = conversationDiv.scrollHeight;
}
scrollToBottom();

