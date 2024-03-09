from flask import Flask, render_template, Response, send_file
from flask_socketio import SocketIO, emit, disconnect
from pyfirmata2 import Arduino, util
import cv2
import io
import threading

app = Flask(__name__)
socketio = SocketIO(app, async_mode=None)
thread = None
thread_lock = threading.Lock()

@app.route('/')
def index():
    return render_template('index.html')

def gen():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture')
def capture():
    cap = cv2.VideoCapture
    ret, frame = cap.read
    if not ret:
        return 'Failed to capture image', 500
    cap.release()

    img = cv2.imencode('.jpg', frame)[1].tobytes()
    return send_file(io.BytesIO(img), mimetype='image/jpeg')

@socketio.on('move', namespace='/test')
def move(message):
    with thread_lock:
        try:
            board = Arduino('COM3')
            led_pin = board.get_pin('d:13:o')
            if message['direction'] in ['up', 'left']:
                led_pin.write(1)  # turn the LED on[^6^][6][^7^][7]
            else:
                led_pin.write(0)  # turn the LED off[^7^][7][^6^][6]
            board.exit() # close the connection
            emit('response', {'data': 'Moved ' + message['direction']})
        except Exception as e:
            emit('response', {'data': f"Failed to move {message['direction']}: {str(e)}"}, 500)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port='5000', debug=True)
