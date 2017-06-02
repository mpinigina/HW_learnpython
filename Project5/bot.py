import os
import re
import random
from pymorphy2 import MorphAnalyzer

morph = MorphAnalyzer()


inquiry = "Введите фразу('выход' чтобы прекратить): "

exit_phrase = "выход" 


def load_data(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding='utf-8') as file_handler:
        return file_handler.read()


def get_words(text):
    return re.findall(r"\w+", text.lower())


def search_for_same_POS(list_of_words, tags):
    for word in list_of_words:
        if tags.gender is not None:
            if morph.parse(word)[0].tag.POS == tags.POS and morph.parse(word)[0].tag.gender == tags.gender:
                rnd = random.random()
                if rnd > 0.9:
                    return word
                else:
                    continue
        else:
            if morph.parse(word)[0].tag.POS == tags.POS:
                rnd = random.random()
                if rnd > 0.9:
                    return word
                else:
                    continue


def apply_inflect(new_word, tags):
    grammems = set()
    if tags.tense is not None:
        grammems.add(tags.tense)
    if tags.number is not None:
        grammems.add(tags.number)
    if tags.case is not None:
        grammems.add(tags.case)
    if tags.person is not None:
        grammems.add(tags.person)
    if tags.aspect is not None:
        grammems.add(tags.aspect)
    try:
        return morph.parse(new_word)[0].inflect(grammems).word
    except AttributeError:
        return new_word


def run_bot(list_of_words):
    while True:
        answer = input(inquiry)
        if answer == exit_phrase:
            break
        else:
            bot_answer = "Бот отвечает: "
            for word in answer.split(" "):
                punctuation = ""
                if word[-1] in "!@#$%^&()?/,":
                    punctuation = word[-1]
                    word = word[0:-1]
                word_tags = morph.parse(word)[0].tag
                new_word = search_for_same_POS(list_of_words, word_tags)
                bot_answer += apply_inflect(new_word, word_tags)
                bot_answer += punctuation
                bot_answer += " "
            print(bot_answer)


if __name__ == '__main__':
    list_of_words = get_words(load_data("example.txt"))
    run_bot(list_of_words)
