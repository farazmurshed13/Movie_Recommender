from flask import Flask, request, session, render_template
from twilio.twiml.messaging_response import MessagingResponse
from Backend import store_conversation as sc
from Backend import movieChooser as mc

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
        form_dict = {}
        form_dict['numwatchers'] = form_data['numwatchers']
        if(form_data['mindate'] == ''):
            form_dict['mindate'] = '0'
        else:
            form_dict['mindate'] = form_data['mindate']

        if(form_data['maxdate'] == ''):
            form_dict['maxdate'] = '0'
        else:
            form_dict['maxdate'] = form_data['maxdate']

        if(form_data['minrating'] == ''):
            form_dict['minrating'] = '0'
        else:
            form_dict['minrating'] = form_data['minrating']

        code = sc.generate_code()
        sc.host_submit(form_dict, code)

        return render_template('data.html', code=code)

@app.route("/about")
def about():
    return render_template('about.html')

# handle incoming sms
@app.route("/sms", methods=['GET', 'POST'])
def handle_sms():
    # store incoming message
    incoming = request.values.get('Body', None)
    inc = int(incoming)

    # store caller
    from_number = request.values.get('From')

    # count messages in session
    counter = session.get('counter', 0)

    # determine which question to ask

    # store user, party code, and ask q1
    if counter == 0:
        if sc.verify_party(inc):
            msg = "Respond to each question with 1 to 5!\n\nWhat would you rather eat for your next meal?\n1. Cereal \U0001F963\n2. Omelette \U0001F373\n3. Spaghetti \U0001F35D\n4. Sushi \U0001F363\n5. Ghost pepper wings \U0001F357"
            counter += 1
            sc.add_member(from_number, inc)
        else:
            msg = "This party code does not exist."
            counter = 0

    # store r1 and ask q2
    elif counter == 1:
        party_code = sc.get_code(from_number)
        sc.record_response("1", inc, party_code)
        msg = "On a scale of 1 to 5, is it currently big brain time? \U0001F9E0\n1 - Last 2 brain cells\n|\n|\n5 - 4D Chess"
        counter += 1
    # store r2 and ask q3
    elif counter == 2:
        party_code = sc.get_code(from_number)
        sc.record_response("2", inc, party_code)
        msg = "What kind of pet would you most want?\n1. Fish \U0001F41F\n2. Turtle \U0001F422\n3. Dog \U0001F436\n4. Tiger \U0001F405\n5. Dragon \U0001F432"
        counter += 1
    # store r3 and ask q4
    elif counter == 3:
        party_code = sc.get_code(from_number)
        sc.record_response("3", inc, party_code)
        msg = "What's the current vibe - more Throwback Thursday \U0001F4FC or Futuristic Friday \U0001F916?\n1 - TBT \U0001F519\n|\n|\n5 - FF \U0001F51C"
        counter += 1
    # store r4; handle movie selection if last user to finish
    else:
        party_code = sc.get_code(from_number)
        sc.record_response("4", inc, party_code)
        
        # check if everyone done
        isDone = sc.done(party_code)
        if isDone:
            msg = "isDone"
            info = sc.get_tot_resp(party_code)
            # use averages of question responses as input for knn algorithm
            t = info[0] / info[4]
            b = info[1] / info[4]
            r = info[2] / info[4]
            f = info[3] / info[4]
            movies_list = mc.generateMovList(t, b, r, f, info[5], info[6], info[7])
            #msg = str(t) + str(b) + str(r) + str(f) + info[5] + info[6] + info[7]
            #msg = sc.movie_msg(ml)
            #msg = movies_list[0]
        else:
            msg = "done - waiting for other users!"

        counter = 0

    # update counter
    session['counter'] = counter

    # reply to user
    outgoing = MessagingResponse()
    outgoing.message(msg)

    return str(outgoing)



# run flask app
if __name__ == '__main__':
    app.run()


