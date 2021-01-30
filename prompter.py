from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse


app = Flask(__name__)

# handle incoming sms
@app.route("/sms", methods=['GET', 'POST'])
def handle_sms():
    # Get the message the user sent to Twilio number
    #body = request.values.get('Body', None)

    # TwiML response
    resp = MessagingResponse()
    resp.message("hello")

    return str(resp)


# run flask app
if __name__ == '__main__':
    app.run()


