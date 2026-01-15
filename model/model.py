import networkx as nx

from database.dao import DAO


class Model:
    def __init__(self):
        self.dictAlbum = DAO.getAlbum()
        self.dictTrack = DAO.getTrack()
        self.dictPlaylistTrack = DAO.getPlaylistTrack()
        self.grafo = nx.Graph()


    def getDictDurataAlbum(self):
        result={}
        for track in self.dictTrack.values():
            if result.get(track.album_id):
                result[track.album_id] += track.milliseconds
            else:
                result[track.album_id] = track.milliseconds
        return result

    def getDictTracksAlbum(self):
        result={}
        for track in self.dictTrack.values():
                result[track.id] = track.album_id
        return result


    def getGrafo(self, durataMin):
        self.grafo.clear()
        durataMin_milliseconds = durataMin * 60000
        dictDurata=self.getDictDurataAlbum()
        dictTrackAlbum = self.getDictTracksAlbum()
        for album_id, durataAlbum in dictDurata.items():
            if durataAlbum > durataMin_milliseconds:
                self.grafo.add_node(album_id)
        for playlist_tracks in self.dictPlaylistTrack.values():
            playlist_tracks = set(playlist_tracks)
            for track_id1 in playlist_tracks:
                for track_id2 in playlist_tracks:
                    if track_id1 != track_id2:
                        album_id1 = dictTrackAlbum[track_id1]
                        album_id2 = dictTrackAlbum[track_id2]
                        if album_id1 != album_id2:
                            if self.grafo.has_node(album_id1) and self.grafo.has_node(album_id2):
                                        self.grafo.add_edge(album_id1, album_id2)
        print(self.grafo.nodes())
        print(self.grafo)


    def getComponenteConnessa(self, album_id):
        albero = nx.dfs_tree(self.grafo,album_id )
        dimensione = len(albero.nodes())
        dictDurataAlbum = self.getDictDurataAlbum()
        durataTOT = 0
        for album_id in albero.nodes():
            durataTOT += dictDurataAlbum[album_id]
        durataTOT = durataTOT / 60000
        return dimensione, durataTOT

    def getCamminoMassimo(self, durataMax, start):
        self.bestDurata = 0
        self.bestListaTrack = []
        self.dictDUrataAlbum = self.getDictDurataAlbum()
        durataMax_millisecond = durataMax
        self.ricorsione([start], self.dictDUrataAlbum[start]/60000, durataMax_millisecond)




    def ricorsione(self, parziale, durataParziale, durataMax):
        if len(parziale) > len(self.bestListaTrack):
            self.bestListaTrack = parziale.copy()
            self.bestDurata = durataParziale

        albero = nx.dfs_tree(self.grafo, parziale[0])
        for nodo in albero.nodes:
            if nodo not in parziale:
                durata = self.dictDUrataAlbum[nodo]/60000
                if durataParziale + durata <= durataMax:
                    parziale.append(nodo)
                    self.ricorsione(parziale, durataParziale + durata , durataMax)
                    parziale.pop()





