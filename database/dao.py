from database.DB_connect import DBConnect
from model.album import Album
from model.playlistTrack import PlaylistTrack
from model.track import Track


class DAO:
    @staticmethod
    def getAlbum():
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM album """

        cursor.execute(query)

        for row in cursor:
            album = Album(**row)
            result[album.id] = album

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getTrack():
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM track """

        cursor.execute(query)

        for row in cursor:
            track = Track(**row)
            result[track.id] = track

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPlaylistTrack():
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM playlist_track """

        cursor.execute(query)

        for row in cursor:
            playlistTrack = PlaylistTrack(**row)
            if result.get(playlistTrack.playlist_id):
                result[playlistTrack.playlist_id].append(playlistTrack.track_id)
            else:
                result[playlistTrack.playlist_id] = [playlistTrack.track_id]

        cursor.close()
        conn.close()
        return result