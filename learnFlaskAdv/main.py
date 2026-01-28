from flask import Flask, render_template
from admin.second import second

app = Flask(__name__)
app.register_blueprint(second, url_prefix="/admin")
# if blueprint and func here has same route, runs whatever comes first
# url prefix puts /admin in the front of url, then passes whatever comes
# after to the file the blueprint is in

@app.route("/")
def test():
    return "<h1>Test</h1>"

if __name__ == "__main__":
    app.run(debug=True)