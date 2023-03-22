from flask import Flask, render_template
from brokenaccess.idor import idor

app = Flask(__name__)
app.secret_key = 'mysecretkey'

app.register_blueprint(idor, url_prefix='/brokenaccess')

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
