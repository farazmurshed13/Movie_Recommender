from flask import Flask, request, session
from twilio.twiml.messaging_response import Message, MessagingResponse


SECRET_KEY = "a secret key"
app = Flask(__name__)
app.config.from_object(__name__)

# handle incoming sms
@app.route("/sms", methods=['GET', 'POST'])
def handle_sms():
    # count messages in session
    counter = session.get('counter', 0)
    counter += 1
    if counter >= 2:
        session['counter'] = 0
    else:
        session['counter'] = counter

    from_number = request.values.get('From')
    incoming = request.values.get('Body', None)

    # Get the message the user sent to Twilio number
    message = '{} was messaged by {}; {} total msg.' \
        .format(incoming, from_number, counter)

    outgoing = MessagingResponse()
    outgoing.message(message)

    return str(outgoing)


@app.route("/")
def site():
    return "hello world"

# run flask app
if __name__ == '__main__':
    app.run()


