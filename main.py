from flask import Flask, render_template

app = Flask(__name__)

all_task = []


@app.route("/")
def home():
    return render_template("index.html", all_task=all_task)


if __name__ == "__main__":
    app.run(debug=True)
