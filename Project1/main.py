import news_links
import files_os

# перед началом работы надо удалить папку newspaper
files_os.create_dir('newspaper')
with open('newspaper/metadata.csv', 'w', encoding='utf-8') as meta:
    meta.write('path\tauthor\tsex\tbirthday\theader\tcreated\tsphere\tgenre_fi\ttype\ttopic\tchronotop\tstyle\taudience_age\taudience_level\taudience_size\tsource\tpublication\tpublisher\tpubl_year\tmedium\tcountry\tregion\tlanguage\n')

# вызов функции из файла news_links
news_links.mark_all_news()
