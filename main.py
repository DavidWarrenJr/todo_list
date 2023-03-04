from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String)
    title = db.Column(db.String(250))
    description = db.Column(db.String)
    due_year = db.Column(db.Integer)
    due_month = db.Column(db.String)
    due_day = db.Column(db.Integer)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    all_task = db.session.query(Todo).all()
    return render_template("index.html", all_task=all_task)


def get_due_month_string(month: str) -> str:
    if month == "01":
        return "Jan"
    if month == "02":
        return "Feb"
    if month == "03":
        return "Mar"
    if month == "04":
        return "Apr"
    if month == "05":
        return "May"
    if month == "06":
        return "June"
    if month == "07":
        return "July"
    if month == "08:":
        return "Aug"
    if month == "09":
        return "Sept"
    if month == "10":
        return "Oct"
    if month == "11":
        return "Nov"
    if month == "12":
        return "Dec"


def get_due_day(day: str) -> str:
    if day[0] == "0":
        return day[1]
    else:
        return day


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        print(request.form.get("cancel-btn"))
        if request.form.get("cancel-btn") == "True":
            return redirect(url_for("home"))

        image = request.form.get("image-input")
        title = request.form.get("title-input")
        description = request.form.get("description-input")
        due_date = request.form.get("date-input")

        if due_date:
            year = due_date.split('-')[0]
            month = due_date.split('-')[1]
            day = due_date.split('-')[2]

            task = Todo(image=image,
                        title=title,
                        description=description,
                        due_year=year,
                        due_month=get_due_month_string(month),
                        due_day=get_due_day(day))
        else:
            task = Todo(image=image,
                        title=title,
                        description=description)

        db.session.add(task)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template("add.html")


@app.route("/delete/<int:task_id>", methods=["GET", "POST"])
def delete(task_id):
    tasks = db.session.query(Todo).all()
    for task in tasks:
        if task.id == task_id:
            db.session.delete(task)
            db.session.commit()

    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
