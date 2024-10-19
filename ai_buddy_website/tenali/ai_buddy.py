# import random
# import pyttsx3
# from ai_buddy_website.tenali.reminders import setup_database, add_reminder, get_reminders, delete_reminder

# #initialize text to speech engine
# engine = pyttsx3.init()

# # Basic command-response dictionary

# responses = {
#     "hello": ["Hello, how can I assist you today?", "Greetings! What do you need help with?"],
#     "how are you": ["I'm doing great, thanks! How about you?", "I'm a bit of code, but feeling witty!"],
#     "what's your name": ["I'm your clever AI buddy, modeled after Tenali Raman!", "Call me Tenali, your AI assistant!"],
#     "bye": ["Goodbye! Have a great day ahead!", "See you soon!"],
#     "set reminder": ["Sure, what would you like me to remind you about?"],
#     "time": ["The current time is..."],
#     "solve this problem": ["Let me think like Tenali... Here's a clever solution!"]
# }

# #function to get a response
# def get_response(user_input):
#     #convert user input to lower_case
#     user_input = user_input.lower()

#     if "set_remainder" in user_input:
#         return "What would you like me to remind you about?"
    
#     elif "view reminders" in user_input:
#         reminders = get_reminders
#         if reminders:
#             response = "Here are your reminders:\n"
#             for rem in reminders:
#                 response += f"{rem[0]}: {rem[1]} at {rem[2]}\n"
#             return response
#         else:
#             return "You have no reminders."
    
#     elif "delete remainder" in user_input:
#         return "Which reminder ID would you like to delete?"
    
#     elif user_input in responses:
#         return random.choice(responses[user_input])
    
#     return "Sorry, I didn't understand that. Can you try again?"
    

# #function to speak the response
# def speak_response(response):
#     engine.say(response)
#     engine.runAndWait()

# #Main loop
# def main():
#     print("Hello! I am Tenali. Type 'bye' to exit.")

#     while True:
#         user_input = input("You: ")

#         if "set reminder" in user_input.lower():
#             print("AI Buddy: What should I remind you about?")
#             reminder_text = input("You: ")
#             print("AI Buddy: When should I remind you? (Format: YYYY-MM-DD HH:MM)")
#             reminder_time = input("You: ")

#             # Add the reminder to the database
#             add_reminder(reminder_text, reminder_time)
#             print("AI Buddy: Reminder set!")

#         elif "view reminders" in user_input.lower():
#             response = get_response(user_input)
#             print(f"AI Buddy: {response}")
        
#         elif "delete reminder" in user_input.lower():
#             print("AI Buddy: Which reminder ID would you like to delete?")
#             reminder_id = input("You: ")
#             delete_reminder(reminder_id)
#             print(f"AI Buddy: Reminder {reminder_id} deleted!")

#         elif user_input.lower() == "bye":
#             response = get_response(user_input)
#             print(f"AI Buddy: {response}")
#             speak_response(response)
#             break

#         else:
#             response = get_response(user_input)
#             print(f"AI Buddy: {response}")
#             speak_response(response)


# if __name__ == "__main__":
#     main()



# buddy/ai_buddy.py

def tenali_raman_conversation(user_input):
    # Tenali Raman-style wit and conversational responses
    if "hello" in user_input:
        return "Hello, my friend! What wisdom can I impart today?"
    elif "how are you" in user_input:
        return "As wise as ever! But how may I serve your brilliant mind?"
    elif "who are you" in user_input:
        return "I am your trusty friend, Tenali! Ready to assist you with wit and wisdom!"
    elif "joke" in user_input:
        return "Why did the mathematician bring a ladder to the bar? To work on some higher-level thinking!"
    else:
        return "Hmm, that’s an interesting question. Let me think... or perhaps you'd prefer a reminder or a clever solution?"
