def cardFromDict(obj:object):
	name = obj['name']
	id = obj['id']
	status = obj['status']
	type = obj['type']
	return Card(name, id, status, type)

class Card:
	def __init__(self, name: str, id: int, status: int, type: int):
		self.name = name
		self.id = id
		self.status = status
		self.type = type
	
	def toDict(self):
		a = {}
		a['name'] = self.name
		a['id'] = self.id
		a['status'] = self.status
		a['type'] = self.type
		return a