#! /usr/bin/env python3

import sys
import ast
import signal
import subprocess
from PyQt4 import QtGui, QtCore


def playerctl(command):
    return ["playerctl", "-p", "spotify", command]


def xdotool(command, id):
    return ["xdotool", command, str(id)]


class SpotifyWrapper(QtGui.QSystemTrayIcon):
    def __init__(self, spotify_id, parent=None):
        self.app = QtGui.QApplication(sys.argv)
        self.spotify_id = spotify_id
        # TODO: Find more reliable way of keeping track of spotify visibility status
        self.spotify_hidden = False

        # TODO: Change to spotify icon
        # icon = QtGui.QIcon(style.standardPixmap(QtGui.QStyle.SP_FileIcon))
        icon = QtGui.QIcon("./spotify.png")
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)

        self.menu = QtGui.QMenu(parent)
        QtCore.QObject.connect(self.menu, QtCore.SIGNAL('aboutToShow()'), self.populate_menu)
        QtCore.QObject.connect(self, QtCore.SIGNAL('activated(QSystemTrayIcon::ActivationReason)'), self.icon_click)
        self.setContextMenu(self.menu)

    def icon_click(self, reason):
        self.toggle_spotify_visibility()

    def populate_menu(self):
        self.menu.clear()
        playing_now = self.track_info()
        track_info = ', '.join(playing_now['artist']) + " - " + playing_now['title'] + "\nfrom: " + playing_now['album']
        self.menu.addAction(track_info, lambda: self.toggle_spotify_visibility())

        self.menu.addSeparator()
        self.menu.addAction('Show Spotify', lambda: self.show_spotify())
        self.menu.addAction('Hide Spotify', lambda: self.hide_spotify())

        self.menu.addSeparator()
        self.menu.addAction('Pause' if self.isPlaying() else 'Play', lambda: self.play_pause())
        self.menu.addAction('Next', lambda: self.next_track())
        self.menu.addAction('Previous', lambda: self.prev_track())

        self.menu.addSeparator()
        self.menu.addAction("Exit", lambda: self.exit_pressed())

    def toggle_spotify_visibility(self):
        if self.spotify_hidden:
            self.show_spotify()
        else:
            self.hide_spotify()

    def hide_spotify(self):
        subprocess.call(xdotool("windowunmap", self.spotify_id))
        self.spotify_hidden = True

    def show_spotify(self):
        subprocess.call(xdotool("windowmap", self.spotify_id))
        subprocess.call(xdotool("windowactivate", self.spotify_id))
        self.spotify_hidden = False

    def play_pause(self):
        subprocess.call(playerctl("play-pause"))

    def next_track(self):
        subprocess.call(playerctl("next"))

    def prev_track(self):
        subprocess.call(playerctl("previous"))

    def exit_pressed(self):
        subprocess.call(xdotool("windowclose", self.spotify_id))
        QtGui.QApplication.quit()

    def isPlaying(self):
        val = subprocess.check_output(playerctl("status")).decode("utf-8")
        if val == "Playing\n":
            return True
        else:
            return False

    def track_info(self):
        val = subprocess.check_output(playerctl("metadata")).decode("utf-8")
        val = val.replace("<", "").replace(">", "").replace("uint64 ", "")
        val = val.replace("xesam:", "").replace("mpris:", "")
        # Evaluating literally because of single/double quotes problem "this 'string', for an example"
        data = ast.literal_eval(val)
        # data = json.loads(val)
        return data


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    find_spotify_command = ["xdotool", "search", "--onlyvisible", "--limit", "1", "--class", "spotify"]
    find_failed = subprocess.call(find_spotify_command)

    if find_failed == 1:
        spotify_process = subprocess.Popen(["spotify"])

    while find_failed == 1:
        find_failed = subprocess.call(find_spotify_command)
    spotify_id = int(subprocess.check_output(find_spotify_command))

    spotify = SpotifyWrapper(spotify_id)
    spotify.show()
    sys.exit(spotify.app.exec_())


if __name__ == '__main__':
    main()
