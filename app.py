from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

ACCESS_TOKEN = "Enter Gernerated Token from meta"
VERIFY_TOKEN = "apicloudtoken"

WHATSAPP_API_URL = "https://graph.facebook.com/v21.0"
PHONE_NUMBER_ID = "488561801012614"  

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        verify_token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if verify_token == VERIFY_TOKEN:
            return challenge, 200
        return "Verification token mismatch", 403

    if request.method == 'POST':
        data = request.json
        print("Received data: ", data)

        if 'entry' in data and len(data['entry']) > 0:
            for entry in data['entry']:
                if 'changes' in entry and len(entry['changes']) > 0:
                    for change in entry['changes']:
                        if 'value' in change and 'messages' in change['value']:
                            for message in change['value']['messages']:
                                sender_id = message['from']
                                text = message['text']['body']
                                print(f"Message from {sender_id}: {text}")

                                # Auto-reply
                                send_message(sender_id, "Hello")

        return "EVENT_RECEIVED", 200

def send_message(recipient_id, message):
    """Send a message to the specified recipient."""
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "messaging_product": "whatsapp",
        "to": recipient_id,
        "type": "text",
        "text": {"body": message},
    }
    response = requests.post(f"{WHATSAPP_API_URL}/{PHONE_NUMBER_ID}/messages", headers=headers, json=data)
    print("Message send response: ", response.json())

if __name__ == '__main__':
    app.run(port=8000, debug=True)
