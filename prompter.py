from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse


app = Flask(__name__)

# handle incoming sms
@app.route("/sms", methods=['GET', 'POST'])
def handle_sms():
    # Get the message the user sent to Twilio number
    code = request.values.get('Body', None)


    # TwiML comms
    ask()
    q2()
    q3()

    q3r = request.values.get('Body', None)
    resp = MessagingResponse()
    resp.message("done")

    return(str(resp))


def ask():
    resp = MessagingResponse()
    resp.message("q1")
    return (str(resp))

def q2():
    q1r = request.values.get('Body', None)
    resp = MessagingResponse()
    resp.message("q2")
    return (str(resp))

def q3():
    q2r = request.values.get('Body', None)
    resp = MessagingResponse()
    resp.message("q3")
    return (str(resp))

@app.route("/")
def site():
    return "hello world"

# run flask app
if __name__ == '__main__':
    app.run()


