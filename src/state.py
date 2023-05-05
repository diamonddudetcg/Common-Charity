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
	with open(file) as lastState:
		raw_card_list = json.load(lastState)
		card_list:List[Card] = []
		for obj in raw_card_list:
			card_list.append(card.cardFromDict(obj))
		return card_list
	
def compareToLastState(cards:List[Card]):
	last_state = loadState()
	diff = []
	for card in cards:
		try:
			previous = next(card2 for card2 in last_state if card2.id == card.id)
		except StopIteration:
			previous = None
		if previous == None:
			diff.append(card.id)
		else:
			if card.status != previous.status:
				diff.append(card.id)
	return diff