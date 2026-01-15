from model.model import Model
model = Model()
model.getGrafo(120)
print(model.getComponenteConnessa(141))
model.getCamminoMassimo(4000, 141)
print(model.bestDurata)
print(model.bestListaTrack)
