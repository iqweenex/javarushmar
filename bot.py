from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from gpt import *
from util import *

async def start(update, context):
    text = load_message("main")
    await send_photo(update, context, "main")
    await send_text(update, context, text)

# тут будем писать наш код :)
async def hello(update, context):
    await send_text(update, context, "Привет")
    await send_text(update, context, "Как дела?")
    await send_text(update, context, "Вы написали " + update.message.text)

    await send_photo(update, context, "gpt")
    await send_text_buttons(update, context, "Запустить что-то", {
        "start": "Запуск",
        "stop": "Стоп"
    })

async def hello_buttons(update, context):
    query = update.callback_query.data
    if query == "start":
        await send_text(update, context, "Запущено")
    else:
        await send_text(update, context, "Остановлено")

app = ApplicationBuilder().token("7771358337:AAF_6deTgmKK50Be7IG5L7jg2XXqYLpFWhc").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CallbackQueryHandler(hello_buttons))
app.run_polling()
