# coding=utf8

# Fallout 4 (ENG) CONFIG BEGIN

name = 'Fallout 4 (ENG)'
domain = 'fallout.fandom.com'
protocol =  'https'
pages_level_max = 3
root_path = f'/wiki'
root_page = '/wiki/Fallout_4'
root_page_links_block = './/table[@class="va-navbox-brick va-navbox-columncont va-navbox-formatlist va-navbox-nowraplinks"]'

page_block = './/main[@class="page__main" and @lang="en"]'
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
/wiki
'''
links_removed = '''
?
#
=edit
?diff
?oldid
?action
Template:
Special:
Talk:
Template_talk:
Message_Wall:
Fallout_Wiki:
Portal:
User:
User_talk:
User_blog:
Category:
static.wikia.nocookie.net
ERROR:root
File:
Help:
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
Fallout series
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
Fallout_4_exploits
Fallout_4_bugs
Fallout_4_ammunition
Fallout_4_armor_and_clothing
Fallout_4_armor_mods
Fallout_4_notes
Fallout_4_add-ons
Fallout_4_notes
Fallout_4_quests
Fallout_4_keys
Fallout_4_magazines
Fallout_4_robots_and_computers
Fallout_4_containers_and_storage
Fallout_4_endings
Fallout_4_locations
Fallout_4_consumables
Fallout_4_perks
Fallout_4_primary_statistics
Fallout_4_companions
Fallout_4_factions
Fallout_4_weapons
Fallout_4_weapon_mods
Fallout_4_patches
Fallout_4_characters
Fallout_4_items
Vault-Tec_bobblehead_(Fallout_4)
Fallout_4_radio_stations
Fallout_4_miscellaneous_items
Fallout_4_random_encounters
Fallout_4_perks
Fallout_4_creatures
Fallout_4_merchants
Fallout_4_vehicles
'''

# Fallout 4 (ENG) CONFIG END
