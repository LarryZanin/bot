from telegram import Update, ChatPermissions
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
import os

# Список запрещённых слов и фраз, которые могут указывать на рекламу
BLOCKED_KEYWORDS = []

# Список пользователей, которых не нужно блокировать
EXCLUDED_USERS = [1569044523, 5284524433]  # ID пользователей, которых нельзя блокировать

# ID администратора, которому нужно отправлять сообщения
ADMIN_ID = 1569044523  # ID пользователя, которому бот будет отправлять сообщения

# Путь к файлу для хранения списка запрещенных слов
BLOCKED_KEYWORDS_FILE = "blocked_keywords.txt"

# Функция для обновления списка запрещённых слов из файла
def update_blocked_keywords():
    global BLOCKED_KEYWORDS
    try:
        with open(BLOCKED_KEYWORDS_FILE, 'r', encoding='utf-8') as file:
            # Читаем файл и обновляем список запрещённых слов
            BLOCKED_KEYWORDS = [line.strip().lower() for line in file.readlines()]
            
        # Отправляем уведомление администратору об обновлении списка
        context.bot.send_message(
            chat_id=ADMIN_ID, 
            text=f"Список запрещённых слов обновлён. Текущее количество слов: {len(BLOCKED_KEYWORDS)}."
        )
    except FileNotFoundError:
        context.bot.send_message(
            chat_id=ADMIN_ID, 
            text=f"Файл {BLOCKED_KEYWORDS_FILE} не найден. Используется пустой список."
        )


# Функция для проверки сообщений на наличие рекламы
def filter_ads(update: Update, context: CallbackContext) -> None:
    # Получаем текст сообщения и ID пользователя
    message_text = update.message.text.lower() if update.message.text else ""
    user_id = update.message.from_user.id

    # Проверяем, содержится ли в тексте одно из запрещённых слов
    if (any(keyword in message_text for keyword in BLOCKED_KEYWORDS) or update.message.photo or update.message.document or update.message.video or update.message.forward_date) and user_id not in EXCLUDED_USERS:
        # Удаляем сообщение
        update.message.delete()

        # Блокируем пользователя (кикаем его из чата)
        chat_id = update.message.chat.id
        context.bot.kick_chat_member(chat_id, user_id)

        # Отправляем сообщение о блокировке в чат
        # context.bot.send_message(chat_id, f"Пользователь {update.message.from_user.full_name} был заблокирован за спам.")

        # Логируем сообщение о спаме (или отправляем сообщение о спаме в другой чат)
        # context.bot.send_message(chat_id, f"Пользователь {update.message.from_user.full_name} ({user_id}) заблокирован за рекламу.")

        # Пересылаем текст сообщения администратору
        context.bot.send_message(ADMIN_ID, f"Заблокированный пользователь: {update.message.from_user.full_name} (ID: {user_id})\n"
                                           f"Текст сообщения: {update.message.text}")
        
# Функция для получения и обработки .txt файла от администратора
def handle_admin_file(update: Update, context: CallbackContext) -> None:
    if update.message.document and update.message.document.file_name.endswith('.txt'):
        user_id = update.message.from_user.id

        # Проверяем, что сообщение пришло от администратора в личном чате
        if user_id == ADMIN_ID and update.message.chat.type == 'private':
            # Скачиваем файл
            file = update.message.document.get_file()
            file.download(BLOCKED_KEYWORDS_FILE)

            # Обновляем список запрещённых слов
            update_blocked_keywords(context)

            # Подтверждаем успешное обновление списка
            context.bot.send_message(
                chat_id=ADMIN_ID, 
                text="Файл успешно загружен и список запрещённых слов обновлён."
            )
def main():
    # Используйте токен вашего бота
    updater = Updater("7878820851:AAEBsy6e_crb-QV_e-nlyZ2KISwDGadcwwU")

    # Получаем диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Обрабатываем текстовые сообщения, изображения и документы
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command | Filters.photo | Filters.document | Filters.video | Filters.forwarded, filter_ads))
  
    # Обрабатываем файлы от администратора в личных сообщениях
    dispatcher.add_handler(MessageHandler(
        Filters.document.file_extension("txt") & Filters.private, 
        handle_admin_file))
  
    # Запускаем бота
    updater.start_polling()
  
    # Загружаем начальный список запрещённых слов
    update_blocked_keywords(updater.bot)

    # Ожидаем завершения работы
    updater.idle()

if __name__ == '__main__':
    main()
