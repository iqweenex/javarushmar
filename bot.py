import time

from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from gpt import *
from util import *

dic = {
    "date_grande": "Ариана Грандэ",
    "date_robbie": "Марго Робби",
    "date_zendaya": "Зендея",
    "date_gosling": "Райан Гослинг",
    "date_hardy": "Том Харди",
}

list_think = ["Обработка запроса.", "Обработка запроса..", "Обработка запроса...", "Обработка запроса...."]


async def start(update, context):
    dialog.mode = "main"
    text = load_message("main")
    await send_photo(update, context, "main")
    await send_text(update, context, text)
    await show_main_menu(update, context, {
        "start": "Запуск",
        "profile": "генерация Tinder-профля ",
        "opener": "сообщение для знакомства",
        "message": "переписка от вашего имени",
        "date": "переписка со звездами",
        "gpt": "Общение с ИИ"
    })


async def gpt(update, context):
    dialog.mode = "gpt"
    text = load_message("gpt")
    await send_photo(update, context, "gpt")
    await send_text(update, context, text)


async def gpt_dialog(update, context):
    text = update.message.text
    prompt = load_prompt("gpt")
    answer = await chatgpt.send_question("Напиши короткий и четкий ответ на следующий запрос: ", text)
    await send_text(update, context, answer)


async def date(update, context):
    dialog.mode = "date"
    text = load_message("date")
    await send_photo(update, context, "date")
    await send_text_buttons(update, context, text, dic)


async def date_dialog(update, context):
    text = update.message.text
    my_message = await send_text(update, context, "Собеседник набирает сообщение...")
    answer = await chatgpt.add_message(text)
    await my_message.edit_text(answer)


async def date_button(update, context):
    query = update.callback_query.data
    await update.callback_query.answer()

    await send_photo(update, context, query)
    await send_html(update, context, f"Пригласи за 5 сообщений {dic[query]}")

    prompt = load_prompt(query)
    chatgpt.set_prompt(prompt)


async def message(update, context):
    dialog.mode = "message"
    text = load_message("message")
    await send_photo(update, context, "message")
    await send_text_buttons(update, context, text, {
        "message_next": "Следующее сообщение",
        "message_date": "Пригласить"
    })
    dialog.list.clear()


async def message_dialog(update, context):
    text = update.message.text
    dialog.list.append(text)


async def message_button(update, context):
    query = update.callback_query.data
    await update.callback_query.answer()

    prompt = load_prompt(query)
    user_chat_history = "\n\n".join(dialog.list)
    my_message = await send_text(update, context, "Обработка запроса")
    for i in range(len(list_think)):
        time.sleep(0.2)
        await my_message.edit_text(list_think[i])
    answer = await chatgpt.send_question(prompt, user_chat_history)
    await my_message.edit_text(answer)


async def hello(update, context):
    if dialog.mode == "gpt":
        await gpt_dialog(update, context)
    if dialog.mode == "date":
        await date_dialog(update, context)
    if dialog.mode == "message":
        await  message_dialog(update, context)
    else:
        await send_text(update, context, "Привет")
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


dialog = Dialog()
dialog.mode = None
dialog.list = []

chatgpt = ChatGptService(
    token="ujavcgkAld/r/7U60nS8WDUhWeWVYkZbhjQYpKBFGTvoj5842ast7Pxc54epaCxHRBWXa4vjUutckFaoaUmyOdt62mPPZjjrSFzHlklUvRxjKkD54HiY1iMRLus7TxOkcmPElgqCRPBocX6wJsuWbUTuGkgPNjhYwE08Bvau9oVOiaBcWnUrI/ewY+ccVqx7dnAN4A7RhT46B8BjZjVtU/H8jZakz1cJir+37f/KOL/cTVnmJo=")

app = ApplicationBuilder().token("7771358337:AAF_6deTgmKK50Be7IG5L7jg2XXqYLpFWhс").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gpt", gpt))
app.add_handler(CommandHandler("date", date))
app.add_handler(CommandHandler("message", message))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))

app.add_handler(CallbackQueryHandler(date_button, pattern="^date_.*"))
app.add_handler(CallbackQueryHandler(message_button, pattern="^message_.*"))
app.add_handler(CallbackQueryHandler(hello_buttons))
app.run_polling()
