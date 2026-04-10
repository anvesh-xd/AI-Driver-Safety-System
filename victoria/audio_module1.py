import os
import subprocess
import queue

def play_audio(audio_file):
    subprocess.run(
        ["cvlc", "--play-and-exit", audio_file],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def run(audio_queue):
    print("Audio process started")

    sound_map = {
        "Reduce speed.": "audio_victoria/audioAI/reduce.speed.mp3",
        "Warning. Abrupt vehicle movement detected.": "audio_victoria/audioAI/warning.abrupt.movement.detected.mp3",
        "Warning. Stop sign detected.": "audio_victoria/audioAI/warning.stop.sign.detected.mp3"
    }

    while True:
        try:
            msg = audio_queue.get(timeout=1)

            if msg["type"] == "alert":
                message = msg["message"]
                audio_file = sound_map.get(message)

                if audio_file and os.path.exists(audio_file):
                    play_audio(audio_file)
                else:
                    print("Missing audio file for:", message)

        except queue.Empty:
            pass
        except Exception as e:
            print("Audio error:", e)
