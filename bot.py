"""
Telegram Bot для магазина Vitamin_krasnodar_123
С корректной передачей Telegram ID в WebApp
"""

import logging
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup, MenuButtonWebApp
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# ==================== НАСТРОЙКИ ====================
BOT_TOKEN = "8458691733:AAF6NF4dwMHyyFEGBwxV9ZedkIyM5pSGWos"
WEBAPP_URL = "https://tshop-admin.emergent.host"

# ==================== ОБРАБОТЧИКИ ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start с поддержкой deep links"""
    user = update.effective_user
    
    # Проверяем параметр deep link (например: /start product_abc123)
    product_id = None
    if context.args and len(context.args) > 0:
        arg = context.args[0]
        if arg.startswith('product_'):
            product_id = arg.replace('product_', '')
    
    # Формируем URL
    if product_id:
        webapp_url = f"{WEBAPP_URL}/product/{product_id}"
        button_text = "🛒 Открыть товар"
        message_text = f"👋 Привет, {user.first_name}!\n\nНажмите кнопку ниже, чтобы посмотреть товар:"
    else:
        webapp_url = WEBAPP_URL
        button_text = "🛒 Открыть магазин"
        message_text = (
            f"👋 Привет, {user.first_name}!\n\n"
            "Добро пожаловать в магазин **Vitamin\\_krasnodar\\_123**\\!\n\n"
            "🌿 У нас вы найдёте:\n"
            "• Витамины и для взрослых и детей\n"
            "• БАДы для здоровья\n"
            "• Спортивные добавки\n\n"
            "Нажмите кнопку ниже, чтобы перейти в магазин\\."
        )
    
    # Используем InlineKeyboardButton с web_app - это гарантирует передачу user data
    keyboard = [
        [InlineKeyboardButton(text=button_text, web_app=WebAppInfo(url=webapp_url))],
        [InlineKeyboardButton(text="📞 Контакты", callback_data="contacts")],
        [InlineKeyboardButton(text="ℹ️ О нас", callback_data="about")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        message_text,
        reply_markup=reply_markup,
        parse_mode='MarkdownV2'
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик нажатий на inline кнопки"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "contacts":
        await query.message.reply_text(
            "📞 *Контакты*\n\n"
            "📍 Адрес: г\\. Краснодар, ул. Ставропольская, д.174/1, вход со двора, 3 этаж\n"
            "📱 Телефон: \\+7 \\(961\\) 590\\-71\\-87\n",
            parse_mode='MarkdownV2'
        )
    elif query.data == "about":
        await query.message.reply_text(
            "ℹ️ *О магазине*\n\n"
            "Мы — магазин витаминов и добавок\\.\n\n"
            "✅ Товары с iHerb и Турции\n"
            "✅ Быстрая доставка\n"
            "✅ Самовывоз",
            parse_mode='MarkdownV2'
        )

async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для получения Chat ID"""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    await update.message.reply_text(
        f"🔑 *Ваши данные:*\n\n"
        f"Chat ID: `{chat_id}`\n"
        f"User ID: `{user_id}`\n\n"
        f"Используйте Chat ID в настройках админ\\-панели\\.",
        parse_mode='MarkdownV2'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений"""
    await update.message.reply_text(
        "Нажмите /start чтобы открыть магазин"
    )

async def post_init(application):
    """Настройка Menu Button после запуска бота"""
    # Устанавливаем кнопку меню, которая открывает WebApp
    await application.bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="🛒 Магазин",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    )

def main():
    application = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("chatid", get_chat_id))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Обработчик callback query для inline кнопок
    from telegram.ext import CallbackQueryHandler
    application.add_handler(CallbackQueryHandler(button_callback))
    
    print("🤖 Бот запущен!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
