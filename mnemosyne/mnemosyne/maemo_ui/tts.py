#!/usr/bin/python -tt
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
TTS engine wrapper.
"""

import commands
import os

def is_available():
    """Checks espeak available on system."""

    if commands.getoutput("which espeak"):
        return True
    return False


class TTS:
    """TTS main class."""

    def __init__(self, language, voice, pitch, speed):
        self.espeak = commands.getoutput("which espeak")
        self.language = language
        self.voice = voice
        self.pitch = pitch
        self.speed = speed
        try:
            import hildon
            self.play_sound = hildon.hildon_play_system_sound
        except ImportError:
            import gst
            def play(fname):
                """gst play function."""
                player = gst.element_factory_make("playbin", "player")
                player.set_property('uri', "file://%s" % fname)
                player.set_state(gst.STATE_PLAYING)                

            self.play_sound = play

    def set_params(self, params):
        """Sets current espeak params."""

        for param in params:
            setattr(self, param, params[param])

    def speak(self, text):
        """Speak text."""

        if not text:
            return
        command = self.espeak
        command += " -v " + self.language + self.voice
        command += " -s " + str(self.speed)
        command += " -p " + str(self.pitch)
        command += " -w /tmp/mnemosyne_tts %s" % text
        os.system(command)
        self.play_sound('/tmp/mnemosyne_tts')


        
