import logging
import string
import sys
from typing import Dict, List

import telebot
from telebot import types

from bigbox import Box
from catalog import Catalog, Item
from recommendation import RecommendationService, UserData

with open('telegram_bot_token.txt', 'r') as file:
    TOKEN = file.read().strip()

bot = telebot.TeleBot(TOKEN)

logger = logging.getLogger("bot")
logging.basicConfig(stream=sys.stdout, level=logging.WARN)

ChatId = string

user_data_context: Dict[ChatId, UserData] = {}
recommendation_service: RecommendationService = None

def get_user_context(chat_id: ChatId) -> UserData:
    user_data = user_data_context.get(chat_id, UserData())
    user_data_context[chat_id] = user_data
    return user_data

# Comando /start para mostrar el menú inicial
@bot.message_handler(commands=['start'])
def send_welcome(message):
    logger.info("Comando start")
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    suggestButton = types.KeyboardButton("👉Sugerir")
    # modifyParameters = types.InlineKeyboardButton("Modificar Parámetros", callback_data="modify_parameters")
    # queryButton = types.KeyboardButton("Consultar")
    # helpButton = types.KeyboardButton("Ayuda")
    markup.add(suggestButton)
    bot.send_message(message.chat.id, "¡Hola! 👋 ¡Bienvenido a NovaRegalos!, gracias por contactarte con nosotros, seré tu asistente para encontrar el regalo perfecto. 🎁", reply_markup=markup)


# Respuesta a cada opción del menú
@bot.message_handler(func=lambda message: True)
def menu_response(message):
    if "Sugerir" in message.text:
        ask_age_range(message)
    else:
        bot.reply_to(message, "Por favor, selecciona una opción válida.")


# # Función para mostrar opciones de modificación de parámetros
# def modify_parameters(message: types.Message):
#     markup = types.InlineKeyboardMarkup()
#     btn1 = types.InlineKeyboardButton("Cantidad de Textos", callback_data="modify_quantity")
#     btn2 = types.InlineKeyboardButton("Número de Caracteres", callback_data="modify_characters")
#     markup.add(btn1, btn2)
#     bot.send_message(message.chat.id, "Elige qué parámetro deseas modificar:", reply_markup=markup)


# Pregunta por el rango de edad
def ask_age_range(message: types.Message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    rango1Button = types.KeyboardButton("👧18-30")
    rango2Button = types.KeyboardButton("🧑30-50")
    rango3Button = types.KeyboardButton("👴50 o más")
    markup.add(rango1Button, rango2Button, rango3Button)
    msg = bot.send_message(message.chat.id, "¡Genial! Contame un poco más sobre ello, 😊 marcá la edad de quien deseas darle este obsequio🌟", reply_markup=markup)
    bot.register_next_step_handler(msg, ask_price_range)

def ask_price_range(message: types.Message):
    user_data = get_user_context(message.chat.id)
    # user_data.age_range = message.text
    user_data.age_range = message.text[1:]

    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    rango1Button = types.KeyboardButton("$10.00 - $15.000")
    rango2Button = types.KeyboardButton("$15.000 - $35.000")
    rango3Button = types.KeyboardButton("$20.0000 - $50.000")
    markup.add(rango1Button, rango2Button, rango3Button)
    msg = bot.send_message(message.chat.id, "¡Perfecto! ¿Decime en qué rango de precio lo deseas?", reply_markup=markup)
    bot.register_next_step_handler(msg, ask_relationship)

def ask_relationship(message: types.Message):
    user_data = get_user_context(message.chat.id)
    user_data.price_range = message.text

    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton("Noviazgo")
    btn2 = types.KeyboardButton("Pariente")
    btn3 = types.KeyboardButton("Laboral")
    btn4 = types.KeyboardButton("Amistad")
    markup.add(btn1, btn2, btn3, btn4)
    msg = bot.send_message(message.chat.id, "Perfecto! ¿A quién le estás buscando un regalo hoy? ✨ seleccioná tu tipo de relación.", reply_markup=markup)
    bot.register_next_step_handler(msg, ask_event_type)

def ask_event_type(message: types.Message):
    get_user_context(message.chat.id).relationship = message.text

    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton("🎂Cumpleaño")
    btn2 = types.KeyboardButton("💐Romantico")
    btn3 = types.KeyboardButton("💍Aniversario")
    btn4 = types.KeyboardButton("💰Incentivo")
    markup.add(btn1, btn2, btn3, btn4)
    msg = bot.send_message(message.chat.id, "¡Qué bonito! 🌿¿Qué acontecimiento te lleva a hacer este regalo hoy? Por Favor seleccioná una opción.", reply_markup=markup)
    bot.register_next_step_handler(msg, ask_interested)


def ask_interested(message: types.Message):
    get_user_context(message.chat.id).event_type = message.text[1:]

    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton("Aventura")
    btn2 = types.KeyboardButton("Entretenimiento")
    btn3 = types.KeyboardButton("Gastronomia")
    btn4 = types.KeyboardButton("Estar bien")
    btn5 = types.KeyboardButton("Relax")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    msg = bot.send_message(message.chat.id, "¿Que tipo de interes tiene?", reply_markup=markup)
    bot.register_next_step_handler(msg, recommend)


def recommend(message: types.Message):
    user_data = get_user_context(message.chat.id)
    user_data.interests = message.text
    recommended_boxes: List[Box] = recommendation_service.recommend(user_data)

    for box in recommended_boxes:
        bot.send_photo(message.chat.id, box.product_image_url, f"🎉 ¡Listo! Basándonos en tus elecciones, te recomendamos: {box.name} - ${box.price}")
        # bot.send_message(message.chat.id, f"Datos guardados: {user_data_context[message.chat.id]}")

    bot.send_poll(message.chat.id, "¿Como recomendarias esta experencia?", ["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐", "⭐"], is_anonymous=False)
    bot.send_message(message.chat.id, f"¿Te gusta la sugerencia? 😊 Si necesitas más opciones, escribime. 🎁")


def main():
    logger.info("Cargando el Catalogo")
    catalog = Catalog()
    catalog.load_catalog()
    global recommendation_service
    recommendation_service = RecommendationService(catalog=catalog)

    logger.info("Iniciando Bot")
    bot.polling()


if __name__ == '__main__':
    main()
