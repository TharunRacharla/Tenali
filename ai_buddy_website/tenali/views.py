from .ai_buddy import speak, takeCommand, process_input
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import datetime

# Greeting function endpoint
@require_http_methods(["GET"])
def wish_me(request):
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        greeting = "Good Morning!"
    elif hour < 18:
        greeting = "Good Afternoon!"
    else:
        greeting = "Good Evening!"
    greeting += " I am AI Buddy. How may I help you?"

    speak(greeting)

    return JsonResponse({"greeting": greeting})

# Main home view
@require_http_methods(["GET", "POST"])
def home(request):
    # Check if the bot should stop listening
    # if user_input.lower() == "wake up buddy":
    #     response = "AI Buddy is awake! How can I assist you?"
    #     stop = False

   
    if request.method == "POST":
        user_input = takeCommand().lower()

        # if request.session.get("stop_listening", False):
        #     return JsonResponse({"user_input": "exit", "response": "AI Buddy has stopped listening.", "stop": True})
        
        # if "exit" in user_input:
        #     response = "Goodbye!"
        #     request.session["stop_listening"] = True  # Set flag to stop further listening
        #     return JsonResponse({"user_input": user_input, "response": response, "stop": True})

        # Process other inputs normally
        response = process_input(user_input)
        return JsonResponse({"user_input": user_input, "response": response, "stop": False})

    return render(request, "tenali/home.html")
