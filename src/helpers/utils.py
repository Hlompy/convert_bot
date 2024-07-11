from typing import Callable

from telegram import InlineKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters



KEYBOARD = "current_keyboard"


class ContextManager:
    def set(self, context: ContextTypes.DEFAULT_TYPE, key, value):
        context.user_data[key] = value

    def get(self, context: ContextTypes.DEFAULT_TYPE, key):
        return context.user_data.get(key)
    
    def set_keys(self, context: ContextTypes.DEFAULT_TYPE, keys: InlineKeyboardMarkup):
        context.chat_data[KEYBOARD] = keys
    
    def set_currency(self, context: ContextTypes.DEFAULT_TYPE, currency):
        context.chat_data['currency'] = currency

    def get_currency(self, context: ContextTypes.DEFAULT_TYPE):
        return context.chat_data.get('currency')
    
    def set_final_currency(self, context: ContextTypes.DEFAULT_TYPE, currency):
        context.chat_data['final_currency'] = currency

    def get_final_currency(self, context: ContextTypes.DEFAULT_TYPE):
        return context.chat_data.get('final_currency')
    
    
    def set_result(self, context: ContextTypes.DEFAULT_TYPE, result):
        context.chat_data['result'] = result

    def get_result(self, context: ContextTypes.DEFAULT_TYPE):
        return context.chat_data.get('result')


context_manager = ContextManager()