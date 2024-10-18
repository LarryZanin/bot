from telegram import Update, ChatPermissions
from telegram.ext import Updater, MessageHandler, filters, CallbackContext

# Список запрещённых слов и фраз, которые могут указывать на рекламу
BLOCKED_KEYWORDS = ['скидка', 'акция', 'купить', 'реклама', 'sale', 'http', 'www']

# Список пользователей, которых не нужно блокировать
EXCLUDED_USERS = [1569044523, 5284524433]  # ID пользователей, которых нельзя блокировать

# Функция для проверки сообщений на наличие рекламы
def filter_ads(update: Update, context: CallbackContext) -> None:
    # Получаем текст сообщения и ID пользователя
    message_text = update.message.text.lower()
    user_id = update.message.from_user.id

    # Проверяем, содержится ли в тексте одно из запрещённых слов
    if any(keyword in message_text for keyword in BLOCKED_KEYWORDS) and user_id not in EXCLUDED_USERS:
        # Удаляем сообщение
        update.message.delete()

        # Блокируем пользователя (кикаем его из чата)
        chat_id = update.message.chat.id
        context.bot.kick_chat_member(chat_id, user_id)

        # Отправляем сообщение о блокировке в чат
        context.bot.send_message(chat_id, f"Пользователь {update.message.from_user.full_name} был заблокирован за спам.")

        # Логируем сообщение о спаме (или отправляем сообщение о спаме в другой чат)
       # context.bot.send_message(chat_id, f"Пользователь {update.message.from_user.full_name} ({user_id}) заблокирован за рекламу.")

        # Можно также уведомить администратора о блокировке или отправить "жалобу"
        # (это опционально, т.к. отправка жалоб на спам напрямую не поддерживается API)

def main():
    # Используйте токен вашего бота
    updater = Updater("7878820851:AAEBsy6e_crb-QV_e-nlyZ2KISwDGadcwwU")

    # Получаем диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Обрабатываем все текстовые сообщения
    dispatcher.add_handler(MessageHandler(filters.text & ~filters.command, filter_ads))

    # Запускаем бота
    updater.start_polling()

    # Ожидаем завершения работы
    updater.idle()

if __name__ == '__main__':
    main()
