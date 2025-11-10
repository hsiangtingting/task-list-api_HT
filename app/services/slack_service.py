import os
import requests


def send_slack_notification(message):

    slack_token = os.environ.get("SLACK_BOT_TOKEN")
    slack_channel = os.environ.get("SLACK_CHANNEL_NAME", "test-slack-api")

    if not slack_token:
        return False

    slack_url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/json"
    }
    json_payload = {
        "channel": slack_channel,
        "text": message
    }

    try:
        response = requests.post(
            slack_url,
            headers=headers,
            json=json_payload,
            timeout=5
        )

        if not response.json().get("ok"):
            print(f"Failed to send Slack notification: {response.json().get('error')}")
            return False

        return True

    except requests.exceptions.RequestException as e:
        print(f"Failed to send Slack notification: {e}")
        return False

