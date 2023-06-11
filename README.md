# DjangoChatBot
Customized Chatbot with predefined responses, trained AI and API connected with OpenAI

## Getting Started
To set up the project, follow these steps:

Clone the repository:
```bash
git clone https://github.com/alfonsomiralles/DjangoChatBot.git
```
Make sure to have installed:
- Python 3.10.11
- Django 4.2

Install the requierements:
```bash
pip install -r requirements.txt
```
Perform the database migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```
Run the API at localhost:
```bash
python manage.py runserver
```
## Now the API should be up and running at http://localhost:8000.

Create a superuser:
```bash
python manage.py createsuperuser
```
