#!/usr/bin/python -tt7
# vim: sw=4 ts=4 expandtab ai
#
# Pomni. Learning tool based on spaced repetition technique
#
# Copyright (C) 2008 Pomni Development Team <pomni@googlegroups.com>
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301 USA
#

"""
Sound engines.
"""

import re
import os
import gst

class GstSoundEngine:
    """Sound engine."""

    def __init__(self):
        """Init variables."""

        self.fname = ""
        self.parent = None
        self.player = gst.element_factory_make("playbin", "player")
        self.player.set_property("volume", 8)
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message", self.on_message)

    def on_message(self, bus, message):
        """On system message."""

        mtype = message.type
        if mtype == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
            self.parent.update_indicator()
        elif mtype == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            print "GstSoundEngine:error: %s" % err, debug

    def play(self, fname, parent):
        """Start playing fname."""

        self.parent = parent # parens is a class, which call this function
        self.fname = self.parse_fname(fname)
        self.player.set_property("uri", "file://" + self.fname)
        self.player.set_state(gst.STATE_PLAYING)

    def stop(self):
        """Stop playing."""

        self.player.set_state(gst.STATE_NULL)
        self.parent.update_indicator()

    @staticmethod
    def parse_fname(text):
        """Returns filename to play."""

        return os.path.abspath(re.search(r"'[^']+'", text).group()[1:-1])
       

class SoundPlayer:
    """Sound Player Interface."""

    def __init__(self):
        self.soundengine = None

    def play(self, text, parent):
        """Start playing."""

        if not self.soundengine:
            self.soundengine = GstSoundEngine()
        self.soundengine.play(text, parent)

    def stop(self):
        """Stop playing."""

        if self.soundengine:
            self.soundengine.stop()

