from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import os

# Dictionary to store the blocked users in memory
blocked_users = set()

# Admin Chat ID (only admin can block/unblock users)
ADMIN_CHAT_ID = 1467729863  # Replace this with your actual admin chat ID

async def start(update: Update, context):
    chat_id = update.effective_chat.id
    if chat_id in blocked_users:
        await update.message.reply_text("You are blocked from using this bot.")
        return

    await update.message.reply_text("Welcome to the bot!")

async def handle_message(update: Update, context):
    chat_id = update.effective_chat.id
    if chat_id in blocked_users:
        await update.message.reply_text("You are blocked from using this bot.")
        return

    await update.message.reply_text("You said: " + update.message.text)

# Command to block users
async def block(update: Update, context):
    chat_id = update.effective_chat.id
    if chat_id != ADMIN_CHAT_ID:
        await update.message.reply_text("You are not authorized to use this command.")
        return

    try:
        user_to_block = int(context.args[0])
        blocked_users.add(user_to_block)
        await update.message.reply_text(f"User {user_to_block} has been blocked.")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /block <user_id>")

# Command to unblock users
async def unblock(update: Update, context):
    chat_id = update.effective_chat.id
    if chat_id != ADMIN_CHAT_ID:
        await update.message.reply_text("You are not authorized to use this command.")
        return

    try:
        user_to_unblock = int(context.args[0])
        blocked_users.discard(user_to_unblock)
        await update.message.reply_text(f"User {user_to_unblock} has been unblocked.")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /unblock <user_id>")

# Command to list blocked users
async def list_blocked(update: Update, context):
    chat_id = update.effective_chat.id
    if chat_id != ADMIN_CHAT_ID:
        await update.message.reply_text("You are not authorized to use this command.")
        return

    if blocked_users:
        await update.message.reply_text(f"Blocked users: {', '.join(map(str, blocked_users))}")
    else:
        await update.message.reply_text("No users are currently blocked.")

def main():
    # Create an ApplicationBuilder with your bot token (replace with your actual token)
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    application = ApplicationBuilder().token(token).build()

    # Command to start the bot
    application.add_handler(CommandHandler("start", start))

    # Handlers for the block and unblock commands (admin only)
    application.add_handler(CommandHandler("block", block))
    application.add_handler(CommandHandler("unblock", unblock))
    application.add_handler(CommandHandler("list_blocked", list_blocked))

    # Handler for all text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start polling to listen to bot events
    application.run_polling()

if __name__ == "__main__":
    main()
