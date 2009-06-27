from mnemosyne.libmnemosyne.filter import Filter
import re
import os
import gst

class SoundPlayer(Filter):
    def __init__(self):
        self.name = "soundmanager"
        self.fname = ""
        self.player = gst.element_factory_make("playbin", "player")
        self.player.set_property("volume", 8)
        self.stopped = True
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message", self.on_message)

    def on_message(self, bus, message):
        """ On system message. """

        t = message.type
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
            self.stopped = True
        elif t == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            print "SoundPlayer:error: %s" % err, debug

    def play(self, fname=None):
        """ Play or stop playing. """

        if self.stopped:
            if fname:
                self.fname = fname
            self.player.set_property("uri", "file://" + self.fname)
            self.player.set_state(gst.STATE_PLAYING)
            self.stopped = False
        else:
            self.stop()

    def stop(self):
        """ Stop playing. """

        self.player.set_state(gst.STATE_NULL)
        self.stopped = True

    def parse_fname(self, text):
        """ Returns filename to play. """

        return os.path.abspath(re.search(r"'[^']+'", text).group()[1:-1])
        

    def run(self, text, fact):
        """ Filter hook. """

        if "sound src=" in text:
            self.play(self.parse_fname(text))
        return text

