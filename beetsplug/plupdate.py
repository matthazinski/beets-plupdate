from beets.plugins import BeetsPlugin
import os

class PlaylistUpdatePlugin(BeetsPlugin):
    def __init__(self):
        super(PlaylistUpdatePlugin, self).__init__()
        self.playlist_dir = self.config['playlist_dir'].get().encode('utf8')
        self.historical_paths = [x.encode('utf8') for x in self.config['historical_paths'].get()]
        self.playlists = {}  # path_to_m3u: list_of_item_paths
        self.changed_playlists = set([])

        self.register_listener('pluginload', self.loaded)
        self.register_listener('item_moved', self.post_move)
        self.register_listener('cli_exit', self.cli_exit)

    def loaded(self):
        for subdir, dirs, files in os.walk(self.playlist_dir):
            for file in files:
                fpath = os.path.join(subdir, file)
                with open(fpath) as playlist:
                    self.playlists[fpath] = playlist.read().splitlines()

    def post_move(self, item, source, destination):
        # Beets source, destination uses full paths but playlists paths are
        # relative to the music directory.
        source_relative_path = ''
        dest_relative_path = ''
        for path_prefix in self.historical_paths:
            if source.startswith(path_prefix):
                source_relative_path = os.path.relpath(source, path_prefix)
            if destination.startswith(path_prefix):
                dest_relative_path = os.path.relpath(destination, path_prefix)

        if not source_relative_path or not dest_relative_path:
            return

        for pl_path in list(self.playlists.keys()):
            # TODO inefficient - iterating twice
            if source_relative_path in self.playlists[pl_path]:
                self.changed_playlists.add(pl_path)
                self.playlists[pl_path] = [dest_relative_path if source_relative_path == x else x for x in self.playlists[pl_path]]
            if source in self.playlists[pl_path]:
                self.playlists[pl_path] = [destination if source == x else x for x in self.playlists[pl_path]]

    def cli_exit(self, lib):
        if self.changed_playlists:
            for pl_path in self.changed_playlists:
                with open(pl_path, 'w') as pl_file:
                    for line in self.playlists[pl_path]: 
                        pl_file.write("%s\n" % line)
                print('Updated {}'.format(pl_path))
