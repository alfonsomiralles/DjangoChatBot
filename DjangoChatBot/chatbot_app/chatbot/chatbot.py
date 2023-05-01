import os
import openai
from dotenv import load_dotenv
from .chatbot_logic import find_predefined_answer, gpt_response, update_predefined_answers
from evaluation.models import Evaluation

load_dotenv()

# Configuración de OpenAI
openai.api_key = os.getenv('API_KEY')

predefined_answers = update_predefined_answers()

def chatbot_get_answer(user, question, user_rating_choice, evaluation_id=None):
    global predefined_answers
    predefined_answers = update_predefined_answers()

    answer_obj = find_predefined_answer(question, predefined_answers)

    if answer_obj is None:
        if openai.api_key:
            gpt_answer = gpt_response(question)
            if gpt_answer is None:
                gpt_answer = "Lo siento, no puedo ayudarte en este momento."
        else:
            gpt_answer = "Lo siento, la API de OpenAI no está disponible."
    else:
        gpt_answer = answer_obj.answer

    if evaluation_id is not None:
        evaluation = Evaluation.objects.get(id=evaluation_id)
        evaluation.user_rating_choice = user_rating_choice
        evaluation.save()
    else:
        evaluation = save_evaluation(user, question, answer_obj, gpt_answer, user_rating_choice)

    return (answer_obj.answer if answer_obj else gpt_answer, evaluation)


def save_evaluation(user, question, answer, gpt_answer, user_rating):
    evaluation = Evaluation(
        user=user,
        question=question,
        answer=answer if answer is not None else None,
        gpt_answer=gpt_answer,
        user_rating_choice=user_rating
    )
    evaluation.save()
    return evaluation