"""
Telegram Bot для магазина Vitamin_krasnodar_123
"""

import logging
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
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
    
    # Если есть product_id, открываем страницу товара
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
        
        # Добавляем основную клавиатуру
        main_keyboard = [
            [KeyboardButton(text="🛒 Открыть магазин", web_app=WebAppInfo(url=WEBAPP_URL))],
            [KeyboardButton(text="📞 Контакты"), KeyboardButton(text="ℹ️ О нас")]
        ]
        await update.message.reply_text(
            "Или используйте меню ниже:",
            reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
        )
        return
    
    # Стандартный /start
    keyboard = [
        [KeyboardButton(text="🛒 Открыть магазин", web_app=WebAppInfo(url=WEBAPP_URL))],
        [KeyboardButton(text="📞 Контакты"), KeyboardButton(text="ℹ️ О нас")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        f"👋 Привет, {user.first_name}!\n\n"
        "Добро пожаловать в магазин **Vitamin_krasnodar_123**!\n\n"
        "🌿 У нас вы найдёте:\n"
        "• Витамины и минералы\n"
        "• БАДы для здоровья взрослых и детей\n"
        "• Спортивные добавки\n\n"
        "Нажмите кнопку ниже, чтобы перейти в магазин.",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📞 **Контакты**\n\n"
        "📍 Адрес: г. Краснодар, ул. Ставропольская 174/1, вход со двора, 3 этаж\n"
        "📱 Телефон: +7 (961) 590-71-87\n",
        parse_mode='Markdown'
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ **О магазине**\n\n"
        "Мы — магазин витаминов и добавок.\n\n"
        "✅ Товары из США, Турции\n"
        "✅ Быстрая доставка\n"
        "✅ Самовывоз",
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "📞 Контакты":
        await contacts(update, context)
    elif text == "ℹ️ О нас":
        await about(update, context)
    else:
        await update.message.reply_text("Нажмите \"🛒 Открыть магазин\" или /start")

async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(
        f"🔑 Ваш Chat ID: `{chat_id}`\n\n"
        "Используйте его в настройках админ-панели.",
        parse_mode='Markdown'
    )

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
