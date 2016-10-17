import re

# получение самой статьи из html-страницы
def get_body(page):
    reg = '<div class="left-column">.*?(<p.*?)<div class="tags">'
    regExp = re.compile(reg, flags=re.DOTALL)
    result = regExp.findall(page)
    if len(result) == 0:
        return ''
    # это рег. выражение находит все тэги
    regTag = re.compile('<.*?>', flags=re.U | re.DOTALL)
    # все скрипты
    regScript = re.compile('<script>.*?</script>', flags=re.U | re.DOTALL)
    # все комментарии
    regComment = re.compile('<!--.*?-->', flags=re.U | re.DOTALL)
    result = regScript.sub('', result[0])
    result = regComment.sub('', result)
    result = regTag.sub('', result)
    return result

# получение автора статьи из html-страницы
def get_author(page):
    reg = '<div class="author">(.*?)</div>'
    regText = re.compile(reg, flags=re.DOTALL)
    result = regText.findall(page)
    if len(result) == 0:
        return ''
    regA = re.compile('</?a.*?>', flags=re.DOTALL)
    result = regA.sub('', result[0])
    result = result.replace('\n', ' ').replace('\t', ' ')
    return result.strip()

# получение заголовка статьи из html-страницы
def get_header(page):
    reg = '<div class="left-column">.*?<h1>(.*?)</h1>'
    regHeader = re.compile(reg, flags=re.DOTALL)
    result = regHeader.findall(page)
    return result[0].strip()

# получение даты создания статьи из html-страницы
def get_created(page):
    reg = '<div class="date sep">(.*?)</div>'
    regHeader = re.compile(reg, flags=re.DOTALL)
    result = regHeader.findall(page)
    return result[0].replace(' ', '')

# получение тематики статьи из html-страницы
def get_topic(page):
    reg = '<div class="category-title">(.*?)</div>'
    regText = re.compile(reg, flags=re.DOTALL)
    result = regText.findall(page)
    if len(result) == 0:
        return ''
    regA = re.compile('</?a.*?>', flags=re.DOTALL)
    result = regA.sub('', result[0])
    return result.strip()

# получение года статьи из html-страницы
def get_year(page):
    created = get_created(page)
    result = created.split('.')[2]
    return result

# получение месяца статьи из html-страницы
def get_month(page):
    created = get_created(page)
    result = created.split('.')[1]
    return result
