import datetime
import threading
import serial
from flask import Flask, render_template

from db import User, Session

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users')
def users():
    all_users = User.select()
    return render_template('users.html', users=all_users)

@app.route('/sessions')
def sessions():
    all_sessions = Session.select().order_by(Session.start_time.desc())
    sessions_with_duration = []

    for session in all_sessions:
        if session.end_time:
            duration = session.end_time - session.start_time
        else:
            duration = datetime.datetime.now() - session.start_time

        sessions_with_duration.append({
            'user': session.user,
            'start_time': session.start_time,
            'end_time': session.end_time,
            'active': session.active,
            'duration': duration
        })

    return render_template('sessions.html', sessions=sessions_with_duration)


SERIAL_PORT = 'COM8'
BAUD_RATE = 9600

def read_serial_data():
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            process_data(data)
            
def process_data(data):
    # Assuming the data received is the authorisation_code for a user
    if data.isalnum():
        try:
            user = User.get(User.authorisation_code == data)
            print(f"User found: {user}")
        except User.DoesNotExist:
            print("No user found with this authorisation code.")
            return None
        try:
            session = Session.get( (Session.user == user) & (Session.active == True) )
            print(f"Before saving: {session.end_time}")
            session.active = False
            session.end_time = datetime.datetime.now()
            session.save()
            print(f"Session found: {session}")
            
            session.save()
            print(f"After saving: {session.end_time}")
        except Session.DoesNotExist:
            print("No active session found for this user.")
            Session.create(user=user)
            print("New session created for this user.")
        
    else:
        print(f"Invalid data received: {data}")


def start_serial_thread():
    serial_thread = threading.Thread(target=read_serial_data)
    serial_thread.daemon = True
    serial_thread.start()


if __name__ == '__main__':
    
    start_serial_thread()
    
    app.run( host='0.0.0.0', port=8000, debug=True)