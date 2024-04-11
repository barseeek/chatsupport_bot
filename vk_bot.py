import random

import vk_api
from environs import Env
from vk_api.longpoll import VkLongPoll, VkEventType
from log import general_logger


def echo(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=random.randint(1,1000)
    )


def main():
    env = Env()
    env.read_env()
    vk_session = vk_api.VkApi(token=env.str("VK_ACCESS_TOKEN"))
    vk_get_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    general_logger.info('DialogFlow VK бот запущен')
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            general_logger.debug('Пришло новое сообщение в VK:{}'.format(event.text) )
            if event.to_me:
                echo(event, vk_get_api)
            else:
                print('От меня для: ', event.user_id)
            print('Текст:', event.text)


if __name__ == '__main__':
    main()
