# coding=utf8

# Fallout 4 CONFIG BEGIN

name = 'Fallout 4'
domain = 'fallout.fandom.com'
protocol =  'https'
pages_level_max = 3
root_path = f'/ru/wiki'
root_page = '/ru/wiki/Fallout_4'
root_page_links_block = './/table[@class="va-navbox-brick va-navbox-columncont va-navbox-formatlist va-navbox-nowraplinks"]'

page_block = './/main[@class="page__main" and @lang="ru"]'
meta_block = './/div[@class="page-header__meta"]'
title_block = './/h1[@class="page-header__title"]'
content_block = './/div[@class="mw-parser-output"]'
summary_block = './/*[@class="intro-bullets"]'
cut_blocks = '''
//span[@class="mw-editsection"]
.//table[@class="va-navbox-border va-navbox-right"]
.//table[@class="va-navbox-border va-navbox-bottom"]
.//table[@class="mbox dabhide"]
.//table[@class="intro"]
'''

links_required = '''
/ru/wiki
'''
links_removed = '''
?
#
=edit
?diff
?oldid
?action
Шаблон:
Служебная:
Обсуждение:
Обсуждение_шаблона:
Стена обсуждения:
Fallout_Wiki:
Портал:
Участник:
Категория:
static.wikia.nocookie.net
ERROR:root
Файл
'''
links_negatives = '''
Fallout Tactics
Brotherhood of Steel
Fallout Shelter
Fallout 2
Fallout 3
Fallout: New Vegas
Fallout New Vegas
Fallout 76
Fallout Extreme
Fallout Tactics 2
Van Buren
Brotherhood of Steel 2
Project V13
Fallout Online
'''
links_positives = '''
Fallout: 4
Fallout 4
'''
links_patches = [
]

meta_required = '''
Fallout 4
Automatron
Wasteland Workshop
Far Harbor
Contraptions Workshop
Vault-Tec Workshop
Nuka-World
High Resolution Texture Pack
Creation Club
'''
meta_removed = '''
'''
meta_negatives = '''
'''
meta_positives = '''
'''
meta_patches = [
]

title_required = '''
'''
title_removed = '''
'''
title_negatives = '''
Fallout Tactics
Brotherhood of Steel
Fallout Shelter
Fallout 2
Fallout 3
Fallout: New Vegas
Fallout New Vegas
Fallout 76
Fallout Extreme
Fallout Tactics 2
Van Buren
Brotherhood of Steel 2
Project V13
Fallout Online
G.E.C.K.
'''
title_positives = '''
Fallout 4
Automatron
Wasteland Workshop
Far Harbor
Contraptions Workshop
Vault-Tec Workshop
Nuka-World
High Resolution Texture Pack
Creation Club
'''
title_patches = [
]

summary_required = '''
'''
summary_removed = '''
'''
summary_negatives = '''
Fallout Tactics
Brotherhood of Steel
Fallout Shelter
Fallout 2
Fallout 3
Fallout: New Vegas
Fallout New Vegas
Fallout 76
Fallout Extreme
Fallout Tactics 2
Van Buren
Brotherhood of Steel 2
Project V13
Fallout Online
Lore
G.E.C.K.
'''
summary_positives = '''
Fallout 4
Automatron
Wasteland Workshop
Far Harbor
Contraptions Workshop
Vault-Tec Workshop
Nuka-World
High Resolution Texture Pack
Creation Club
нескольких играх серии
игр серии
'''
summary_patches = [
]

content_required = '''
'''
content_removed = '''
'''
content_negatives = '''
'''
content_positives = '''
'''
content_patches = [
]

print_filters = '''
_
Fallout 4
Automatron
Wasteland Workshop
Far Harbor
Contraptions Workshop
Vault-Tec Workshop
Nuka-World
High Resolution Texture Pack
Creation Club
( )
()
[ ]
[]
'''
main_filter = '''
Fallout 4
Fallout_4_SPECIAL
Активаторы Fallout_4
Баги Fallout_4
Боеприпасы Fallout_4
Броня и одежда Fallout_4
Голодиски Fallout_4
Дополнения Fallout_4
Заметки Fallout_4
Квесты Fallout_4
Ключи Fallout_4
Книги Fallout_4
Компьютеры и роботы Fallout_4
Контейнеры Fallout_4
Концовки Fallout_4
Локации Fallout_4
Медпрепараты и еда Fallout_4
Навыки Fallout_4
Напарники Fallout_4
Организации Fallout_4
Оружие Fallout_4
Патчи Fallout_4
Персонажи Fallout_4
Предметы Fallout_4
Пупсы Fallout_4
Радиостанции Fallout_4
Разные предметы Fallout_4
Случайные встречи Fallout_4
Способности Fallout_4
Существа Fallout_4
Терминалы Fallout_4
Титры Fallout_4
Торговцы Fallout_4
'''

# Fallout 4 CONFIG END
