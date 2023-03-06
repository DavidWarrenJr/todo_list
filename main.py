from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

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


class Doing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String)
    title = db.Column(db.String(250))
    description = db.Column(db.String)
    due_year = db.Column(db.Integer)
    due_month = db.Column(db.String)
    due_day = db.Column(db.Integer)


class Done(db.Model):
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
    todo_tasks = db.session.query(Todo).all()
    doing_tasks = db.session.query(Doing).all()
    done_tasks = db.session.query(Done).all()

    return render_template("index.html",
                           all_task=todo_tasks,
                           doing_task=doing_tasks,
                           done_task=done_tasks)


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
    col_type = request.args.get("column_type")
    if col_type == "Todo":
        tasks = db.session.query(Todo).all()
        for task in tasks:
            if task.id == task_id:
                db.session.delete(task)
                db.session.commit()
    elif col_type == "Doing":
        tasks = db.session.query(Doing).all()
        for task in tasks:
            if task.id == task_id:
                db.session.delete(task)
                db.session.commit()
    elif col_type == "Done":
        tasks = db.session.query(Done).all()
        for task in tasks:
            if task.id == task_id:
                db.session.delete(task)
                db.session.commit()

    return redirect(url_for('home'))


def remove_prev_entry(end_container, start_container, title):
    if end_container == start_container:
        return

    task = None
    if start_container == "Todo":
        task = db.session.query(Todo).filter_by(title=title).first()
    elif start_container == "Doing":
        task = db.session.query(Doing).filter_by(title=title).first()
    elif start_container == "Done":
        task = db.session.query(Done).filter_by(title=title).first()

    if task:
        db.session.delete(task)
        db.session.commit()


@app.route("/update", methods=["POST"])
def update():
    if request.method == 'POST':
        data = request.get_json()

        title = data["title"]
        description = data["description"]
        due_date = data["due_date"]
        end_container = data["end_container"].title()
        start_container = data["start_container"].title()

        remove_prev_entry(end_container, start_container, title)

        if end_container == "Todo":
            if not db.session.query(Todo).filter_by(title=title).first():
                if due_date != "None":
                    month = due_date.split()[1]
                    day = due_date.split()[2]

                    task = Todo(title=title,
                                description=description,
                                due_month=month,
                                due_day=day)
                else:
                    task = Todo(title=title,
                                description=description)

                db.session.add(task)
                db.session.commit()
        elif end_container == "Doing":
            if not db.session.query(Doing).filter_by(title=title).first():
                if due_date != "None":
                    month = due_date.split()[1]
                    day = due_date.split()[2]

                    task = Doing(title=title,
                                 description=description,
                                 due_month=month,
                                 due_day=day)
                else:
                    task = Doing(title=title,
                                 description=description)

                db.session.add(task)
                db.session.commit()
        elif end_container == "Done":
            if not db.session.query(Done).filter_by(title=title).first():
                if due_date != "None":
                    month = due_date.split()[1]
                    day = due_date.split()[2]

                    task = Done(title=title,
                                description=description,
                                due_month=month,
                                due_day=day)
                else:
                    task = Done(title=title,
                                description=description)

                db.session.add(task)
                db.session.commit()

        return 'Sucesss', 200


if __name__ == "__main__":
    app.run(debug=True)
