from dataclasses import dataclass

@dataclass
class PlaylistTrack:
    playlist_id : int
    track_id : int

    def __hash__(self):
        return hash(self.playlist_id)