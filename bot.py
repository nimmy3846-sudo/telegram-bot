import random
import string
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = "8838766761:AAGk4quvFD3qRzlZBQ3HxR-3qtFLuZt0nVs"

TOTAL_CAPTCHAS = 20000000

user_data_store = {}


def generate_captcha():
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=4))


def menu_keyboard():
    return ReplyKeyboardMarkup(
        [["Next", "Withdraw", "Vault"]],
        resize_keyboard=True
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    user_data_store[user_id] = {
        "count": 0,
        "captcha": generate_captcha()
    }

    captcha = user_data_store[user_id]["captcha"]

    await update.message.reply_text(
        f"""
🔐 CAPTCHA TASK

Captcha 1 / {TOTAL_CAPTCHAS}

Type this captcha:

{captcha}
""",
        reply_markup=menu_keyboard()
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if user_id not in user_data_store:
        await update.message.reply_text(
            "Send /start first",
            reply_markup=menu_keyboard()
        )
        return

    data = user_data_store[user_id]

    if text.lower() == "withdraw":
        await update.message.reply_text(
            "💸 Withdraw system coming soon",
            reply_markup=menu_keyboard()
        )
        return

    if text.lower() == "vault":
        await update.message.reply_text(
            f"🏦 Vault\nCompleted: {data['count']} captchas",
            reply_markup=menu_keyboard()
        )
        return

    if text.lower() == "next":
        data["captcha"] = generate_captcha()

        await update.message.reply_text(
            f"""
🔐 NEXT CAPTCHA

Captcha {data['count'] + 1} / {TOTAL_CAPTCHAS}

Type this:

{data['captcha']}
""",
            reply_markup=menu_keyboard()
        )
        return

    if text.upper() == data["captcha"]:
        data["count"] += 1

        if data["count"] >= TOTAL_CAPTCHAS:
            await update.message.reply_text(
                "✅ All captchas completed!",
                reply_markup=menu_keyboard()
            )
            return

        data["captcha"] = generate_captcha()

        await update.message.reply_text(
            f"""
✅ Correct

Captcha {data['count'] + 1} / {TOTAL_CAPTCHAS}

Type this captcha:

{data['captcha']}
""",
            reply_markup=menu_keyboard()
        )

    else:
        await update.message.reply_text(
            "❌ Wrong captcha. Try again.",
            reply_markup=menu_keyboard()
        )


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...")
app.run_polling()
        

    

    
