from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse


app = Flask(__name__)

# handle incoming sms
@app.route("/sms", methods=['GET', 'POST'])
def handle_sms():
    # Get the message the user sent to Twilio number
    body = request.values.get('Body', None)

    # TwiML response
    resp = MessagingResponse()
    resp.message(body)
    print(str(resp))

    body = request.values.get('Body', None)
    resp.message(body)
    print(str(resp))
    return


@app.route("/")
def site():
    return "hello world"

# run flask app
if __name__ == '__main__':
    app.run()


