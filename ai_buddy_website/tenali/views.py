from .ai_buddy import process_input
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import datetime
from .actuators import speak
from .sensors import listen
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie, csrf_exempt
import json
from playsound3 import playsound
import logging

logger = logging.getLogger(__name__)

# Greeting function endpoint
@csrf_exempt
@require_http_methods(["GET"])
def wish_me(request):
    """Display greeting message with time-based salutation.
    
    Returns:
        HttpResponse: Renders home template with greeting message
    """
    playsound("tenali\\assets\\sound_effects\\mixkit-high-tech-bleep-confirmation-2520.wav", block=True)
    hour = datetime.datetime.now().hour
    if hour < 12:
        greeting = "Good Morning!"
    elif hour < 18:
        greeting = "Good Afternoon!"
    else:
        greeting = "Good Evening!"
    greeting += " I am AI Buddy. How may I help you?"

    speak(greeting)  # Call the actuator to speak

    # Render the home page with the greeting
    return render(request, "tenali/home.html", {"greeting": greeting})

# Main home view
@csrf_exempt
@require_http_methods(["GET", "POST"])
def home(request):
    """Main AI Buddy home view. Handles voice input and processes commands.
    
    GET: Renders the home page template
    POST: Processes voice input and returns AI buddy response
    
    Returns:
        HttpResponse: Home page template or JSON response with AI buddy reply
    """
    if request.method == "POST":
        try:
            user_input = listen().lower()
            response = process_input(user_input)
            return JsonResponse({"user_input": user_input, "response": response})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    # For GET requests, render the home page
    return render(request, "tenali/home.html")
