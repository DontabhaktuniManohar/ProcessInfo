from flask import Flask, render_template
from flask_cors import CORS
from api import api_blueprint

app = Flask(__name__)
CORS(app)

# Register API routes
app.register_blueprint(api_blueprint)

# Serve the HTML UI
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
