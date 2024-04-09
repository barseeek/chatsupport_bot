import logging

import environs
from log import TelegramLogsHandler
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text='Здравствуйте')


def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)


def main():
    env = environs.Env()
    env.read_env()
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=env.str('LOG_LEVEL', 'INFO'))
    chat_id = env.str('TELEGRAM_CHAT_ID')
    log_bot_token = env.str('TELEGRAM_LOG_BOT_TOKEN')
    logger.addHandler(TelegramLogsHandler(chat_id, log_bot_token))

    updater = Updater(env.str('TELEGRAM_BOT_TOKEN'))
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    updater.start_polling()
    logger.info('Бот запущен')

    updater.idle()


if __name__ == '__main__':
    main()
