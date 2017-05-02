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

No installation is required. You just need to clone the repository or download the zip file locally
```
git clone git@github.com:Kasama/SpotifyTray.git
cd SpotifyTray
```

and run the script with python
```
python3 main.py
```

You can also create a (or change spotify's) `.desktop` file to launch the script

License
-------

This project is distributed under the [MIT license][mit].

Spotify is a trademark of [Spotify Inc.][spotify] It is not my work in any way and all its rights are reserved.

[python]: https://www.python.org/downloads/release/python-361/
[pyqt]: https://www.riverbankcomputing.com/software/pyqt/download
[xdotool]: http://www.semicomplete.com/projects/xdotool
[playerctl]: https://github.com/acrisci/playerctl
[mit]: LICENSE.md
[spotify]: https://www.spotify.com
