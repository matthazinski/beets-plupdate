beets playlist updater
======================

This is a small plugin for [beets](https://github.com/beetbox/beets) that
updates M3U playlists when beets moves your files around. It's pretty handy
when you occasionally move your music library between mount points or want to
change your file naming scheme without losing playlists.


Config
======

Append the following to your beets config (usually `~/.config/beets/config.yaml`):

```yaml
plupdate:
    playlist_dir: /path/to/playlists
    historical_paths:
        - /path/to/beets/library
```

If your beets database includes multiple base paths that point to music files,
include them all in `historical_paths`.


TODO
====

This wasn't written with efficiency in mind as I only have about 100
human-generated playlists. A lot of the search/sort logic can be optimized.

I have only tested this using playlists with relative paths (which is the
ncmpcpp default). Doing otherwise could break things.

