import sys
import requests
import os
from urllib.request import urlopen
from pathlib import Path


def download_file(url, filename):
    with urlopen(url) as file:
        content = file.read()

        # Save to file
    with open(f'./emojis/{filename}', 'wb') as download:
        download.write(content)

def main():
    if len(sys.argv) < 2:
        print('Usage: getEmoji.py AUTH_TOKEN')
        exit(1)

    auth_token = sys.argv[1]
    response = requests.get('https://slack.com/api/emoji.list', headers={'Authorization':f'Bearer {auth_token}'})

    if not response.ok:
        print('Failed to get emoji metadata from Slack API. Error:', response.content)
        exit(1)

    json_response = response.json()
    if 'error' in json_response:
        print('Failed to get emoji metadata from Slack API. Error:', json_response['error'])
        exit(1)

    Path("./emojis").mkdir(parents=True, exist_ok=True)
    for name,url in json_response['emoji'].items():
        if not url.startswith('alias:'):
            _, file_extension = os.path.splitext(url)
            emoji_file_name = f'{name}{file_extension}'
            print(emoji_file_name)
            download_file(url, emoji_file_name)


if __name__ == "__main__":
    main()
