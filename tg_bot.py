import logging

import environs

from dialogflow import create_api_key, detect_intent_texts, read_credentials
from log import TelegramLogsHandler
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logger = logging.getLogger('bot')


def start(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text='Здравствуйте')


def reply_to_user(update: Update, context: CallbackContext) -> None:
    project_id = context.bot_data['PROJECT_ID']
    language_code = context.bot_data['LANGUAGE_CODE']
    logger.info('Получено сообщение в tg "{}" от {}'.format(update.message.text, update.effective_chat.id))
    message_text = detect_intent_texts(project_id, update.message.chat.id, update.message.text, language_code).fulfillment_text
    update.message.reply_text(message_text)


def main():
    env = environs.Env()
    env.read_env()

    language_code = env.str('LANGUAGE_CODE')
    project_id = read_credentials(env.str('GOOGLE_APPLICATION_CREDENTIALS'))['quota_project_id']
    chat_id = env.str('TELEGRAM_CHAT_ID')

    telegram_log_token = env.str('TELEGRAM_LOG_BOT_TOKEN')
    tg_handler = TelegramLogsHandler(chat_id, telegram_log_token)
    logger.addHandler(tg_handler)
    logger.setLevel(env.str('LOG_LEVEL', 'INFO'))

    create_api_key(project_id, chat_id)
    updater = Updater(env.str('TELEGRAM_BOT_TOKEN'))
    dispatcher = updater.dispatcher
    dispatcher.bot_data['PROJECT_ID'] = project_id
    dispatcher.bot_data['LANGUAGE_CODE'] = language_code
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_to_user))
    updater.start_polling()
    logger.info('DialogFlow TG бот запущен')
    updater.idle()


if __name__ == '__main__':
    main()
