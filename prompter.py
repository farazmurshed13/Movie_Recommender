from flask import Flask, request, render_template
from twilio.twiml.messaging_response import MessagingResponse


app = Flask(__name__)


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
        return render_template('data.html', form_data = form_data)

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


