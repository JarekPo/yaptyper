import random
from datetime import datetime


def generate_random_color():
    chat_text_colors = [
        "#003366",
        "#990000",
        "#5B2E91",
        "#0033CC",
        "#4B3D28",
        "#007A7A",
        "#CC6600",
        "#FF1493",
        "#6B8E23",
        "#2F4F4F",
        "#4B0082",
        "#A52A2A",
    ]
    return random.choice(chat_text_colors)

def get_message_color(message):
    if message.message_time is not None:
        if message.message_time.date() == datetime.now().date():
            return "#000000"
    return "#A9A9A9"

def get_message_time(message):
    if message.message_time is not None:
        return message.message_time.strftime("%Y-%m-%d %H:%M")
    return None
