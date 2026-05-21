from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import random
import string

TOKEN = "YOUR_BOT_TOKEN"

# User data
users = {}

# Generate captcha
def generate_captcha():
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(6))

# Keyboard buttons
buttons = [
    ["Next"],
    ["Withdraw"],
    ["Vault"]
]

reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in users:
        users[user_id] = {
            "balance": 0.0,
            "captcha": ""
        }

    captcha = generate_captcha()
    users[user_id]["captcha"] = captcha

    image_url = f"https://dummyimage.com/400x200/000/fff&text={captcha}"

    await update.message.reply_photo(
        photo=image_url,
        caption="Solve this captcha",
        reply_markup=reply_markup
    )

# Message handler
async def messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.upper()

    if user_id not in users:
        users[user_id] = {
            "balance": 0.0,
            "captcha": ""
        }

    # NEXT button
    if text == "NEXT":
        captcha = generate_captcha()
        users[user_id]["captcha"] = captcha

        image_url = f"https://dummyimage.com/400x200/000/fff&text={captcha}"

        await update.message.reply_photo(
            photo=image_url,
            caption="New captcha"
        )
        return

    # VAULT button
    if text == "VAULT":
        bal = users[user_id]["balance"]

        await update.message.reply_text(
            f"💰 Your Balance: ₹{bal:.2f}"
        )
        return

    # WITHDRAW button
    if text == "WITHDRAW":
        bal = users[user_id]["balance"]

        if bal < 10:
            await update.message.reply_text(
                f"❌ Minimum withdraw is ₹10\n\nCurrent Balance: ₹{bal:.2f}"
            )
        else:
            await update.message.reply_text(
                f"✅ Withdrawal Requested\n\nYour balance: ₹{bal:.2f}"
            )
        return

    # Captcha checking
    correct = users[user_id]["captcha"]

    if text == correct:
        users[user_id]["balance"] += 0.05

        new_balance = users[user_id]["balance"]

        await update.message.reply_text(
            f"✅ Correct\n\n₹0.05 Added\nBalance: ₹{new_balance:.2f}"
        )

        # Auto next captcha
        captcha = generate_captcha()
        users[user_id]["captcha"] = captcha

        image_url = f"https://dummyimage.com/400x200/000/fff&text={captcha}"

        await update.message.reply_photo(
            photo=image_url,
            caption="Next captcha"
        )

    else:
        await update.message.reply_text("❌ Wrong captcha")

# Main
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, messages))

print("Bot running...")
app.run_polling()



        


        

    

    
