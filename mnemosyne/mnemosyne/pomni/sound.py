import re
import os
import gst

class SoundPlayer:
    def __init__(self):
        """ Init variables. """

        self.fname = ""
        self.parent = None
        self.player = gst.element_factory_make("playbin", "player")
        self.player.set_property("volume", 8)
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message", self.on_message)

    def on_message(self, bus, message):
        """ On system message. """

        mtype = message.type
        if mtype == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
            self.parent.update_indicator()
        elif mtype == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            print "SoundPlayer:error: %s" % err, debug

    def play(self, fname, parent):
        """ Play or stop playing. """

        self.parent = parent # parens is a class, which call this function
        self.fname = fname
        self.player.set_state(gst.STATE_NULL)
        self.player.set_property("uri", "file://" + self.fname)
        self.player.set_state(gst.STATE_PLAYING)

    def stop(self):
        """ Stop playing. """

        self.player.set_state(gst.STATE_NULL)

    def parse_fname(self, text):
        """ Returns filename to play. """

        return os.path.abspath(re.search(r"'[^']+'", text).group()[1:-1])
        
