import os
import asyncio

from config import ROOT_DIR, get_tts_voice, get_tts_engine, get_edge_tts_voice

KITTEN_MODEL = "KittenML/kitten-tts-mini-0.8"
KITTEN_SAMPLE_RATE = 24000


class TTS:
    def __init__(self) -> None:
        self._engine = get_tts_engine()

        if self._engine == "kitten_tts":
            import soundfile as sf
            from kittentts import KittenTTS as KittenModel

            self._sf = sf
            self._model = KittenModel(KITTEN_MODEL)
            self._voice = get_tts_voice()
        else:
            # Default to edge_tts
            import edge_tts

            self._edge_tts = edge_tts
            self._voice = get_edge_tts_voice()

    def synthesize(self, text, output_file=None):
        if self._engine == "kitten_tts":
            if output_file is None:
                output_file = os.path.join(ROOT_DIR, ".mp", "audio.wav")
            audio = self._model.generate(text, voice=self._voice)
            self._sf.write(output_file, audio, KITTEN_SAMPLE_RATE)
            return output_file
        else:
            # Edge-TTS: save as MP3 (AudioFileClip handles MP3 fine)
            if output_file is None:
                output_file = os.path.join(ROOT_DIR, ".mp", "audio.mp3")
            communicate = self._edge_tts.Communicate(text, self._voice)
            asyncio.run(communicate.save(output_file))
            return output_file
