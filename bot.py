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
    suggestButton = types.KeyboardButton("Sugerir")
    # modifyParameters = types.InlineKeyboardButton("Modificar Parámetros", callback_data="modify_parameters")
    # queryButton = types.KeyboardButton("Consultar")
    # helpButton = types.KeyboardButton("Ayuda")
    markup.add(suggestButton)
    bot.send_message(message.chat.id, "¡Bienvenido! Escoge una opción:", reply_markup=markup)


# Respuesta a cada opción del menú
@bot.message_handler(func=lambda message: True)
def menu_response(message):
    if message.text == "Sugerir":
        ask_age_range(message)
        # image_url1 = "https://media.bigbox.com.ar/1/fit/90/0/ce/1/aHR0cHM6Ly9zdGF0aWMuYmlnYm94LmNvbS5hci91cGxvYWRzL2JveC9waHlzaWNhbC84OTE5NDAwZi1mNzMzLTQ0ZGEtOTMwYi00NWE4NTVmNjJjMmEucG5n"
        # image_url2 = "https://media.bigbox.com.ar/1/fit/90/0/ce/1/aHR0cHM6Ly9zdGF0aWMuYmlnYm94LmNvbS5hci91cGxvYWRzL2JveC9waHlzaWNhbC8wZGFmNzFhZS0xYmEyLTRhMWItODVhOS02N2I4NzEzYTI4NmUucG5n"
        # bot.send_photo(message.chat.id, image_url1, "Tentación")
        # bot.send_photo(message.chat.id, image_url2, "Street Food")
        # bot.send_poll(message.chat.id, "¿Cuál de estos regalos prefieres?", ["Tentación", "Street Food"], is_anonymous=False)
    # elif message.text == "Modificar Parámetros":
    #     modify_parameters(message)
    # elif message.text == "Contacto":
    #     bot.reply_to(message, "Puedes contactarnos en: contacto@miempresa.com")
    else:
        bot.reply_to(message, "Por favor, selecciona una opción válida.")


# Función para mostrar opciones de modificación de parámetros
def modify_parameters(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Cantidad de Textos", callback_data="modify_quantity")
    btn2 = types.InlineKeyboardButton("Número de Caracteres", callback_data="modify_characters")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Elige qué parámetro deseas modificar:", reply_markup=markup)


# Pregunta por el rango de edad
def ask_age_range(message: types.Message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    rango1Button = types.KeyboardButton("18-30")
    rango2Button = types.KeyboardButton("30-50")
    rango3Button = types.KeyboardButton("50 o más")
    markup.add(rango1Button, rango2Button, rango3Button)
    msg = bot.send_message(message.chat.id, "Elige el rango de edad", reply_markup=markup)
    bot.register_next_step_handler(msg, ask_price_range)

def ask_price_range(message: types.Message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    rango1Button = types.KeyboardButton("$10.00 - $15.000")
    rango2Button = types.KeyboardButton("$15.000 - $35.000")
    rango3Button = types.KeyboardButton("$20.0000 - $50.000")
    markup.add(rango1Button, rango2Button, rango3Button)
    msg = bot.send_message(message.chat.id, "Elige el rango de precio", reply_markup=markup)
    bot.register_next_step_handler(msg, ask_relationship)

def ask_relationship(message: types.Message):
    user_data = get_user_context(message.chat.id)
    user_data.age_range = message.text

    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton("Noviazgo")
    btn2 = types.KeyboardButton("Pariente")
    btn3 = types.KeyboardButton("Laboral")
    btn4 = types.KeyboardButton("Amistad")
    markup.add(btn1, btn2, btn3, btn4)
    msg = bot.send_message(message.chat.id, "¿Que relación tenes con la persona?", reply_markup=markup)
    bot.register_next_step_handler(msg, ask_event_type)

def ask_event_type(message: types.Message):
    get_user_context(message.chat.id).relationship = message.text

    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton("Cumpleaños")
    btn2 = types.KeyboardButton("Romantico")
    btn3 = types.KeyboardButton("Aniversario")
    btn4 = types.KeyboardButton("Incentivo")
    markup.add(btn1, btn2, btn3, btn4)
    msg = bot.send_message(message.chat.id, "¿Que relación tenes con la persona?", reply_markup=markup)
    bot.register_next_step_handler(msg, ask_interested)


def ask_interested(message: types.Message):
    get_user_context(message.chat.id).event_type = message.text

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
        bot.send_photo(message.chat.id, box.product_image_url, box.name)
    # bot.send_photo(message.chat.id, image_url1, "Tentación")
    # bot.send_message(message.chat.id, f"Datos guardados: {user_data_context[message.chat.id]}")


# # Maneja la selección de modificación de parámetros
# @bot.callback_query_handler(func=lambda call: call.data in ["modify_quantity", "modify_characters"])
# def handle_callback_query(call):
#     if call.data == "modify_quantity":
#         msg = bot.send_message(call.message.chat.id, "Introduce la cantidad de textos (1-10):")
#         bot.register_next_step_handler(msg, set_quantity)
#     elif call.data == "modify_characters":
#         msg = bot.send_message(call.message.chat.id, "Introduce el número de caracteres por texto (50-500):")
#         bot.register_next_step_handler(msg, set_characters)

# # Función para establecer la cantidad de textos
# def set_quantity(message):
#     global text_quantity
#     try:
#         text_quantity = int(message.text)
#     except ValueError:
#         bot.reply_to(message, "Por favor, introduce un número válido.")
#
# # Función para establecer el número de caracteres por texto
# def set_characters(message):
#     global text_characters
#     try:
#         text_characters = int(message.text)
#     except ValueError:
#         bot.reply_to(message, "Por favor, introduce un número válido.")

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
