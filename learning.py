import argparse
import json

from dialogflow import create_intent, read_credentials
from environs import Env


def learn_chat_bot(project_id, filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        training_phrases = json.load(file)
    for theme in training_phrases:
        questions = training_phrases[theme]['questions']
        answer = training_phrases[theme]['answer']
        create_intent(project_id, theme, questions, answer)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a chat bot using phrases from a JSON file.")
    parser.add_argument('-f', '--filepath', type=str, default='questions.json',
                        help="Path to the JSON file containing the training data. Default is 'questions.json'.")

    args = parser.parse_args()
    env = Env()
    env.read_env()
    project_id = read_credentials(env.str('GOOGLE_APPLICATION_CREDENTIALS'))['quota_project_id']
    learn_chat_bot(project_id, args.filepath)
