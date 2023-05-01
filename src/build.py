import lflistgen
import sitegen

print("Generating card list...", flush=True)
cards = lflistgen.generateCardList()
print("Generating ban list...", flush=True)
lflistgen.generateBanlist(cards)
print("Building website...", flush=True)
sitegen.generateSite(cards)
print("Done", flush=True)