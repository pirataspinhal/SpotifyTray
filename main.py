import sys
import signal
from PyQt4 import QtGui, QtCore
import json
import subprocess

def playerctl(command):
    return ["playerctl", "-p", "spotify", command]

def xdotool(command, id):
    return ["xdotool", command, str(id)]

class SpotifyWrapper(QtGui.QSystemTrayIcon):
    def __init__(self, spotify_id , parent=None):
        self.app = QtGui.QApplication(sys.argv)
        style = self.app.style()
        self.spotify_id = spotify_id
        # TODO: Find more reliable way of keeping track of spotify visibility status
        self.spotify_hidden = False

        # TODO: Change to spotify icon
        icon = QtGui.QIcon(style.standardPixmap(QtGui.QStyle.SP_FileIcon))
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)

        self.menu = QtGui.QMenu(parent)
        QtCore.QObject.connect(self.menu, QtCore.SIGNAL('aboutToShow()'), self.populate_menu)
        self.setContextMenu(self.menu)

    def populate_menu(self):
        self.menu.clear()
        playing_now = self.track_info()
        track_info = ', '.join(playing_now['artist']) + " - " + playing_now['title'] + "\nfrom: " + playing_now['album']
        self.menu.addAction(track_info, self.toggle_spotify_visibility)

        self.menu.addSeparator()
        self.menu.addAction('Pause' if self.isPlaying() else 'Play', lambda: self.play_pause())
        self.menu.addAction('Next', lambda: self.next_track())
        self.menu.addAction('Previous', lambda: self.previous_track())

        self.menu.addSeparator()
        self.menu.addAction("Exit", lambda: self.exit_pressed())

    def toggle_spotify_visibility(self):
        if self.spotify_hidden:
            self.show_spotify()
            self.spotify_hidden = False
        else:
            self.hide_spotify()
            self.spotify_hidden = True

    def hide_spotify(self):
        subprocess.call(xdotool("windowunmap", self.spotify_id))

    def show_spotify(self):
        subprocess.call(xdotool("windowmap", self.spotify_id))

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
        val = val.replace("<", "").replace(">", "").replace("'", "\"").replace("uint64 ", "")
        val = val.replace("xesam:", "").replace("mpris:", "")
        data = json.loads(val)
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
    print("spotify id: " + str(spotify_id))

    spotify = SpotifyWrapper(spotify_id)
    spotify.show()
    sys.exit(spotify.app.exec_())














if __name__ == '__main__':
    main()

