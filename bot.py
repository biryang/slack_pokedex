import os
from slack_sdk import WebClient
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter
from WebDex import poke_dex_info

env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(
    os.environ['SLACK_SIGNIG'], '/slack/events', app)

client = WebClient(token=os.environ['SLACK_TOKEN'])

BOT_ID = client.api_call("auth.test")['user_id']


@slack_events_adapter.on('message')
def message(payload):
    # print(payload)
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    # print(channel_id)

    if text is not None:
        text_equals = text[0:4] == "!도감 "
    else:
        return

    if BOT_ID != user_id and text_equals:
        if(text.replace('!도감 ', '').isdecimal()):
            poke_num = int(text.replace('!도감 ', ''))
        else:
            return

        if poke_num >= 1 and poke_num <= 893:
            poke_info = poke_dex_info(poke_num)
            client.chat_postMessage(
                channel=channel_id,
                text=f"{poke_info['name']}",
                icon_emoji=":pokeball:",
                attachments=[{
                    "author_name": "Image",
                    "image_url": f"{poke_info['img']}"
                }])


@app.route('/')
def hello():
    return 'Hello, PokeDex!'


if __name__ == "__main__":
    app.run(debug=True)
