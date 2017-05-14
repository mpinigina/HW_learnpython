import re
import flask
import telebot
import conf

WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)


bot = telebot.TeleBot(conf.TOKEN, threaded=False)
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)
app = flask.Flask(__name__)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я умею считать количество слов в твоём сообщении!")


@bot.message_handler(func=lambda m: True)
def send_num_of_words(message):
    splited_text = re.split('\W', message.text)
    splited_text = [word for word in splited_text if word]
    num_of_words = len(splited_text)
    if num_of_words % 100 in range(11, 20):
        endword = 'слов'
    elif num_of_words % 10 in range(2, 5):
        endword = 'слова'
    elif num_of_words % 10 == 1:
        endword = 'слово'
    else:
        endword = 'слов'
    bot.reply_to(message, 'В этом сообщении {0} {1}.'.format(num_of_words, endword))


@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'


@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    flask.abort(403)
