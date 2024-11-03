import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from dotenv import load_dotenv
from mistralai import Mistral

# Load environment variables
load_dotenv()

# Get API keys from environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# Mistral client setup
mistral_client = Mistral(api_key=MISTRAL_API_KEY)
mistral_model = "open-mistral-nemo"


# Command handler for /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hello! I'm a bot powered by Mistral AI. How can I help you today?"
    )


# Message handler for chat
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text

    # Get response from Mistral
    chat_response = mistral_client.chat.complete(
        model=mistral_model,
        messages=[
            {
                "role": "user",
                "content": user_message,
            },
        ],
    )

    ai_response = chat_response.choices[0].message.content

    # Send the response back to the user
    await update.message.reply_text(ai_response)


def main() -> None:
    # Create the Application and pass it your bot's token
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
