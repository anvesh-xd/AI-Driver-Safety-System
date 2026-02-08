import subprocess

print("Starting speaker test...")

text = "Hello you are going way too fast Mister!"

subprocess.run(
    ["espeak-ng", text],
    check=True
)

print("Speaker test finished.")
