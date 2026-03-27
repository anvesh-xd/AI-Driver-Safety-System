import subprocess
import queue

def speak(text):
    subprocess.run(
        ["espeak-ng", text],
        check=False,          # never crash system on audio failure
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def run(audio_queue):
    print("Audio process started")

    while True:
        try:
            msg = audio_queue.get(timeout=1)

            if msg["type"] == "alert":
                speak(msg["message"])

        except queue.Empty:
            pass
        except Exception:
            pass
