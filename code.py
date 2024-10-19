from telegram import Update, ChatPermissions
from telegram.ext import Updater, MessageHandler, filters, CallbackContext

# Список запрещённых слов и фраз, которые могут указывать на рекламу
BLOCKED_KEYWORDS = ['работа', 'рабочие','разнорабочие','рабочих','разнорабочих','стажировка','стажировки','стажировку','научу','обучу','казино','Казино','КАЗИНО','регистрации', 'выигрыш', 'выигрыша', 'реклама','t.me','долги','долгах','должник','срочно','с деньгами','финансовые проблемы', 'sale', 'http', 'www']

# Список пользователей, которых не нужно блокировать
EXCLUDED_USERS = [1569044523, 5284524433]  # ID пользователей, которых нельзя блокировать

# ID администратора, которому нужно отправлять сообщения
ADMIN_ID = 1569044523  # ID пользователя, которому бот будет отправлять сообщения

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
        # context.bot.send_message(chat_id, f"Пользователь {update.message.from_user.full_name} был заблокирован за спам.")

        # Логируем сообщение о спаме (или отправляем сообщение о спаме в другой чат)
        # context.bot.send_message(chat_id, f"Пользователь {update.message.from_user.full_name} ({user_id}) заблокирован за рекламу.")
        
        # Пересылаем текст сообщения администратору
        context.bot.send_message(ADMIN_ID, f"Заблокированный пользователь: {update.message.from_user.full_name} (ID: {user_id})\n"
                                           f"Текст сообщения: {update.message.text}")

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
