import schedule
import time

from telegram import Bot

bot = Bot(token="TOKEN")
_id = 0
text_event = ''


def job():
    bot.send_message(_id, text=f"Напоминаю: {text_event}")


def main(chat_id, data):
    global _id, text_event
    _id = chat_id

    for event in data:
        day_ev = data[event]
        if event == "понедельник":
            for el in day_ev:
                text_event = f"{el[0]} в {str(el[1][0]).rjust(2, '0')}:{str(el[1][1]).rjust(2, '0')}"
                schedule.every().monday.at(f"{str(el[2][0]).ljust(2, '0')}:{str(el[2][1]).ljust(2, '0')}").do(job)
        if event == "вторник":
            for el in day_ev:
                text_event = f"{el[0]} в {str(el[1][0]).rjust(2, '0')}:{str(el[1][1]).rjust(2, '0')}"
                schedule.every().tuesday.at(f"{str(el[2][0]).ljust(2, '0')}:{str(el[2][1]).ljust(2, '0')}").do(job)
        if event == "среда":
            for el in day_ev:
                text_event = f"{el[0]} в {str(el[1][0]).rjust(2, '0')}:{str(el[1][1]).rjust(2, '0')}"
                schedule.every().wednesday.at(f"{str(el[2][0]).ljust(2, '0')}:{str(el[2][1]).ljust(2, '0')}").do(job)
        if event == "четверг":
            for el in day_ev:
                text_event = f"{el[0]} в {str(el[1][0]).rjust(2, '0')}:{str(el[1][1]).rjust(2, '0')}"
                schedule.every().thursday.at(f"{str(el[2][0]).ljust(2, '0')}:{str(el[2][1]).ljust(2, '0')}").do(job)
        if event == "пятница":
            for el in day_ev:
                text_event = f"{el[0]} в {str(el[1][0]).rjust(2, '0')}:{str(el[1][1]).rjust(2, '0')}"
                schedule.every().friday.at(f"{str(el[2][0]).ljust(2, '0')}:{str(el[2][1]).ljust(2, '0')}").do(job)
        if event == "суббота":
            for el in day_ev:
                text_event = f"{el[0]} в {str(el[1][0]).rjust(2, '0')}:{str(el[1][1]).rjust(2, '0')}"
                schedule.every().saturday.at(f"{str(el[2][0]).ljust(2, '0')}:{str(el[2][1]).ljust(2, '0')}").do(job)
        if event == "воскресенье":
            for el in day_ev:
                text_event = f"{el[0]} в {str(el[1][0]).rjust(2, '0')}:{str(el[1][1]).rjust(2, '0')}"
                schedule.every().sunday.at(f"{str(el[2][0]).rjust(2, '0')}:{str(el[2][1]).rjust(2, '0')}").do(job)

    # schedule.every(3).seconds.do(bot.send_message(chat_id, text="book rabotaet"))
    # schedule.every(3).seconds.do(job)
    # schedule.every().sunday.at("12:31").do(job)
    # schedule.every().hour.do(job)
    # schedule.every().day.at("10:30").do(job)
    # schedule.every().monday.do(job)
    # schedule.every().wednesday.at("13:15").do(job)
    # schedule.every().minute.at(":17").do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

