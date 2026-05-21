from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import random
import string

TOKEN = "TOKEN = "8838766761:AAFhyC2n2ssbwVScY53iN8Pt2MzXCdsCLgM"

users = {}

TOTAL_CAPTCHAS = 20000000


def generate_captcha():
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(6))


keyboard = [
    ["Next"],
    ["Vault"],
    ["Withdraw"]
]

reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def send_captcha(update, user_id):
    captcha = generate_captcha()

    users[user_id]["captcha"] = captcha
    users[user_id]["count"] += 1

    image_url = f"https://dummyimage.com/500x250/000/fff&text={captcha}"

    await update.message.reply_photo(
        photo=image_url,
        caption=(
            f"🔐 CAPTCHA TASK\n\n"
            f"Captcha {users[user_id]['count']} / {TOTAL_CAPTCHAS}\n\n"
            f"Solve this captcha"
        ),
        reply_markup=reply_markup
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    users[user_id] = {
        "balance": 0.0,
        "captcha": "",
        "count": 0
    }

    await send_captcha(update, user_id)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.upper()

    if user_id not in users:
        users[user_id] = {
            "balance": 0.0,
            "captcha": "",
            "count": 0
        }

    # NEXT
    if text == "NEXT":
        await send_captcha(update, user_id)
        return

    # VAULT
    if text == "VAULT":
        bal = users[user_id]["balance"]

        await update.message.reply_text(
            f"💰 Your Balance: ₹{bal:.2f}"
        )
        return

    # WITHDRAW
    if text == "WITHDRAW":
        bal = users[user_id]["balance"]

        if bal < 10:
            await update.message.reply_text(
                f"❌ Minimum withdraw is ₹10\n\nCurrent Balance: ₹{bal:.2f}"
            )
        else:
            await update.message.reply_text(
                f"✅ Withdrawal Request Sent\n\nYour Balance: ₹{bal:.2f}"
            )
        return

    # CAPTCHA CHECK
    correct = users[user_id]["captcha"]

    if text == correct:
        users[user_id]["balance"] += 0.05

        await update.message.reply_text(
            f"✅ Correct\n\n"
            f"₹0.05 Added\n"
            f"Balance: ₹{users[user_id]['balance']:.2f}"
        )

        await send_captcha(update, user_id)

    else:
        await update.message.reply_text(
            "❌ Wrong Captcha"
        )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot Running...")
app.run_polling()



        


        

    

    
