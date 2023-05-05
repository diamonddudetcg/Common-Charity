from typing import List
from card import Card
import constants
from io import TextIOWrapper

site = "index.html"
header = "siteutils/header.txt"
footer = "siteutils/footer.txt"
table_start = "siteutils/table_start.txt"
table_end = "siteutils/table_end.txt"
table_entry = "siteutils/table_entry.txt"

cardUrl = "https://db.ygoprodeck.com/card/?search=%s"


def generateSite(cards: List[Card], diff: List[int]):
	outfile = open(site, "w", encoding="utf-8")
	writeHeader(outfile)
	writeAllCards(cards, diff, outfile)
	writeFooter(outfile)
    

def writeHeader(outfile: TextIOWrapper):
	headerText = open(header).read()
	outfile.write(headerText)

def writeFooter(outfile:TextIOWrapper):
	footerText = open(footer).read()
	outfile.write(footerText)


def writeAllCards(cards:List[Card], diff:List[int], outfile: TextIOWrapper):
	for status in [-1, 0, 1, 2]:
		section = [card for card in cards if card.status == status]
		writeSection(section, diff, outfile)
	
	unlim = [card for card in cards if card.status == 3 and card.id in diff]
	if len(unlim) > 0:
		writeSection(unlim, diff, outfile)


def writeSection(cards:List[Card], diff:List[int], outfile:TextIOWrapper):
	outfile.write(open(table_start).read())

	for section in [0, constants.CARD_TYPE_NORMAL_MONSTER, constants.CARD_TYPE_EFFECT_MONSTER, constants.CARD_TYPE_RITUAL_MONSTER,constants.CARD_TYPE_FUSION_MONSTER, constants.CARD_TYPE_LINK_MONSTER, constants.CARD_TYPE_SYNCHRO_MONSTER, constants.CARD_TYPE_XYZ_MONSTER, constants.CARD_TYPE_SPELL,constants.CARD_TYPE_TRAP]:
		subsection = [card for card in cards if card.type == section]
		writeSubSection(subsection, diff, outfile)

	outfile.write(open(table_end).read())

def writeSubSection(cards:List[Card], diff:List[int], outfile:TextIOWrapper):
	for card in sorted(cards, key=lambda x: x.name.lower()):
		writeCard(card, diff, outfile)

def writeCard(card:Card, diff:List[int], outfile:TextIOWrapper):
	entry = open(table_entry).read()
	type = card.type
	name = card.name
	status = card.status
	id = str(card.id)
	while(len(id)<8):
		id = "0%s"%id
	css_class = getCssClassFromType(type)
	type_label = getLabelFromType(type)
	name_label = name.upper()
	status_label = getLabelFromStatus(status)

	entry = entry.replace("&css_class&", css_class).replace("&card_type&", type_label).replace("&card_name&", name_label).replace("&card_status&", status_label).replace("&card_id&", id)
	if card.id in diff:
		entry = entry.replace("&new&", "NEW")
	else:
		entry = entry.replace("&new&", "")
	outfile.write(entry)

def getCssClassFromType(type:int):
	if type == constants.CARD_TYPE_NORMAL_MONSTER:
		return "cardlist_monster"
	if type == constants.CARD_TYPE_EFFECT_MONSTER:
		return "cardlist_effect"
	if type == constants.CARD_TYPE_FUSION_MONSTER:
		return "cardlist_fusion"
	if type == constants.CARD_TYPE_RITUAL_MONSTER:
		return "cardlist_ritual"
	if type == constants.CARD_TYPE_LINK_MONSTER:
		return "cardlist_link"
	if type == constants.CARD_TYPE_XYZ_MONSTER:
		return "cardlist_xyz"
	if type == constants.CARD_TYPE_SYNCHRO_MONSTER:
		return "cardlist_synchro"
	if type == constants.CARD_TYPE_SPELL:
		return "cardlist_spell"
	if type == constants.CARD_TYPE_TRAP:
		return "cardlist_trap"
	return "cardlist"
	
def getLabelFromType(type:int):
	if type == constants.CARD_TYPE_NORMAL_MONSTER:
		return "Monster"
	if type == constants.CARD_TYPE_EFFECT_MONSTER:
		return "Monster / Effect"
	if type == constants.CARD_TYPE_FUSION_MONSTER:
		return "Monster / Fusion"
	if type == constants.CARD_TYPE_RITUAL_MONSTER:
		return "Monster / Ritual"
	if type == constants.CARD_TYPE_LINK_MONSTER:
		return "Monster / Link"
	if type == constants.CARD_TYPE_SYNCHRO_MONSTER:
		return "Monster / Synchro"
	if type == constants.CARD_TYPE_XYZ_MONSTER:
		return "Monster / Xyz"
	if type == constants.CARD_TYPE_SPELL:
		return "Spell"
	if type == constants.CARD_TYPE_TRAP:
		return "Trap"
	return "other"

def getLabelFromStatus(status:int):
	if status == -1:
		return "Illegal"
	if status == 0:
		return "Forbidden"
	if status == 1:
		return "Limited"
	if status == 2:
		return "Semi-Limited"
	return "Unlimited"