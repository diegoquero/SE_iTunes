import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""

        if self._view.txt_durata.value is None or not self._view.txt_durata.value.isnumeric():
            self._view.show_alert('inserire una durata valida')
            return
        durata = int(self._view.txt_durata.value)
        self._model.getGrafo(durata)
        numNodi = self._model.grafo.number_of_nodes()
        numArchi = self._model.grafo.number_of_edges()
        self._view.lista_visualizzazione_1.clean()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f'grafo creato : Album {numNodi}, archi {numArchi}'))

        for album_id in self._model.grafo.nodes():
            nome_album = self._model.dictAlbum[album_id].title
            self._view.dd_album.options.append(ft.dropdown.Option(text=nome_album, key=album_id))

        self._view.update()

    def abilita_componente(self, e):
        self._view.pulsante_analisi_comp.disabled = False
        self._view.pulsante_set_album.disabled = False
        self._view.update()


    def handle_analisi_comp(self, e):
        """ Handler per gestire l'analisi della componente connessa """""
        album_id = int(self._view.dd_album.value)
        dimensione, durata = self._model.getComponenteConnessa(album_id)
        self._view.lista_visualizzazione_2.clean()
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f'dimensione componente : {dimensione}'))
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f'durata totale : {durata}'))
        self._view.update()


    def handle_get_set_album(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del set di album """""
        if self._view.txt_durata_totale.value is None or not self._view.txt_durata_totale.value.isnumeric():
            self._view.show_alert('inserire una durata valida')
            return
        durata = int(self._view.txt_durata_totale.value)
        start = int(self._view.dd_album.value)

        self._model.getCamminoMassimo(durata, start)
        listaAlbum = self._model.bestListaTrack
        durataTotale = self._model.bestDurata
        self._view.lista_visualizzazione_3.clean()
        self._view.lista_visualizzazione_3.controls.append(ft.Text(f'Set Trovato: lunghezza : {len(listaAlbum)}, durata totale : {durataTotale}'))
        for album_id in listaAlbum:
            nome_album = self._model.dictAlbum[album_id].title
            durataAlbum = self._model.dictDUrataAlbum[album_id]/60000
            self._view.lista_visualizzazione_3.controls.append(ft.Text(f'-{nome_album} : {durataAlbum} min'))
        self._view.update()
