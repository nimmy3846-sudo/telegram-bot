from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import random
import string

TOKEN = "8838766761:AAFhyC2n2ssbwVScY53iN8Pt2MzXCdsCLgM"

users = {}

TOTAL_CAPTCHAS = 20000000

keyboard = [
    ["Next"],
    ["Vault"],
    ["Withdraw"]
]

reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def generate_captcha():
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(6))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    users[user_id] = {
        "balance": 0,
        "count": 0,
        "captcha": generate_captcha()
    }

    text = f"""
🔐 CAPTCHA TASK

Captcha 1 / {TOTAL_CAPTCHAS}

Type this captcha:

{users[user_id]['captcha']}
"""

    await update.message.reply_text(text, reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    msg = update.message.text

    if user_id not in users:
        return

    if msg == "Next":
        users[user_id]["captcha"] = generate_captcha()

        text = f"""
🔐 CAPTCHA TASK

Captcha {users[user_id]['count']+1} / {TOTAL_CAPTCHAS}

Type this captcha:

{users[user_id]['captcha']}
"""

        await update.message.reply_text(text, reply_markup=reply_markup)
        return

    if msg == "Vault":
        bal = users[user_id]["balance"]

        await update.message.reply_text(
            f"💰 Your Balance: ₹{bal:.2f}",
            reply_markup=reply_markup
        )
        return

    if msg == "Withdraw":
        bal = users[user_id]["balance"]

        if bal < 10:
            await update.message.reply_text(
                "❌ Minimum withdraw is ₹10",
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                f"✅ Withdraw Requested\n💸 Amount: ₹{bal:.2f}",
                reply_markup=reply_markup
            )
        return

    if msg.upper() == users[user_id]["captcha"]:
        users[user_id]["balance"] += 0.05
        users[user_id]["count"] += 1

        users[user_id]["captcha"] = generate_captcha()

        text = f"""
✅ Correct

💰 Earned: ₹0.05
🏦 Balance: ₹{users[user_id]['balance']:.2f}

🔐 Next Captcha:
{users[user_id]['captcha']}
"""

        await update.message.reply_text(text, reply_markup=reply_markup)

    else:
        await update.message.reply_text(
            "❌ Wrong captcha",
            reply_markup=reply_markup
        )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot Running...")
app.run_polling()
        


        

    

    
