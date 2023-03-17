from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    
    rkm = ReplyKeyboardMarkup(resize_keyboard=True)
    boughtCursBtn = KeyboardButton("Я купил(а) курс, что делать?")
    otherCursesBtn = KeyboardButton("Другие курсы от Александра Гультяева")
    rkm.add(boughtCursBtn).add(otherCursesBtn)
    return rkm