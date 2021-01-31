from flask import Flask, request, session, render_template
from twilio.twiml.messaging_response import MessagingResponse
from Backend import store_conversation as sc

SECRET_KEY = "a secret key"
app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/start")
def start():
    return render_template('start.html')

@app.route("/data", methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/start' to submit form"
    if request.method == 'POST':
        form_data = request.form
        code = 1456
        return render_template('data.html', code=code)

# handle incoming sms
@app.route("/sms", methods=['GET', 'POST'])
def handle_sms():
    # store incoming message
    # from_number = request.values.get('From')
    incoming = request.values.get('Body', None)

    # count messages in session
    counter = session.get('counter', 0)

    # determine which question to ask
    # store party code and ask q1
    if counter == 0:
        party_code = incoming
        if sc.verify_party(party_code):
            msg = "question 1"
        else:
            msg = "This party code does not exist."

    # store r1 and ask q2
    elif counter == 1:
        msg = "question 2"
    # store r2 and ask q3
    elif counter == 2:
        msg = "question 3"
    # store r3 and ask q4
    elif counter == 3:
        msg = "question 4"
    # store r4
    else:
        msg = "done!"

    # increment or reset counter
    if counter > 3:
        counter = 0
    else:
        counter += 1
    session['counter'] = counter

    # reply to user
    outgoing = MessagingResponse()
    outgoing.message(msg)

    return str(outgoing)



# run flask app
if __name__ == '__main__':
    app.run()


