import urllib.request as requests
import json
from typing import List
from card import Card
from datetime import datetime
import constants

header= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
			'AppleWebKit/537.11 (KHTML, like Gecko) '
			'Chrome/23.0.1271.64 Safari/537.11',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
			'Accept-Encoding': 'none',
			'Accept-Language': 'en-US,en;q=0.8',
			'Connection': 'keep-alive'}

common_banlists_url = "https://api.ygoprog.com/api/banlist/common"
banlist_url = "https://api.ygoprog.com/api/banlist/public/%s"
cards_url = "https://api.ygoprog.com/api/cards"
printings_url = "https://api.ygoprog.com/api/cards/printings"
banlist_label = "Tcg"
lflist_file = "docs/lflist/common_charity.lflist.conf"

def generateCardList():
	print("Getting common banlists...", flush=True)
	request = requests.Request(common_banlists_url, None, header)
	with requests.urlopen(request) as response:
		banlists = json.loads(response.read().decode())
		advanced_id = next(obj for obj in banlists if obj['format'] == 'Tcg')['_id']

	print("Getting Advanced banlist...", flush=True)
	request = requests.Request(banlist_url % advanced_id, None, header)
	with requests.urlopen(request) as response:
		data = json.loads(response.read().decode())
		forbidden = data['forbidden']
		limited = data['limited']
		semi = data['semi_limited']

	print("Getting list of all cards...", flush=True)
	request = requests.Request(cards_url, None, header)
	with requests.urlopen(request) as response:
		cards = json.loads(response.read().decode())

	print("Getting printing data...", flush=True)
	request = requests.Request(printings_url, None, header)
	with requests.urlopen(request) as response:
		result = json.loads(response.read().decode())
		common_ids = list({card['card_id'] for card in result if card['set_rarity_code'] == 'C'})	
	
	print("Calculating legality...", flush=True)
	all_cards: List[Card] = []
	for card in cards:
		id = card['id']
		type = card['type']
		subtype = card['subtype']
		name = card['name']
		if not type in ['Skill', 'Token']:
			status = -1
			if id in common_ids:
				if id in forbidden:
					status = 0
				elif id in limited:
					status = 1
				elif id in semi:
					status = 2
				else:
					status = 3
		if type == "Spell":
			card_type = constants.CARD_TYPE_SPELL
		elif type == "Trap":
			card_type = constants.CARD_TYPE_TRAP
		else:
			if "Ritual" in subtype:
				card_type = constants.CARD_TYPE_RITUAL_MONSTER
			elif "Fusion" in subtype:
				card_type = constants.CARD_TYPE_FUSION_MONSTER
			elif "Xyz" in subtype:
				card_type = constants.CARD_TYPE_XYZ_MONSTER
			elif "Synchro" in subtype:
				card_type = constants.CARD_TYPE_SYNCHRO_MONSTER
			elif "Normal" in subtype:
				card_type = constants.CARD_TYPE_NORMAL_MONSTER
			elif "Link" in subtype:
				card_type = constants.CARD_TYPE_LINK_MONSTER
			elif "Effect" in subtype:
				card_type = constants.CARD_TYPE_EFFECT_MONSTER

		all_cards.append(Card(name, id, status, card_type))

	return all_cards

def generateBanlist(cards: List[Card]):
	with open(lflist_file, 'w', encoding="utf-8") as outfile:
		outfile.write("#[Common Charity Format]\n")
		outfile.write("!Common Charity %s.%s\n\n" % (datetime.now().month, datetime.now().year))
		for card in sorted(cards, key=lambda x: x.name.lower()):
			outfile.write("%d %d -- %s\n"%(card.id, card.status, card.name))