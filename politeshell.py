# politeshell.py

import os
import subprocess
from politeness import detect_politeness, classify_politeness, PHRASES


def clean_polite_phrases(command: str) -> str:
    cmd = command
    for phrase in sorted(PHRASES, key=len, reverse=True):
        lower_cmd = cmd.lower()
        lower_phrase = phrase.lower()
        idx = lower_cmd.find(lower_phrase)
        if idx != -1:
            cmd = cmd[:idx] + cmd[idx + len(phrase) :]
    return cmd.strip()


def main():
    print("\nWelcome to PoliteShell")
    print("Politeness is required—type 'exit' or Ctrl-D to quit.\n")

    while True:
        try:
            user = input("PoliteShell> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye. Stay courteous!")
            break

        if user.lower() in ("exit", "quit"):
            print("Goodbye. Stay courteous!")
            break

        score = detect_politeness(user)
        level = classify_politeness(score)

        if level == "rude":
            print("I'm sorry, but you must ask politely.")
            continue
        if level == "basic_politeness":
            print("Accepting your command...")
        elif level == "good_politeness":
            print("Thank you for being polite.")
        else:
            print("Beautiful manners!")

        cmd = clean_polite_phrases(user)
        if not cmd:
            print("No command detected after polite words.")
            continue

        if cmd.startswith("cd "):
            path = cmd[3:].strip()
            try:
                os.chdir(path)
            except Exception as e:
                print(f"cd error: {e}")
            continue

        subprocess.run(cmd, shell=True)


if __name__ == "__main__":
    main()
