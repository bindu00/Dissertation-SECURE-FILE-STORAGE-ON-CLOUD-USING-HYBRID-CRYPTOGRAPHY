from flask import Flask,render_template
from mymail import send_email
app=Flask(__name__)
@app.route('/')
def index():
    send_email("hi", "hello ggg", "dhaatrisolutions@gmail.com")
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)