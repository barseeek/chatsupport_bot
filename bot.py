import logging

import environs
from dialogflow import create_api_key, detect_intent_texts, read_credentials
from log import general_logger
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


env = environs.Env()
env.read_env()

LANGUAGE_CODE = 'ru-RU'
PROJECT_ID = read_credentials(env.str('GOOGLE_APPLICATION_CREDENTIALS'))['quota_project_id']
CHAT_ID = env.str('TELEGRAM_CHAT_ID')


def start(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text='Здравствуйте')


def echo(update: Update, context: CallbackContext) -> None:
    message_text = detect_intent_texts(PROJECT_ID, CHAT_ID, update.message.text, LANGUAGE_CODE)
    update.message.reply_text(message_text)


def main():
    create_api_key(PROJECT_ID, CHAT_ID)
    updater = Updater(env.str('TELEGRAM_BOT_TOKEN'))
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    updater.start_polling()
    general_logger.info('DialogFlow бот запущен')

    updater.idle()


if __name__ == '__main__':
    main()
