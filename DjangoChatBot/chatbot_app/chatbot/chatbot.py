import os
import openai
from dotenv import load_dotenv
from .chatbot_logic import find_predefined_answer, gpt_response, update_predefined_answers

load_dotenv()

# Configuración de OpenAI
openai.api_key = os.getenv('API_KEY')

predefined_answers = update_predefined_answers()

def chatbot_get_answer(question):
    global predefined_answers
    predefined_answers = update_predefined_answers()

    answer = find_predefined_answer(question, predefined_answers)

    if answer is None:
        if openai.api_key:
            answer = gpt_response(question)
            if answer is None:
                answer = "Lo siento, no puedo ayudarte en este momento."
        else:
            answer = "Lo siento, la API de OpenAI no está disponible."

    return answer