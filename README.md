# Чатботы на базе Dialogflow для Telegram и VKontakte
Проект состоит из двух чатботов, один для Telegram, а другой для VKontakte.
Они созданы для взаимодействия пользователей с сервисами через платформу асинхронного ИИ Dialogflow.
Боты могут обрабатывать стандартные текстовые запросы и отвечать на них в соответствии с заранее определенными шаблонами (intents).
Бот Vkontakte не отвечает пользователю, если он не распознал фразу

[Сообщество VK с ботом ](https://vk.com/sh1t_post1ng)

[Телеграм бот](https://t.me/voice_recognition_dvmn_bot)
## Пример работы
![](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZnlmZGt5cWg1N3V2YnhlNmFtZWd3cnAyd2V5NTI0NjdqdjBnZHdqdiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/DGdRfN1vQbmtzIFu07/giphy.gif)


## Как запустить
Для начала работы с чатботами необходимо выполнить несколько шагов по настройке среды и конфигурации проекта.

1. Клонируйте репозиторий

    ```bash
    git clone https://github.com/barseeek/chatsupport_bot.git
    ```
2. Установите Python и зависимости:
   
    ```bash   
    pip install -r requirements.txt
    ```   
3. Создайте проект в [Dialogflow](https://dialogflow.cloud.google.com/) и настройте агента.
4. Создайте Intents, в котором укажите фразы пользователя и желаемый ответ бота
5. Получите токены доступов и настройте переменные окружения как описано ниже.
6. Запустите ботов
    ```bash   
    python tg_bot.py
    python vk_bot.py
    ```   

## Как настроить
### Обучение бота
С помощью скрипта ```learning.py``` можно обучать чат-бота, считывая фразы из JSON-файла и используя их для создания намерений(Intents) в проекте Dialogflow.
Пример файла questions.json, используемого для обучения:
```json
{
    "theme1": {
       "questions": [
       "What is your name?",
       "Who are you?"
       ],
    "answer": "I am a chatbot."
    },
    "theme2": {
       "questions": [
       "What do you do?",
       "Tell me more about your functions."
       ],
    "answer": "I can help answer your questions."
    }
}
```
Запустим скрипт для обучения, указав в качестве параметра путь к файлу с данными для обучения (по умолчанию ```questions.json```):
```bash
python learning.py -f path/to/your/file.json
```
### Файл учетных записей Google для Dialogflow:

Для взаимодействия с API Dialogflow, вам необходимо создать и настроить файл с ключами Google Cloud. Вот пример файла учетных данных, который следует использовать:

```json
{
  "account": "",
  "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
  "client_secret": "YOUR_CLIENT_SECRET",
  "quota_project_id": "your-project-id",
  "refresh_token": "YOUR_REFRESH_TOKEN",
  "type": "authorized_user",
  "universe_domain": "googleapis.com"
}
```
### Переменные окружения
Для работы чатботов необходимо установить следующие переменные окружения:

```ini
GOOGLE_APPLICATION_CREDENTIALS=Путь к файлу с ключами доступа Dialogflow.
TELEGRAM_BOT_TOKEN=Токен бота Telegram.
TELEGRAM_LOG_BOT_TOKEN=Токен бота Telegram для логгирования
LANGUAGE_CODE=Языковой код (например, ru-RU).
TELEGRAM_CHAT_ID=Идентификатор пользователя Telegram для логгирования.
LOG_LEVEL=Уровень логгирования.
VK_ACCESS_TOKEN=Токен доступа Vkontakte.
```
