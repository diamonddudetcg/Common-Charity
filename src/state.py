from typing import List
from card import Card
import card
import json

file = "state/laststate.json"

def saveState(cards:List[Card]):
	stateList = []
	for card in cards:
		stateList.append(card.toDict())
	with open(file, "w") as outfile:
		outfile.write(json.dumps(stateList))

def loadState():
	card_list:List[Card] = []
	try:
		with open(file) as lastState:
			raw_card_list = json.load(lastState)
			for obj in raw_card_list:
				card_list.append(card.cardFromDict(obj))
			return card_list
	except FileNotFoundError:
		return card_list
	
def compareToLastState(cards:List[Card]):
	last_state = loadState()
	diff = []
	for card in cards:
		try:
			previous = next(card2 for card2 in last_state if card2.name == card.name)
		except StopIteration:
			previous = None
		if previous == None:
			diff.append(card)
		else:
			if card.status != previous.status:
				diff.append(card)
	return diff