# buddy/reminder_handler.py

from .models import Reminder
from django.utils.dateparse import parse_datetime

def set_reminder(reminder_text, reminder_time):
    """Set a new reminder."""
    Reminder.objects.create(reminder_text=reminder_text, reminder_time=reminder_time)
    return f"Your reminder for '{reminder_text}' has been set for {reminder_time.strftime('%Y-%m-%d %H:%M')}."

def get_reminders():
    """Retrieve all reminders."""
    return Reminder.objects.all()

def delete_reminder(reminder_id):
    """Delete a reminder by its ID."""
    try:
        reminder = Reminder.objects.get(id=reminder_id)
        reminder.delete()
        return f"Reminder '{reminder.reminder_text}' deleted successfully."
    except Reminder.DoesNotExist:
        return "Reminder not found. Please provide a valid ID."

def handle_reminder_flow(user_input, session):
    """Manage the reminder conversation flow."""
    if session.get('waiting_for_reminder_text'):
        reminder_text = user_input
        session['reminder_text'] = reminder_text
        session['waiting_for_reminder_text'] = False
        session['waiting_for_reminder_time'] = True
        return "Aha! Got it. When should I remind you? (Enter time in YYYY-MM-DD HH:MM format)"

    elif session.get('waiting_for_reminder_time'):
        reminder_time_str = user_input
        reminder_time = parse_datetime(reminder_time_str)
        if reminder_time:
            reminder_text = session.pop('reminder_text', None)
            return set_reminder(reminder_text, reminder_time)
        else:
            return "Hmm... that doesn't seem like a valid time. Please use the format YYYY-MM-DD HH:MM."

    return None
