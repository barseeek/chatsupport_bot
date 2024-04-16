import logging

import environs
from dialogflow import create_api_key, detect_intent_texts, read_credentials
from log import TelegramLogsHandler
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


logger = logging.getLogger('bot')


def start(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text='Здравствуйте')


def echo(update: Update, context: CallbackContext) -> None:
    logger.info('Получено сообщение в tg "{}" от {}'.format(update.message.text, update.effective_chat.id))
    message_text = detect_intent_texts(PROJECT_ID, CHAT_ID, update.message.text, LANGUAGE_CODE).fulfillment_text
    update.message.reply_text(message_text)


def main():
    create_api_key(PROJECT_ID, CHAT_ID)
    updater = Updater(env.str('TELEGRAM_BOT_TOKEN'))
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    updater.start_polling()
    logger.info('DialogFlow TG бот запущен')
    updater.idle()


if __name__ == '__main__':
    env = environs.Env()
    env.read_env()

    LANGUAGE_CODE = env.str('LANGUAGE_CODE')
    PROJECT_ID = read_credentials(env.str('GOOGLE_APPLICATION_CREDENTIALS'))['quota_project_id']
    CHAT_ID = env.str('TELEGRAM_CHAT_ID')
    telegram_log_token = env.str('TELEGRAM_LOG_BOT_TOKEN')
    tg_handler = TelegramLogsHandler(CHAT_ID, telegram_log_token)
    logger.addHandler(tg_handler)
    logger.setLevel(env.str('LOG_LEVEL', 'INFO'))

    main()
