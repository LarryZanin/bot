from telegram import Update, ChatPermissions
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

# Список запрещённых слов и фраз, которые могут указывать на рекламу
BLOCKED_KEYWORDS = ['подработку','подработка','подработки','награда','Лс', 'рабочие','разнорабочие','рабочих','работы','работа','работ','разнорабочих','стажировка',
                    'стажировки','совершеннолетние','совершеннолетних','курьер','курьеры','курьера','водитель','водители','курьерах','курьеров','водителей','оплата','плата','лс',
                    '18+','16+','напиши','пиши','@','приумножить средства','приумножать средства','приумножение средств',
                    'стажировку','научу','обучу','казино','Казино','КАЗИНО','регистрации', 'выигрыш', 'выигрыша','личку',
                    'реклама','t.me','долги','долгах','должник','срочно','с деньгами', 'деньги','средств','средства',
                    '$','бесплатно','законно','законный','финансовые проблемы', 'sale', 'http', 'www']

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
    if (any(keyword in message_text for keyword in BLOCKED_KEYWORDS) or update.message.photo or update.message.document or update.message.video) and user_id not in EXCLUDED_USERS:
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
       if message_text:
        context.bot.send_message(ADMIN_ID, f"Заблокированный пользователь: {update.message.from_user.full_name} (ID: {user_id})\n"
                                           f"Текст сообщения: {update.message.text}")
       else:
            context.bot.send_message(ADMIN_ID, f"Заблокированный пользователь: {update.message.from_user.full_name} (ID: {user_id}) отправил файл или изображение.")

def main():
    # Используйте токен вашего бота
    updater = Updater("7878820851:AAEBsy6e_crb-QV_e-nlyZ2KISwDGadcwwU")

    # Получаем диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Обрабатываем текстовые сообщения, изображения и документы
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command | Filters.photo | Filters.document | Filters.video, filter_ads))

    # Запускаем бота
    updater.start_polling()

    # Ожидаем завершения работы
    updater.idle()

if __name__ == '__main__':
    main()
