from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

if __name__ == '__main__':
    print("Starting minimal Flask app on port 5555...")
    app.run(host='127.0.0.1', port=5555, debug=False)
