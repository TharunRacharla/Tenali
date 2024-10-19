from django.shortcuts import render
from django.http import JsonResponse
from .ai_buddy import tenali_raman_conversation
from .reminder_handler import handle_reminder_flow, get_reminders, delete_reminder

def home(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
        user_input = request.POST.get("user_input").lower()

        # Reminder handling
        reminder_response = handle_reminder_flow(user_input, request.session)
        if reminder_response:
            return JsonResponse({"response": reminder_response})

        elif "view reminders" in user_input:
            reminders = get_reminders()
            if reminders:
                reminders_list = ", ".join([f"{reminder.reminder_text} at {reminder.reminder_time.strftime('%Y-%m-%d %H:%M')}" for reminder in reminders])
                return JsonResponse({"response": f"Here are your reminders: {reminders_list}"})
            else:
                return JsonResponse({"response": "You have no reminders set."})

        elif "delete reminder" in user_input:
            reminder_id = user_input.split()[-1]  # Extract ID from input
            response = delete_reminder(reminder_id)
            return JsonResponse({"response": response})

        elif "set reminder" in user_input:
            request.session['waiting_for_reminder_text'] = True
            return JsonResponse({"response": "Ah! You need to be reminded. What task would you like me to remember for you?"})

        else:
            response = tenali_raman_conversation(user_input)
            return JsonResponse({"response": response})

    return render(request, "tenali/home.html")
