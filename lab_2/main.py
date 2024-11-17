import os
import io
import numpy as np
import requests
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
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from PyPDF2 import PdfReader

import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get API keys from environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
FAISS_SERVICE_URL = os.getenv("FAISS_SERVICE_URL", "http://faiss_db:5000")

# Mistral client setup
mistral_client = Mistral(api_key=MISTRAL_API_KEY)
mistral_model = "open-mistral-nemo"

# Embedding model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Text splitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hello! I'm a bot powered by Mistral AI and FAISS. You can send me documents to add to my knowledge base, or ask me questions."
    )


async def add_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.document:
        try:
            file = await context.bot.get_file(update.message.document.file_id)
            file_bytes = await file.download_as_bytearray()

            if update.message.document.file_name.endswith(".pdf"):
                pdf_reader = PdfReader(io.BytesIO(file_bytes))
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
            else:
                text = file_bytes.decode("utf-8")

            chunks = text_splitter.split_text(text)
            for chunk in chunks:
                vector = embeddings.embed_query(chunk)
                response = requests.post(
                    f"{FAISS_SERVICE_URL}/add", json={"vector": vector, "text": chunk}
                )
                response.raise_for_status()

            # Save the updated index
            requests.post(f"{FAISS_SERVICE_URL}/save").raise_for_status()

            await update.message.reply_text("Document added to the knowledge base.")
        except Exception as e:
            logger.error(f"Error adding document: {str(e)}")
            await update.message.reply_text(
                "An error occurred while adding the document."
            )
    else:
        await update.message.reply_text("Please send a document file.")


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text

    try:
        # FAISS retrieval
        query_vector = embeddings.embed_query(user_message)
        response = requests.post(
            f"{FAISS_SERVICE_URL}/search", json={"vector": query_vector, "k": 3}
        )
        response.raise_for_status()

        search_results = response.json()["results"]

        if not search_results:
            await update.message.reply_text(
                "I don't have enough information to answer that question."
            )
            return

        context_text = ""
        for result in search_results:
            context_text += f"Context {result['index']} (distance: {result['distance']}): {result['text']}\\n\\n"

        # Get response from Mistral
        chat_response = mistral_client.chat.complete(
            model=mistral_model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Use the provided context to answer the user's question.",
                },
                {
                    "role": "user",
                    "content": f"Context: {context_text}\\n\\nQuestion: {user_message}",
                },
            ],
        )

        ai_response = chat_response.choices[0].message.content

        # Send the response back to the user
        await update.message.reply_text(ai_response)
    except Exception as e:
        logger.error(f"Error in chat function: {str(e)}")
        await update.message.reply_text(
            "An error occurred while processing your request."
        )


def main() -> None:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Document.ALL, add_document))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    # Load the saved index when starting the application
    try:
        response = requests.post(f"{FAISS_SERVICE_URL}/load")
        response.raise_for_status()
        logger.info("Index loaded or initialized")
    except Exception as e:
        logger.error(f"Error loading index: {str(e)}")

    main()
