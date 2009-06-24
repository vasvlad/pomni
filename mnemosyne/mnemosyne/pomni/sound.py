from mnemosyne.libmnemosyne.filter import Filter
import re
import os
import gst

class SoundPlayer(Filter):
    def __init__(self):
        self.player = gst.element_factory_make("playbin", "player")
        self.state = "stopped"
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message", self.on_message)

    def on_message(self, bus, message):
        """ On system message. """

        t = message.type
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
            self.state = "stopped"
        elif t == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            print "SoundPlayer:error: %s" % err, debug

    def play(self, fname):
        """ Play or stop playing. """

        if self.state == "stopped":
            self.player.set_property("uri", "file://" + fname)
            self.player.set_state(gst.STATE_PLAYING)
            self.state = "playing"
        else:
            self.player.set_state(gst.STATE_NULL)
            self.state = "stopped"
            
        
    def run(self, text, fact):
        """ Filter hook. """

        if "sound src=" in text:
            fname = os.path.abspath(re.search(r"'[^']+'", text).group()[1:-1])
            self.play(fname)
            return "Press here to play/stop listening"
        return text

