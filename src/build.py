import lflistgen
import sitegen
import state

saveState = True

print("Generating card list...", flush=True)
cards = lflistgen.generateCardList()
print("Generating change list...", flush=True)
diff = state.compareToLastState(cards)
if saveState:
	print("Saving last state...", flush=True)
	state.saveState(cards)
print("Generating ban list...", flush=True)
lflistgen.generateBanlist(cards)
print("Building website...", flush=True)
sitegen.generateSite(cards, diff)
print("Done", flush=True)