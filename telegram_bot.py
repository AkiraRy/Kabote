import io
import os
import base64
import random

import requests
import telegram.constants
from telegram import Update, InputFile
from telegram.constants import ChatAction, ParseMode
from telegram.ext import (Application,
                          CommandHandler,
                          MessageHandler,
                          filters,
                          ContextTypes,
                          Defaults,
                          ApplicationHandlerStop,
                          TypeHandler,
                          )
from dotenv import load_dotenv
from render_text import render
from test import  create_deck
load_dotenv()
TOKEN = os.getenv("TG_TOKEN")

def gen_num(start, end):
    return random.randint(start, end)

class MyBot:
    def __init__(self):
        # env values
        self.BOT_USERNAME = os.getenv("BOT_NAME")
        self.NICKNAME = os.getenv('BOT_NICKNAME')
        self.CREATOR_ID = int(os.getenv('CREATOR_ID'))
        self.CREATOR_USERNAME = os.getenv('CREATOR_USERNAME')
        self.deck =None


    async def whitelist_user(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_chat.id != self.CREATOR_ID or update.message.chat.type != 'private':
            await update.effective_message.reply_text('Be patient. This AI bot is not available for anyone')
            raise ApplicationHandlerStop


    async def draw_card(self):
        number = gen_num(0, self.deck["cards"]["length"])
        my_card = await self.deck["cards"]["get"](number)
        return my_card


    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.deck = await create_deck()
        await update.message.reply_text(':smile:')
        print(f'user ({update.message.chat.id}) in {update.message.chat.type}: "{update.message.text}')

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('help')

    async def handle_response(self):
        return "Hello"


    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
        card_info = await self.draw_card()
        print(card_info)
        img = render(card_info["question"])

        answers = ','.join(card_info["answer"])
        # print(answers)
        meaning = card_info["meaning"]
        # print(meaning)
        text = f"Correct Answers: {answers}\nMeaning: {meaning}"
        await context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=img, caption=text)


    # Errors
    async def error(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(f'error {context.error} from {update}')




def start_bot(TOKEN: str):

    bot = MyBot()
    defaults = Defaults(parse_mode=ParseMode.HTML)

    app = (
        Application.builder()
        .token(TOKEN)
        .defaults(defaults)
        .build()
    )
    filter_users = TypeHandler(Update, bot.whitelist_user)
    app.add_handler(filter_users, -1)

    # Commands
    app.add_handler(CommandHandler('start', bot.start_command))
    app.add_handler(CommandHandler('help', bot.help_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, bot.handle_message))

    # Error
    app.add_error_handler(bot.error)

    app.run_polling(drop_pending_updates=True)


def main() -> None:

    start_bot(TOKEN)


if __name__ == '__main__':
    main()
