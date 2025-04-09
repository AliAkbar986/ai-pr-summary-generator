
import os
import subprocess
import requests

HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
HF_TOKEN = os.getenv("HF_TOKEN")
headers = {"Authorization": f"Bearer {HF_TOKEN}"}


def get_latest_commit_message():
    result = subprocess.run(['git', 'log', '-1', '--pretty=%B'], capture_output=True, text=True)
    return result.stdout.strip()


def query_huggingface(prompt):
    payload = {"inputs": prompt}
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        print("Error from HF API:", response.text)
        return "Could not generate changelog entry."
    return response.json()[0]['generated_text']


def update_changelog(entry):
    with open("CHANGELOG.md", "a") as f:
        f.write(f"\n- {entry}\n")


if __name__ == "__main__":
    commit_message = get_latest_commit_message()
    prompt = f"Summarize this commit for a changelog: {commit_message}"
    changelog_entry = query_huggingface(prompt)
    update_changelog(changelog_entry)
    print("Changelog updated.")
