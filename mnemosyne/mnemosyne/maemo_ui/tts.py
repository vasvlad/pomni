import commands
import os

PITCH_MIN = 0
PITCH_MAX = 100
SPEED_MIN = 30
SPEED_MAX = 200

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
                player = gst.element_factory_make("playbin", "player")
                player.set_property('uri', "file://%s" % fname)
                player.set_state(gst.STATE_PLAYING)                
            self.play_sound = play

    def set_pitch(self, pitch):
        self.pitch = pitch

    def set_speed(self, speed):
        self.speed = speed

    def set_params(self, params):
        for param in params:
            setattr(self, param, params[param])

    def speak(self, text):
        command = self.espeak
        command += " -v " + self.language + self.voice
        command += " -s " + str(self.speed)
        command += " -p " + str(self.pitch)
        command += " -w /tmp/mnemosyne_tts %s" % text
        os.system(command)
        self.play_sound('/tmp/mnemosyne_tts')


        
