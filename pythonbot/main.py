
import slack
import os
import berserk
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    os.environ['SIGN_SECRET'], '/slack/events', app
    )

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

lichess = berserk.Client()


def WatchChessGamesLive():
    channels = lichess.games.get_tv_channels()
    return channels['Blitz']['gameId']


def sendChallenge():
    timeControl = 5 * 60
    timeSecs = 0
    challenge = lichess.challenges.create_open(timeControl, timeSecs)
    lichessLink = challenge['challenge']['url']
    return lichessLink



@app.route('/watch', methods=['POST'])
def watch():
    data = request.form
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    gameid = WatchChessGamesLive()
    gifId = 'https://lichess1.org/game/export/gif/' + gameid + '.gif'
    print(sendChallenge())
    client.chat_postMessage(channel=channel_id, text=gifId)
    return Response(), 200

@app.route('/playchess', methods=['POST'])
def playchess():
    data = request.form
    channel_id = data.get('channel_id')
    gameLink = sendChallenge()
    client.chat_postMessage(channel=channel_id, text= 'Click here to play chess! ' + gameLink)



if __name__ == "__main__":
    app.run(debug=True)