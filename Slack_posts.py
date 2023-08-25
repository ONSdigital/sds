from Publish_schema import publish_schema_to_sds
import requests


def send_slack_notification(message):
    webhook_url = "https://hooks.slack.com/services/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"
    payload = {"text": message}
    response = requests.post(webhook_url, json=payload)
    if response.status_code == 200:
        print("Notification sent successfully.")
    else:
        print(
            f"Failed to send notification. Status code: {response.status_code}, Response: {response.text}"
        )
