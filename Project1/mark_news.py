import os
import html
# подключение файлов
import news_parser
import news_links
import files_os

# открывает mystem.exe и размечает текст в формате xml
# в аргументах передаются пути к неразмеченному тексту (inp)
# и к размеченному xml (outp)
def mystem_xml(inp, outp):
    os.system('mystem.exe -idn --format xml %s %s' % (inp, outp))

# открывает mystem.exe и размечает текст в формате plain-text
# в аргументах передаются пути к неразмеченному тексту (inp)
# и к размеченному plain-text (outp)
def mystem_plain(inp, outp):
    os.system('mystem.exe -idn %s %s' % (inp, outp))

def mark_page(link, file_id):
    source = 'http://tumentoday.ru' + link
    # скачивание html-страницы статьи
    page = news_links.download_page(source)
    # замена спецсимволов
    page = html.unescape(page)
    
    author = news_parser.get_author(page)
    header = news_parser.get_header(page)
    created = news_parser.get_created(page)
    topic = news_parser.get_topic(page)
    year = news_parser.get_year(page)
    month = news_parser.get_month(page)

    # директория файла с неразмеченным текстом
    plain_dir = 'plain/%s/%s' % (year, month)
    # название файла
    filename = 'article%d' % (file_id)
    # директория + название файла с расширением
    plain_path = '%s/%s.txt' % (plain_dir, filename)
    files_os.create_dir('newspaper/' + plain_dir)
    files_os.write_meta(plain_path, author, header, created, topic,
                        source, year)

    plain_body = news_parser.get_body(page)
    # запись файла с неразмеченным текстом без метаданных
    files_os.write_file('newspaper/' + plain_path, plain_body)
    # директория файла в формате mystem-xml
    m_xml_dir = 'newspaper/mystem-xml/%s/%s' % (year, month)
    files_os.create_dir(m_xml_dir)
    # директория + название файла с расширением
    m_xml_path = '%s/%s.xml' % (m_xml_dir, filename)
    # создание размеченного файла в формате xml
    mystem_xml('newspaper/' + plain_path, m_xml_path)

    # директория файла в формате mystem-plain
    m_plain_dir = 'newspaper/mystem-plain/%s/%s' % (year, month)
    files_os.create_dir(m_plain_dir)
    # директория + название файла с расширением
    m_plain_path = '%s/%s.txt' % (m_plain_dir, filename)
    # создание размеченного файла в формате plain
    mystem_plain('newspaper/' + plain_path, m_plain_path)
    # неразмеченный текст с метаданными
    meta_plain_body = files_os.ins_plain_meta(plain_body, author,
                            header, created, topic, source)
    # запись файла с неразмеченным текстом с метаданными
    files_os.write_file('newspaper/' + plain_path, meta_plain_body)
    # выводит номер статьи и url
    print('%d. %s' % (file_id, source))
