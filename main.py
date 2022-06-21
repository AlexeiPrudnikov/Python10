from telegram import Update, Bot
from random import randint

minStep = 1
maxStep = 28
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
file = open('token', 'r', encoding='utf-8')
token = file.readline()
file.close()
bot = Bot(token)
updater = Updater(token, use_context=True)
dispatcher = updater.dispatcher

def StepBot(allCandies):
    candies = allCandies % (maxStep + 1)
    if candies == 0: return randint(minStep, maxStep)
    return candies

def start(update, context):
    global allCandies
    allCandies = 2021
    mess = f'Играем в конфеты, осталось {allCandies} конфет.\n'
    mess += f'Взять за ход можно от {minStep} до {maxStep} конфет.\n'
    context.bot.send_message(update.effective_chat.id, mess)


def info(update, context):
    infoText = f'/start - начало новой игры \n'
    infoText += f'Выигрывает тот, кто взял последнюю конфету'
    context.bot.send_message(update.effective_chat.id, infoText)


def message(update, context):
    global allCandies
    text = update.message.text
    step = int(text)
    if allCandies == 0:
        infoText = f'Игра закончена, /start для начала новой игры'
        context.bot.send_message(update.effective_chat.id, infoText)
        return
    if (step < minStep) or (step > maxStep) or (step > allCandies):
        answer = f'{step} конфет взять невозможно! Повторите ввод.\n'
        answer += f'Осталось {allCandies} конфет.\n'
        context.bot.send_message(update.effective_chat.id, answer)
    else:
        allCandies -= int(text)
        answer = f'Осталось {allCandies} конфет.\n'
        if allCandies == 0:
            answer += 'Браво, Вы победили!!! \n'
            answer += '/start для повторения игры. \n'
        else:
            answer += 'Ходит бот \n'
            botStep = StepBot(allCandies)
            allCandies -= botStep
            answer += f'Бот взял {botStep} конфет \n'
            answer += f'Осталось {allCandies} конфет.\n'
            if allCandies == 0:
                answer += 'Увы, Вы проиграли \n'
                answer += '/start для повторения игры. \n'
        context.bot.send_message(update.effective_chat.id, answer)

def unknown(update, context):
    context.bot.send_message(update.effective_chat.id, 'Ты несешь какую-то дичь...')

start_handler = CommandHandler('start', start)
info_handler = CommandHandler('info', info)
message_handler = MessageHandler(Filters.text, message)
unknown_handler = MessageHandler(Filters.command, unknown)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(info_handler)
dispatcher.add_handler(unknown_handler)
dispatcher.add_handler(message_handler)


updater.start_polling()
updater.idle()

