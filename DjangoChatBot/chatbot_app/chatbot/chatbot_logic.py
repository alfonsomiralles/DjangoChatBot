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
            best_answer = answer

    return best_answer if max_score > 0 else None

def synthesize_speech(text):
    tts_engine = pyttsx3.init()
    tts_engine.say(text)
    tts_engine.runAndWait()

def gpt_response(prompt):
    try:
        prompt = f"Por favor, responde en español: {prompt}"
        response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=100, n=1, stop=None, temperature=0.5)
        return response.choices[0].text.strip()
    except Exception as e:
        return None

 
