# DjangoChatBot
Customized Chatbot with predefined responses, trained AI and API connected with OpenAI

## YouTube video demo
https://youtu.be/ShxIssICgYg?si=bJWW8Vt29aFUdDKb

## Take a look
![image](https://github.com/alfonsomiralles/DjangoChatBot/assets/62959463/b8565305-1442-4d6d-a88f-2a874379a55a)

![image](https://github.com/alfonsomiralles/DjangoChatBot/assets/62959463/d0b4b71b-44de-4bc1-be29-f70d221d090b)

![image](https://github.com/alfonsomiralles/DjangoChatBot/assets/62959463/32f12ec1-6ac6-43c4-bc27-dc1791cb9e55)

![image](https://github.com/alfonsomiralles/DjangoChatBot/assets/62959463/d5c41af5-c854-4b11-9ee2-337f327694e9)

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
