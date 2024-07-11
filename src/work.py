import os
import logging
import requests

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
   Application, 
   CommandHandler, 
   ContextTypes, 
   CallbackQueryHandler, 
   ConversationHandler,
   )

from helpers.utils import context_manager

logging.basicConfig(
   format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
   level=logging.INFO,
   filename='main.log',
   filemode='w',
   encoding='UTF-8'
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

API_ENDPOINT = f'http://api.exchangeratesapi.io/v1/latest?access_key={os.getenv("ACCESS_KEY")}'
html_response = requests.get(API_ENDPOINT) 

CHOOSING, CONVERTED, CONFIRMATION, AGAIN = range(4)


async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  keyboard = [
     [
        InlineKeyboardButton("🇷🇺RUB", callback_data='RUB'),
        InlineKeyboardButton("🇹🇷TRY", callback_data='TRY'),
        InlineKeyboardButton("🇺🇸USD", callback_data='USD'),
        InlineKeyboardButton("🇪🇺EUR", callback_data='EUR'),
        InlineKeyboardButton("🇬🇧GBP", callback_data='GBP'),
     ]
  ]
  reply_markup = InlineKeyboardMarkup(keyboard)
  context_manager.set_keys(context, keyboard)
  await update.message.reply_text('Choose from which currency do you want to convert:', reply_markup=reply_markup)
  return CHOOSING

async def getting_final_currency(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
   currency = update.callback_query
   await currency.answer()
   keyboard = [
     [
        InlineKeyboardButton("🇷🇺RUB", callback_data='RUB'),
        InlineKeyboardButton("🇹🇷TRY", callback_data='TRY'),
        InlineKeyboardButton("🇺🇸USD", callback_data='USD'),
        InlineKeyboardButton("🇪🇺EUR", callback_data='EUR'),
        InlineKeyboardButton("🇬🇧GBP", callback_data='GBP'),
      ]
  ]
   reply_markup = InlineKeyboardMarkup(keyboard)
   context_manager.set_currency(context, currency)
   await currency.edit_message_text(text=f'Do you want to convert {currency.data} to: ', reply_markup=reply_markup)
   return CONVERTED



async def convertate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
   final_currency = update.callback_query
   await final_currency.answer()
   currency = context_manager.get_currency(context)
   keyboard = [
      [
         InlineKeyboardButton("Yes✅", callback_data='Yes'),
         InlineKeyboardButton("No❌", callback_data='No'),
      ]
   ]
   reply_markup = InlineKeyboardMarkup(keyboard)
   data = requests.get(API_ENDPOINT)
   currencies = data.json()

   first_number = currencies['rates'][currency.data]
   second_number = currencies['rates'][final_currency.data]
   result = second_number / first_number   
   context_manager.set_result(context, result)
   context_manager.set_currency(context, currency)
   context_manager.set_final_currency(context, final_currency)
   await final_currency.edit_message_text(text=f'Do you want to convert {currency.data} to: {final_currency.data}', reply_markup=reply_markup)
   return CONFIRMATION


async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
   answer = update.callback_query
   currency = context_manager.get_currency(context)
   final_currency = context_manager.get_final_currency(context)
   result = context_manager.get_result(context)
   final_result = round(result, 2)
   if answer.data=='Yes':
      await answer.message.reply_text(text=f'Rate: 1 {currency.data} = {final_result} {final_currency.data}\nBack to Currencies - /start')
   else:
      await answer.edit_message_text(text=f'See you soon!🤚\nBack to Currencies - /start')
   return ConversationHandler.END






TOKEN = os.getenv("TELEGRAM_TOKEN")
def main():
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
       entry_points=[CommandHandler("start", start_callback)],
       states={
          CHOOSING: [CallbackQueryHandler(getting_final_currency)],
          CONVERTED: [CallbackQueryHandler(convertate)],
          CONFIRMATION: [CallbackQueryHandler(confirm)],
       },
       fallbacks=[CommandHandler("start", start_callback)],
    )

    application.add_handler(conv_handler)


    application.run_polling(allowed_updates=Update.ALL_TYPES)





if __name__ == "__main__":
    main()

