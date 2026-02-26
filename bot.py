"""
Telegram Bot для магазина Vitamin_krasnodar_123
"""

import logging
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
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
    
    # Формируем URL магазина
    if product_id:
        webapp_url_with_product = f"{WEBAPP_URL}/product/{product_id}"
        
        keyboard = [[InlineKeyboardButton(
            text="🛒 Открыть товар",
            web_app=WebAppInfo(url=webapp_url_with_product)
        )]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"👋 Привет, {user.first_name}!\n\n"
            "Нажмите кнопку ниже, чтобы посмотреть товар:",
            reply_markup=reply_markup
        )
        return
    
    # Стандартный /start без параметров
    welcome_text = f"""
👋 Привет, {user.first_name}!

Добро пожаловать в магазин **Vitamin_krasnodar_123**!

🌿 У нас вы найдёте:
• Витамины и минералы
• БАДы для здоровья
• Спортивное питание

Нажмите кнопку меню слева от поля ввода, чтобы перейти в магазин.
"""
    
    await update.message.reply_text(
        welcome_text,
        parse_mode='Markdown'
    )

async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для получения Chat ID"""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    await update.message.reply_text(
        f"🔑 **Ваши данные:**\n\n"
        f"Chat ID: `{chat_id}`\n"
        f"User ID: `{user_id}`",
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений"""
    await update.message.reply_text("Нажмите кнопку меню или /start")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("chatid", get_chat_id))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 Бот запущен!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
