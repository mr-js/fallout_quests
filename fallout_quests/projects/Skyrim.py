# coding=utf8

# SKYRIM CONFIG BEGIN

name = 'Skyrim'
domain = 'elderscrolls.fandom.com'
protocol =  'https'
pages_level_max = 4
root_path = f'/ru/wiki'
root_page = 'Portal/The_Elder_Scrolls_V:_Skyrim'
root_page_links_block = './/div[@id="portal_content"]'

page_block = '//main[@class="page__main" and @lang="ru"]'
meta_block = '//div[@class="page-header__meta"]'
title_block = '//h1[@class="page-header__title"]'
content_block = '//div[@class="mw-parser-output"]'
summary_block = '//*[@class="linkPreviewText"]'
cut_blocks = '''
//span[@class="mw-editsection"]
//div[contains(@class, "portal_section")]
'''
# cut_blocks = '''
# .//table[@class="va-navbox-border va-navbox-right"]
# .//table[@class="va-navbox-border va-navbox-bottom"]
# .//table[@class="mbox dabhide"]
# .//table[@class="intro"]
# '''

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
The Elder Scrolls Wiki:
Портал:
Участник:
Категория:
static.wikia.nocookie.net
ERROR:root
Файл
'''
links_negatives = '''
Arena
Daggerfall
Morrowind
The Elder Scrolls III
Oblivion
The Elder Scrolls IV
Online
The Elder Scrolls Online
Adventures
Eye of Argonia
Paradise Sugar
Redguard
Blades
Travels
Dawnstar
Shadowkey
Stormhold
Battlespire
Legends
Адский город
'''
links_positives = '''
The Elder Scrolls V
'''
links_patches = [
]

meta_required = '''
Skyrim
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
Arena
Daggerfall
Morrowind
The Elder Scrolls III
Oblivion
The Elder Scrolls IV
Online
The Elder Scrolls Online
Adventures
Eye of Argonia
Paradise Sugar
Redguard
Blades
Travels
Dawnstar
Shadowkey
Stormhold
Battlespire
Legends
Адский город
Construction Set
'''
title_positives = '''
Tribunal
Bloodmoon
'''
title_patches = [
]

summary_required = '''
'''
summary_removed = '''
'''
summary_negatives = '''
Arena
Daggerfall
Oblivion
The Elder Scrolls III
Morrowind
The Elder Scrolls IV
Online
The Elder Scrolls Online
Adventures
Eye of Argonia
Paradise Sugar
Redguard
Blades
Travels
Dawnstar
Shadowkey
Stormhold
Battlespire
Legends
Адский город
Lore
Construction Set
'''
summary_positives = '''
Скайрим
Skyrim
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
(Skyrim)
( )
()
[ ]
[]
'''
main_filter = '''
The Elder Scrolls V Skyrim

Атрибуты (Skyrim)
Навыки (Skyrim)
Камни судьбы (Skyrim)
Классы (Skyrim)
Доспехи (Skyrim)
Оружие (Skyrim)
Заклинания (Skyrim)
Ту%27ум
Вампиризм (Skyrim)
Ликантропия (Skyrim)
Алхимия (Skyrim)
Артефакты (Skyrim)
Предметы (Skyrim)
ID предметов (Skyrim)

Персонажи (Skyrim)
Учителя навыков (Skyrim)
Компаньоны
Карта (Skyrim)
Локации (Skyrim)
Существа (Skyrim)
Дракон (Skyrim)

Главный квест (Skyrim)
Квесты (Skyrim)

Консольные команды (Skyrim)
Управление (Skyrim)
Пасхальные яйца (Skyrim)


'''

# SKYRIM CONFIG END