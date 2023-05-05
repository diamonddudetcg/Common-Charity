from typing import List

def cardFromDict(obj:object):
	name = obj['name']
	ids = obj['ids']
	status = obj['status']
	main_id = obj['main_id']
	type = obj['type']
	return Card(name, main_id, ids, status, type)

class Card:
	def __init__(self, name: str, main_id: int, ids: List[int], status: int, type: int):
		self.name = name
		self.main_id = main_id
		self.ids = ids
		self.status = status
		self.type = type
	
	def toDict(self):
		a = {}
		a['name'] = self.name
		a['ids'] = self.ids
		a['main_id'] = self.main_id
		a['status'] = self.status
		a['type'] = self.type
		return a