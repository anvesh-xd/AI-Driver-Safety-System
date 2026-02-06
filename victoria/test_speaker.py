import subprocess

print("Starting speaker test...")

text = "Hello. This is a speaker test."

subprocess.run(
    ["espeak-ng", text],
    check=True
)

print("Speaker test finished.")
