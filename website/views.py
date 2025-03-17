from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from models import Note, User
from setup import db
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from_address = "j.hansen.pythonanywhere@gmail.com"


views = Blueprint('views', __name__)

def send_email(to_user, body, subject):
    to_address = to_user.email
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = to_address

    html = body

    # Record the MIME type - text/html.
    part1 = MIMEText(html, 'html')

    # Attach parts into message container
    msg.attach(part1)

    # Credentials
    username = from_address
    password = 'sekq aqrs nybl bzja'

    # Sending the email
    ## note - this smtp config worked for me, I found it googling around, you may have to tweak the # (587) to get yours to work
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(from_address, to_address, msg.as_string())
    server.quit()

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')#Gets the note from the HTML

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note
            db.session.add(new_note) #adding the note to the database
            db.session.commit()
            flash('Note added!', category='success')

            email_message = f'Neues Todo "{note}"'
            send_email(current_user, email_message, 'Neues ToDo')



    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            email_message = f'ToDo  "{note.data}" wurde entfernt'
            send_email(current_user, email_message, "ToDo entfernt")

    return jsonify({})
