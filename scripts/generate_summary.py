
import sys
import requests
import json
import os

HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
HF_TOKEN = os.getenv("HF_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("GITHUB_REPOSITORY")

headers = {"Authorization": f"Bearer {HF_TOKEN}"}


def query_huggingface(prompt):
    payload = {"inputs": prompt}
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        print("Error from HF API:", response.text)
        return "Could not generate summary."
    return response.json()[0]['generated_text']


def post_comment_to_pr(summary, pr_number):
    url = f"https://api.github.com/repos/{REPO}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = json.dumps({"body": summary})
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 201:
        print("Comment posted successfully.")
    else:
        print("Failed to post comment:", response.text)


if __name__ == "__main__":
    pr_title = sys.argv[1]
    pr_diff_url = sys.argv[2]
    pr_number = sys.argv[3]

    diff = requests.get(pr_diff_url).text

    prompt = f"Generate a concise PR summary for the following title and code diff.\nTitle: {pr_title}\nCode Diff:\n{diff[:4000]}"

    summary = query_huggingface(prompt)
    post_comment_to_pr(summary, pr_number)
