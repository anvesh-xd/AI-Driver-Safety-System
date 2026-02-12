import subprocess

print("Starting speaker test...")

text = " You are going way too fast Mister "

subprocess.run(
    ["espeak-ng", text],
    check=True
)

print("Speaker test finished.")
