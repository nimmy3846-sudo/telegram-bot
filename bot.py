from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import random
import string

# =========================
# BOT TOKEN
# =========================
TOKEN = "8838766761:AAFhyC2n2ssbwVScY53iN8Pt2MzXCdsCLgM"

# =========================
# SETTINGS
# =========================
TOTAL_CAPTCHAS = 20000000
REWARD_PER_CAPTCHA = 0.05
MIN_WITHDRAW = 10.0

# =========================
# USER DATA
# =========================
users = {}

# =========================
# BUTTONS
# =========================
keyboard = [
    ["Next"],
    ["Vault"],
    ["Withdraw"]
]

reply_markup = ReplyKeyboardMarkup(
    keyboard,
    resize_keyboard=True
)

# =========================
# CAPTCHA GENERATOR
# =========================
def generate_captcha():
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(6))

# =========================
# START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    users[user_id] = {
        "balance": 0.0,
        "count": 0,
        "captcha": generate_captcha()
    }

    text = f"""
🔐 CAPTCHA TASK

Captcha 1 / {TOTAL_CAPTCHAS}

Type this captcha:

{users[user_id]["captcha"]}
"""

    await update.message.reply_text(
        text,
        reply_markup=reply_markup
    )

# =========================
# SEND NEW CAPTCHA
# =========================
async def send_new_captcha(update: Update, user_id):

    users[user_id]["captcha"] = generate_captcha()

    current = users[user_id]["count"] + 1

    text = f"""
🔐 CAPTCHA TASK

Captcha {current} / {TOTAL_CAPTCHAS}

Type this captcha:

{users[user_id]["captcha"]}
"""

    await update.message.reply_text(
        text,
        reply_markup=reply_markup
    )

# =========================
# MESSAGE HANDLER
# =========================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    text = update.message.text

    # User not started
    if user_id not in users:
        await update.message.reply_text(
            "Send /start first"
        )
        return

    # =====================
    # NEXT BUTTON
    # =====================
    if text == "Next":
        await send_new_captcha(update, user_id)
        return

    # =====================
    # VAULT BUTTON
    # =====================
    if text == "Vault":

        bal = users[user_id]["balance"]
        solved = users[user_id]["count"]

        await update.message.reply_text(
            f"""
🏦 YOUR VAULT

💰 Balance: ₹{bal:.2f}

✅ Solved: {solved}
"""
        )
        return

    # =====================
    # WITHDRAW BUTTON
    # =====================
    if text == "Withdraw":

        bal = users[user_id]["balance"]

        if bal < MIN_WITHDRAW:

            need = MIN_WITHDRAW - bal

            await update.message.reply_text(
                f"""
❌ Minimum withdraw is ₹10

You need ₹{need:.2f} more
"""
            )

        else:

            await update.message.reply_text(
                f"""
✅ Withdraw Request Sent

💰 Your Balance: ₹{bal:.2f}
"""
            )

            users[user_id]["balance"] = 0.0

        return

    # =====================
    # CAPTCHA CHECK
    # =====================
    captcha = users[user_id]["captcha"]

    if text.upper() == captcha:

        users[user_id]["balance"] += REWARD_PER_CAPTCHA
        users[user_id]["count"] += 1

        await update.message.reply_text(
            f"""
✅ Correct

💰 +₹{REWARD_PER_CAPTCHA}

Current Balance:
₹{users[user_id]["balance"]:.2f}
"""
        )

        await send_new_captcha(update, user_id)

    else:

        await update.message.reply_text(
            "❌ Wrong Captcha"
        )

# =========================
# MAIN
# =========================
def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    print("Bot Running...")

    app.run_polling()

# =========================
# RUN
# =========================
if __name__ == "__main__":
    main()
