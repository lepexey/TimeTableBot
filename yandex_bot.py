import logging
import threading

from telegram import Bot, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters

import book

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

button_help = "Помощь"
days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье", "понедельник", "вторник",
        "среда", "четверг", "пятница", "суббота", "воскресенье"]
exceptions = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16',
              '17', '18', '19', '20', '21', '22', '23']
chat_id = None
data = []


def start(update, context):
    global chat_id

    my_thread = threading.Thread(target=book.main, args=(chat_id,))
    my_thread.start()

    update.message.reply_text("Для создания нового события напишите /new <название>")


def get_help(update, context):
    update.message.reply_text(
        "Команды: "
        "\n '/new <название' - создание нового события "
        "\n '/timetable' - для просмотра расписания")


def new(update, context):
    reply_markup = ReplyKeyboardMarkup(
        [
            [
                KeyboardButton(text="Понедельник"),
                KeyboardButton(text="Вторник"),
                KeyboardButton(text="Среда"),
                KeyboardButton(text="Четверг"),
                KeyboardButton(text="Пятница"),
                KeyboardButton(text="Суббота"),
                KeyboardButton(text="Воскресенье")
            ],
        ],
        resize_keyboard=True
    )
    if context.args is not None:
        data.append(context.args[0])
        update.message.reply_text(
            "Введите день недели", reply_markup=reply_markup)
    else:
        update.message.reply_text(
            "Неправильный формат. Введите еще раз пожалуйста", reply_markup=ReplyKeyboardRemove())

    return 1


def first_response(update, context, flag=True):
    # Это ответ на первый вопрос.
    # Мы можем использовать его во втором вопросе.
    if update.message.text in days:
        data.append(update.message.text.lower())
    elif flag:
        return new(update=update, context=context)
    else:
        update.message.reply_text(
            "Неправильный формат. Введите время в формате чч:мм")
        return 2
    update.message.reply_text(
        "Введите время в формате чч:мм", reply_markup=ReplyKeyboardRemove())
    return 2


def second_response(update, context):
    time = update.message.text
    if len(time) != 5 or time[2] != ':':
        return first_response(update=update, context=context, flag=False)
    if time[:2] in exceptions:
        h = exceptions.index(time[:2])
    else:
        return first_response(update=update, context=context, flag=False)
    print(time[:2])
    m = -1
    if time[3:][0] == '0':
        m = exceptions.index(time[3:])
    else:
        m = int(time[3:])

    if h < 0 or h > 23 or m < 0 or m > 59:
        return first_response(update=update, context=context, flag=True)
    else:
        data.append((h, m))

        reply_markup = ReplyKeyboardMarkup(
            [
                [
                    KeyboardButton(text="2 часа"),
                    KeyboardButton(text="1 час"),
                    KeyboardButton(text="40 минут"),
                    KeyboardButton(text="20 минут"),
                    KeyboardButton(text="10 минут"),
                    KeyboardButton(text="5 минут"),
                ],
            ],
            resize_keyboard=True
        )
    update.message.reply_text("Выберите за сколько времени до события вам напомнить", reply_markup=reply_markup)
    return 3


def third_response(update, context):
    h, m = data[2][0], data[2][1]
    if update.message.text == "2 часа":
        if h < 2:
            h = 24 + h - 2
        else:
            h -= 2
    elif update.message.text == "1 час":
        if h == 0:
            h = 23
        else:
            h -= 1
    elif update.message.text == "40 минут":
        if m >= 40:
            m -= 40
        else:
            m = 60 + m - 40
            h -= 1
    elif update.message.text == "20 минут":
        if m >= 20:
            m -= 20
        else:
            m = 60 + m - 20
            h -= 1
    elif update.message.text == "10 минут":
        if m >= 10:
            m -= 10
        else:
            m = 60 + m - 10
            h -= 1
    elif update.message.text == "5 минут":
        if m >= 5:
            m -= 5
        else:
            m = 60 + m - 5
            h -= 1

    reply_markup = ReplyKeyboardMarkup(
        [
            [
                KeyboardButton(text="/timetable"),
                KeyboardButton(text="/help")
            ],
        ],
        resize_keyboard=True
    )

    update.message.reply_text("Событие создано!", reply_markup=reply_markup)
    print(data[0], data[1], data[2], data, sep="\n")
    if data[1] in context.user_data:
        context.user_data[data[1]].append((data[0], data[2], (h, m)))
    else:
        context.user_data[data[1]] = [(data[0], data[2], (h, m))]

    if data[1] in book.data:
        book.data[data[1]].append((data[0], data[2], (h, m)))
    else:
        book.data[data[1]] = [(data[0], data[2], (h, m))]

    chat_id = update.message.chat_id
    data.clear()

    # book.main(chat_id, context.user_data)

    return ConversationHandler.END


def timetable(update, context):
    print(context.user_data)
    out = 'Понедельник:'
    if "понедельник" in context.user_data:
        for event in context.user_data["понедельник"]:
            out += f'\n    @ {event[0]} в {str(event[1][0]).rjust(2, "0")}:{str(event[1][1]).rjust(2, "0")}'
    out += '\nВторник:'
    if "вторник" in context.user_data:
        for event in context.user_data["вторник"]:
            print('vt')
            out += f'\n    @ {event[0]} в {str(event[1][0]).rjust(2, "0")}:{str(event[1][1]).rjust(2, "0")}'
    out += '\nСреда:'
    if "среда" in context.user_data:
        for event in context.user_data["среда"]:
            out += f'\n    @ {event[0]} в {str(event[1][0]).rjust(2, "0")}:{str(event[1][1]).rjust(2, "0")}'
    out += '\nЧетверг:'
    if "четверг" in context.user_data:
        for event in context.user_data["четверг"]:
            out += f'\n    @ {event[0]} в {str(event[1][0]).rjust(2, "0")}:{str(event[1][1]).rjust(2, "0")}'
    out += '\nПятница:'
    if "пятница" in context.user_data:
        for event in context.user_data["пятница"]:
            out += f'\n    @ {event[0]} в {str(event[1][0]).rjust(2, "0")}:{str(event[1][1]).rjust(2, "0")}'
    out += '\nСуббота:'
    if "суббота" in context.user_data:
        for event in context.user_data["суббота"]:
            out += f'\n    @ {event[0]} в {str(event[1][0]).rjust(2, "0")}:{str(event[1][1]).rjust(2, "0")}'
    out += '\nВоскресенье:'
    if "воскресенье" in context.user_data:
        for event in context.user_data["воскресенье"]:
            out += f'\n    @ {event[0]} в {str(event[1][0]).rjust(2, "0")}:{str(event[1][1]).rjust(2, "0")}'

    update.message.reply_text(out)


def stop(update, context):
    pass


def get_chat_id():
    return chat_id


updater = Updater("1779607359:AAHK7ecuquIM_tnEkOlXlJDNwlw8kOb0_bI")
bot = Bot(token="1779607359:AAHK7ecuquIM_tnEkOlXlJDNwlw8kOb0_bI")

dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("help", get_help))
dispatcher.add_handler(CommandHandler("start", start))

dispatcher.add_handler(CommandHandler("timetable", timetable))

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('new', new)],

    states={
        1: [MessageHandler(Filters.text, first_response, pass_user_data=True)],

        2: [MessageHandler(Filters.text, second_response, pass_user_data=True)],

        3: [MessageHandler(Filters.text, third_response, pass_user_data=True)]
    },

    fallbacks=[CommandHandler('stop', stop)]
)
dispatcher.add_handler(conv_handler)

updater.start_polling()
updater.idle()
