from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8838766761:AAGk4quvFD3qRzlZBQ3HxR-3qtFLuZt0nVs"
ADMIN_ID = 1282253529

tasks = [
    {
        "image": "https://dummyimage.com/300x100/000/fff&text=AB12",
        "answer": "AB12"
    },
    {
        "image": "https://dummyimage.com/300x100/000/fff&text=K9LM",
        "answer": "K9LM"
    }
]

users = {}
stats = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    users[user_id] = 0

    if user_id not in stats:
        stats[user_id] = 0

    await send_task(update)

async def send_task(update):
    user_id = update.effective_user.id
    index = users[user_id]

    if index >= len(tasks):
        await update.message.reply_text("✅ All tasks completed")
        return

    task = tasks[index]

    await update.message.reply_photo(
        photo=task["image"],
        caption="Type the text shown in the image"
    )

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in users:
        await update.message.reply_text("Send /start first")
        return

    index = users[user_id]

    if index >= len(tasks):
        return

    answer = tasks[index]["answer"]

    if update.message.text.upper() == answer:
        users[user_id] += 1
        stats[user_id] += 1

        await update.message.reply_text("✅ Correct")

        await send_task(update)

    else:
        await update.message.reply_text("❌ Wrong")

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Access denied")
        return

    total_users = len(stats)

    text = f"👥 Total Users: {total_users}\n\n"

    for uid, solved in stats.items():
        text += f"ID: {uid} | Solved: {solved}\n"

    await update.message.reply_text(text)

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

print("Bot Running...")

app.run_polling()
