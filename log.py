import logging

import environs
from telegram import Bot


class TelegramLogsHandler(logging.Handler):

    def __init__(self, chat_id, log_bot_token):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = Bot(token=log_bot_token)

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def get_logger(token, chat_id, level):

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=level)
    logger = logging.getLogger(__name__)

    logger.addHandler(TelegramLogsHandler(chat_id, token))
    return logger


env = environs.Env()
env.read_env()
general_logger = get_logger(token=env.str('TELEGRAM_LOG_BOT_TOKEN'),
                            chat_id=env.str('TELEGRAM_CHAT_ID'),
                            level=env.str('LOG_LEVEL'))
