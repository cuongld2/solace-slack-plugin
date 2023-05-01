import os
# Use the package we installed
from slack_bolt import App

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING")
)


# Add functionality here
# @app.event("app_home_opened") etc

@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    try:
        # views.publish is the method that your app uses to push a view to the Home tab
        client.views_publish(
            # the user that opened your app's app home
            user_id=event["user"],
            # the view object that appears in the app home
            view={
                "type": "home",
                "callback_id": "home_view",

                # body of the view
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Welcome to your _App's Home_* :tada:"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "This button won't do much for now but you can set up a listener for it using the `actions()` method and passing its unique `action_id`. See an example in the `examples` folder within your Bolt app."
                        }
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Click me!"
                                }
                            }
                        ]
                    }
                ]
            }
        )

    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")


@app.command("/subscribe-solace")
def subscribe_solace(ack, respond, command):
    # Acknowledge command request
    ack()
    user_input = command['text']

    list_params = user_input.split(" ")

    response_conversation_list = app.client.conversations_list(types="private_channel")

    print(response_conversation_list)
    for each_channel in response_conversation_list['channels']:
        if list_params[0] == each_channel['name']:
            app.client.conversations_invite(channel=each_channel['id'], users=list_params[1])
    # respond(response_conversation_list)


@app.command("/book-meeting")
def book_meeting(ack, respond, command):
    # Acknowledge command request
    ack()
    # Call book meeting API
    import requests

    user_input = command['text']

    list_params = user_input.split(" ")

    url = 'http://localhost:4000/api/meetings/'
    myobj = {
        "sender_userid": f"{list_params[0]}",
        "receiver_userid": [f"{list_params[1]}"],
        "meeting_title": f"{list_params[2]}",
        "meeting_description": f"{list_params[3]}",
        "meeting_category": f"{list_params[4]}"
    }
    print(myobj)

    requests.post(url, json=myobj)


if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3001)))
