import random

import vk_api
from environs import Env
from vk_api.longpoll import VkLongPoll, VkEventType

from dialogflow import read_credentials, detect_intent_texts
from log import general_logger


def echo(event, vk_api, project_id, language_code):
    general_logger.info('Пришло новое сообщение в VK "{}" от {}'.format(event.text, event.user_id))
    query_result = detect_intent_texts(project_id, event.user_id, event.text, language_code)
    message = query_result.fulfillment_text
    if query_result.intent.is_fallback:
        general_logger.warning("Can't understand message: {}".format(event.text))
        return None
    vk_api.messages.send(
        user_id=event.user_id,
        message=message,
        random_id=random.randint(1, 1000)
    )


def main():
    env = Env()
    env.read_env()
    project_dialogflow_id = read_credentials(env.str('GOOGLE_APPLICATION_CREDENTIALS'))['quota_project_id']
    language_code = env.str('LANGUAGE_CODE')
    vk_session = vk_api.VkApi(token=env.str("VK_ACCESS_TOKEN"))
    vk_get_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    general_logger.info('DialogFlow VK бот запущен')
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_get_api, project_dialogflow_id, language_code)


if __name__ == '__main__':
    main()
