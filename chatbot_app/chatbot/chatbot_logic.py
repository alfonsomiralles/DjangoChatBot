import re, pyttsx3, openai
from ..models import PredefinedAnswer

def update_predefined_answers():
    answers = PredefinedAnswer.objects.all()
    predefined_answers_dict = {}

    for answer in answers:
        keywords = re.findall(r'\w+', answer.keywords.lower())
        for keyword in keywords:
            predefined_answers_dict[keyword] = answer.answer

    return predefined_answers_dict

def find_predefined_answer(question, predefined_answers):
    question_words = question.lower().split()
    question_words = [re.sub(r'[^\w\s]', '', word) for word in question_words]  # Eliminar signos de puntuación

    max_score = 0
    best_answer = None

    for key, answer in predefined_answers.items():
        key_words = key.lower().split()
        match_count = sum([1 for word in question_words if word in key_words])
        score = match_count / len(key_words)

        if score > max_score:
            max_score = score
            best_answer = PredefinedAnswer.objects.get(answer=answer)

    return best_answer if max_score > 0 else None

def synthesize_speech(text):
    tts_engine = pyttsx3.init()
    tts_engine.say(text)
    tts_engine.runAndWait()

def gpt_response(prompt):
    try:
        description = '''
        Eres un asistente del Museo y te debes limitar a responder sobre temas relacionados con museos.
        Si una pregunta no está relacionada con el museo, desvía la respuesta a un asunto relacionado con museos. 
        Por favor, responde de forma breve en español a esta pregunta:
        '''
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[
            {"role": "system", "content":description},
            {"role": "user", "content":prompt},
            ],
            max_tokens = 200,
            temperature = 0.5,)
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(e)
        return None

 
