import os

def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def ins_plain_meta(text, au, ti, da, topic, url):
    if au == '':
        au = 'Noname'
    text = ('@au %s\n@ti %s\n@da %s\n@topic %s\n@url %s\n%s' %
        (au, ti, da, topic, url, text))
    return text

# добавление строки с описанием статьи в конец файла metadata.csv
def write_meta(path, author, header, created, topic, source, publ_year):
    template = ('%s\t%s\t\t\t%s\t%s\tпублицистика\t\t\t%s\t\tнейтральный\t'+
                'н-возраст\tн-уровень\tобластная\t%s\tТюменская область сегодня'+
                '\t\t%s\tгазета\tРоссия\tТюменская область\tru\n')
    row = template % (path, author, header, created, topic, source, publ_year)
    with open('newspaper/metadata.csv', 'a', encoding='utf-8') as meta:
        meta.write(row)

def write_file(path, body):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(body)
