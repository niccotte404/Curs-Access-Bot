from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.markdown import text, bold, italic
from aiogram.types import Message, ParseMode, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove,\
    InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import keyboards
import db
import os

bot = Bot(token=os.getenv("token"))
dp = Dispatcher(bot, storage=MemoryStorage())

# При запуске бота принты в консоль
async def on_startup(_):
    print("Bot started OK")
    await db.open_database()
    
    
# FSM для добавления курса
class AddCursFSM(StatesGroup):
    name = State()
    description = State()
    url = State()


# FSM для получения курса
class BoughtCursFSM(StatesGroup):
    curs = State()
    mail = State()

    
# Обработчик команды /start
@dp.message_handler(commands=["start"])
async def answer_for_start(message: Message):
    
    await db.add_user(message)
    msg = text(bold("Добро пожаловать в Gultyaev History\n"), "Если вы являетесь администратором бота, введите команду /moderator, чтобы совершить изменения", sep="\n")
    await bot.send_message(message.from_user.id, msg, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboards.main_menu())
    
    
# Обработчик команды /moderator
@dp.message_handler(commands=["moderator"])
async def answer_to_moderator(message: Message):
    
    await message.delete()
    if await db.check_admin(message):
        msg = text(italic("Проверка на модератора пройдена успешно\n"), bold("Вам доступны следующие команды:"),\
            "/add - добавление курса в базу данных",\
            "/del - удаление курса из базы данных",\
            "/start - возвращает в главное меню", sep="\n"
            )
        await bot.send_message(message.from_user.id, msg, parse_mode=ParseMode.MARKDOWN)
    else:
        msg = text(bold("❗️Вы не обладаете правами администратора❗️"))
        await bot.send_message(message.from_user.id, msg, parse_mode=ParseMode.MARKDOWN)
    

# Обработчик команды /add и запуск FSM *FSM - AddCursFSM*
@dp.message_handler(commands=["add"], state=None)
async def add_curs_FSM_start(message: Message):
    
    if await db.check_admin(message):
        await AddCursFSM.name.set()
        await bot.send_message(message.from_user.id, "Введите название курса", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton("❌ОТМЕНА❌")))
        
        
# Выход из FSM и отмена добавления *FSM - AddCursFSM*
@dp.message_handler(lambda msg: msg.text.startswith("❌ОТМЕНА❌"), state=AddCursFSM)
async def add_curs_cancel(message: Message, state: FSMContext):
    
    if await db.check_admin(message):
        curr_state = await state.get_state()
        if state == None:
            return
        else:
            await state.finish()
            await bot.send_message(message.from_user.id, "Добавление курса отменено", reply_markup=keyboards.main_menu())
            

# Добавление имени курса *Состояние - name*, *FSM - AddCursFSM*
@dp.message_handler(state=AddCursFSM.name)
async def add_curs_set_name(message: Message, state=FSMContext):
    
    if await db.check_admin(message):
        async with state.proxy() as data:
            data["name"] = message.text
        await AddCursFSM.next()
        await bot.send_message(message.from_user.id, "Введите описание курса\n\nНе ленитесь и напишите хорошее описание со всякими ссылочками, иначе пользователям не понравится😉")
        

# Добавление описания курса *Состояние - description*, *FSM - AddCursFSM*
@dp.message_handler(state=AddCursFSM.description)
async def add_curs_set_description(message: Message, state: FSMContext):
    
    if await db.check_admin(message):
        async with state.proxy() as data:
            data["description"] = message.text
        await AddCursFSM.next()
        await bot.send_message(message.from_user.id, "Отправьте ссылку на сайт курса")
        
        
        
@dp.message_handler(state=AddCursFSM.url)
async def add_curs_set_url(message: Message, state: FSMContext):
    
    if await db.check_admin(message):
        async with state.proxy() as data:
            data["url"] = message.text
            await db.add_curs(tuple(data.values()))
        await state.finish()
        await bot.send_message(message.from_user.id, "Курс добавлен🤠", reply_markup=ReplyKeyboardRemove())



# Купленный курс + запуск FSM *FSM - BoughtCursFSM*
@dp.message_handler(lambda msg: msg.text.startswith("Я купил(а) курс, что делать?"), state=None)
async def load_curs_FSM_start(message: Message):
    
    await BoughtCursFSM.curs.set()
    data = await db.load_curses()
    data = "\n".join(data)
    msg = text(bold("Выберите курс, который вы приобрели и введите его название\n"), data, sep="\n")
    await bot.send_message(message.from_user.id, msg, parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton("❌ОТМЕНА❌")))


# Отмена загрузки курса
@dp.message_handler(lambda msg: msg.text.startswith("❌ОТМЕНА❌"), state=BoughtCursFSM)
async def load_curs_cansel(message: Message, state=FSMContext):
    
    if await db.check_admin(message):
        curr_state = await state.get_state()
        if state == None:
            return
        else:
            await state.finish()
            await bot.send_message(message.from_user.id, "ОК", reply_markup=keyboards.main_menu())



@dp.message_handler(state=BoughtCursFSM.curs)
async def load_curs_get_name(message: Message, state: FSMContext):
    
    await BoughtCursFSM.next()
    async with state.proxy() as data:
        data["curs"] = message.text
    await bot.send_message(message.from_user.id, "Введите свою электронную почту, а которую пришло подтверждение о покупке курса")



@dp.message_handler(state=BoughtCursFSM.mail)
async def load_curs_get_mail(message: Message, state: FSMContext):
    
    async with state.proxy() as data:
        data["mail"] = message.text
        # await db.mail_data(tuple(data.values()))
        

    ########### Работаем с этим хэндлером
    # Здесь нужно написать 
    # 1) связь с бд -> связь с почтой
    # 2) Выгрузка данных и их проверка
        
    await state.finish()
    await bot.send_message(message.from_user.id, "Для дальнейших действий нужен доступ к скриптам, отвечающим за:\nРассылку писем о подтверждении оплаты\nГенерацию данных пользователя для доступа к курсу и отсылку данных по почте")



@dp.message_handler(lambda msg: msg.text.startswith("Другие курсы от Александра Гультяева"))
async def other_curses(message: Message):
    
    data = await db.load_curses_for_other()
    for item in data:
        msg = text(bold(f"Курс \"{item[0]}\"\n"), item[1], sep="\n")
        await bot.send_message(message.from_user.id, msg, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(row_width=1)\
            .add(InlineKeyboardButton(text=f"Купить курс \"{item[0]}\"", url=item[2])))
        
        


# Обработчик всего текста, введенного пользователем - общение только через команды или кнопки
@dp.message_handler()
async def chat_only_with_buttons(message: Message):
    
    await bot.send_message(message.from_user.id, "Пожалуйста, общайтесь с ботом через кнопки или команды😉")


# Поллинг
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)