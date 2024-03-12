from flask import Flask

app = Flask(__name__)

@app.route('/api/v1')
def home():
    return "Hello, Flask!"

if __name__ == "__main__":
    app.run("localhost", 8080, debug=True)