from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    due_month = db.Column(db.String)
    due_day = db.Column(db.Integer)


class Doing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    due_month = db.Column(db.String)
    due_day = db.Column(db.Integer)


class Done(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
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
                           todo_task=todo_tasks,
                           doing_task=doing_tasks,
                           done_task=done_tasks)


def get_due_month_string(month: str) -> str:
    """Takes month as string of numbers and returns the abbreviation as a string"""
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
    """Takes the day number as a string and remove leading zero if day is less than 10"""
    if day[0] == "0":
        return day[1]
    else:
        return day


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        # cancel button is clicked do nothing
        if request.form.get("cancel-btn") == "True":
            return redirect(url_for("home"))

        title = request.form.get("title-input")
        description = request.form.get("description-input")
        due_date = request.form.get("date-input")

        if due_date:
            # extract month and day from the date string
            month = due_date.split('-')[1]
            day = due_date.split('-')[2]

            task = Todo(title=title,
                        description=description,
                        due_month=get_due_month_string(month),
                        due_day=get_due_day(day))

        else:
            task = Todo(title=title,
                        description=description)

        db.session.add(task)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("add.html")


def remove_task(tasks, task_to_delete_id):
    for task in tasks:
        if task.id == task_to_delete_id:
            db.session.delete(task)
            db.session.commit()


@app.route("/delete/<int:task_to_delete_id>", methods=["GET", "POST"])
def delete(task_to_delete_id):
    col_type = request.args.get("column_type")

    if col_type == "Todo":
        tasks = db.session.query(Todo).all()
        remove_task(tasks, task_to_delete_id)
    elif col_type == "Doing":
        tasks = db.session.query(Doing).all()
        remove_task(tasks, task_to_delete_id)
    elif col_type == "Done":
        tasks = db.session.query(Done).all()
        remove_task(tasks, task_to_delete_id)

    return redirect(url_for('home'))


def remove_prev_entry(end_container, start_container, title):
    """Deletes old copy of object that was just dropped from the database to prevent duplicates"""
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


def update_database(title, description, due_date, end_container):
    """Converts data to correct format and add to database"""

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


@app.route("/update", methods=["POST"])
def update():
    """Updates database after drag and drop is completed"""
    if request.method == 'POST':
        data = request.get_json()

        title = data["title"]
        description = data["description"]
        due_date = data["due_date"]
        end_container = data["end_container"].title()
        start_container = data["start_container"].title()

        if start_container == end_container:
            pass
        else:
            update_database(title=title,
                            description=description,
                            due_date=due_date,
                            end_container=end_container)

        remove_prev_entry(end_container, start_container, title)

        return 'Success', 200


if __name__ == "__main__":
    app.run(debug=True)
