from app import app

# Decorators which define the app route, both decorate the index function
@app.route("/api/v1")
@app.route("/index")
def index():
    return "Hello World Again"