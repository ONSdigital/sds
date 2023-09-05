import requests

# A new method to send slack alerts using webhook url


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
