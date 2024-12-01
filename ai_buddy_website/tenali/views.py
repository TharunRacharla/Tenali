from .ai_buddy import process_input
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import datetime
from .actuators import speak
from .sensors import listen
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
import json

# Greeting function endpoint
@ensure_csrf_cookie
@require_http_methods(["GET"])
def wish_me(request):
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
@csrf_protect
@require_http_methods(["GET", "POST"])
def home(request):
    if request.method == "POST":
        try:
            user_input = listen().lower()
            response = process_input(user_input)
            return JsonResponse({"user_input": user_input, "response": response})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    # For GET requests, render the home page
    return render(request, "tenali/home.html")
