Spotify Tray Wrapper
====================

This project aims to overcome the problem the latest spotify versions introduced, which is that they have removed the tray icon and the possibility to minimize the player to tray on the Linux official client. This has forced many users to use the outdated client, which had this feature.

What this program does:

- Finds a running instance of spotify (or launches a new one).
- Creates a Tray icon with a menu to control playback (play/pause, next, previous).
- Adds the possiblity to hide the spotify client (minimize to tray).

Requirements
------------

- A Linux distribuition (as the problem is not present on Windows/MacOS)
- [Python >= 3][python] (to run the script)
	- [PyQt4][pyqt] (to manage tray icon and menu)
- [xdotool][xdotool] (to hide/show spotify)
- [playerctl][playerctl] (to control playback)

Installation
------------

### Arch Linux

__AUR Support will be added later__

Clone the [`PKGBUILD`][pkgbuild] Repository and run `makepkg`

```sh
$ git clone git@github.com:Kasama/SpotifyTrayPKGBUILD.git
$ cd SpotifyTrayPKGBUILD
$ makepkg -s
```
You can then install the generated package with `pacman -U`

```sh
# pacman -U spotify-tray*.tar.xz
```

### Other Distros

__Real installation will be implemented soon, for now you can follow below__

No installation is required. You just need to clone the repository or download the zip file locally
```sh
$ git clone git@github.com:Kasama/SpotifyTray.git
$ cd SpotifyTray
```

and run the script with python
```sh
$ python3 spotify-tray.py
```

You can also use the provided `.desktop` file to launch the script. The `.desktop` should be in `/usr/share/applications/` or `~/.local/share/applications` and the python script should be in your `$PATH`

Known Bugs
----------

- If you close spotify manually with this program running, it will hang useless and you won't be able to close it.

You can kill it with:
```sh
kill -9 `ps -aux | grep spotify-tray | head -1 | sed 's/\s\+/ /g' | cut -d' ' -f2`
```

License
-------

This project is distributed under the [MIT license][mit].

Spotify is a trademark of [Spotify Inc.][spotify] It is not my work in any way and all its rights are reserved.

[python]: https://www.python.org/downloads/release/python-361/
[pyqt]: https://www.riverbankcomputing.com/software/pyqt/download
[xdotool]: http://www.semicomplete.com/projects/xdotool
[playerctl]: https://github.com/acrisci/playerctl
[pkgbuild]: https://github.com/Kasama/SpotifyTrayPKGBUILD
[mit]: LICENSE.md
[spotify]: https://www.spotify.com
