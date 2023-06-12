import subprocess

def open_discord():
    package_name = "com.discord"
    activity_name = "com.discord.main.MainActivity"

    try:
        subprocess.run(["am", "start", "-n", f"{package_name}/{activity_name}"])
    except FileNotFoundError:
        subprocess.run(["termux-open", "https://discord.com"])

open_discord()
