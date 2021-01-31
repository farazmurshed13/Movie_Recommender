from flask import Flask, request, render_template
from twilio.twiml.messaging_response import MessagingResponse


app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')

# handle incoming sms
@app.route("/sms", methods=['GET', 'POST'])
def handle_sms():
    # Get the message the user sent to Twilio number
    body = request.values.get('Body', None)

    # TwiML response
    resp = MessagingResponse()
    resp.message(body)

    return str(resp)


# run flask app
if __name__ == '__main__':
    app.run()


