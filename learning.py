import json
from pathlib import Path

from environs import Env

from dialogflow import create_intent, read_credentials


def learn_chat_bot(project_id, filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        training_phrases = json.load(file)
    for theme in training_phrases:
        questions = training_phrases[theme]['questions']
        answer = training_phrases[theme]['answer']
        create_intent(project_id, theme, questions, answer)


if __name__ == "__main__":
    env = Env()
    env.read_env()
    project_id = read_credentials(env.str('GOOGLE_APPLICATION_CREDENTIALS'))['quota_project_id']
    filepath = Path('questions.json')
    learn_chat_bot(project_id, filepath)
