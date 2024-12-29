# Tenali Raman AI Buddy

Welcome to the **Tenali Raman AI Buddy** project! This is a personal AI assistant inspired by the wit and wisdom of Tenali Raman, capable of handling daily tasks and managing reminders. The project is built using Python and Django, and it’s designed to be easily extendable for future features.

## Features

- Conversational interface inspired by Tenali Raman.
- Modular structure for easy feature expansion.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python** (version 3.x)
- **Pip** (Python package installer)
- **Django** (version 3.x or above)

## Installation

Follow these steps to set up the project locally:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your_username/your_repository_name.git
   cd your_repository_name

Create a virtual environment (optional but recommended):
~~~
python -m venv .venv
~~~

Activate the virtual environment:

On Windows:
~~~
.venv\Scripts\activate
~~~
On macOS/Linux:
~~~
source .venv/bin/activate
~~~


Install the required packages:

~~~
pip install -r requirements.txt
~~~

Run database migrations:
~~~
python manage.py migrate
~~~

Create a superuser (optional): If you want to access the Django admin site, create a superuser:
~~~
python manage.py createsuperuser
~~~

Run the development server:
~~~
python manage.py runserver
~~~


#Access the application: Open your web browser and navigate to http://127.0.0.1:8000 to start using your AI buddy.

#Usage
Start a conversation by typing your input into the web interface.
Use commands like "set reminder," "view reminders," and "delete reminder" to interact with the reminder functionality.

#Contributing
If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch:
~~~
git checkout -b feature/YourFeature
~~~
3. Make your changes and commit them:
~~~
git commit -m "Add some feature"
~~~
4. Push to the branch:
~~~
git push origin feature/YourFeature
~~~
5. Open a Pull Request.


