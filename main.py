from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(255))
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(255))
    coffee_price = db.Column(db.String(255))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# enable when want create the table
# db.create_all()

@app.route("/")
def home():
    cafes_query = Cafe.query.all()
    cafes = [cafe.as_dict() for cafe in cafes_query]
    return render_template("home.html", cafes=cafes)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form.get('name')
        map_url = request.form.get('map_url')
        img_url = request.form.get('img_url')
        location = request.form.get('location')
        has_sockets = request.form.get('has_sockets') == "on"
        has_toilet = request.form.get('has_toilet') == "on"
        has_wifi = request.form.get('has_wifi') == "on"
        can_take_calls = request.form.get('can_take_calls') == "on"
        seats = request.form.get('seats')
        coffee_price = request.form.get('coffee_price')

        cafe = Cafe(
            name=name,
            map_url=map_url,
            img_url=img_url,
            location=location,
            has_sockets=has_sockets,
            has_toilet=has_toilet,
            has_wifi=has_wifi,
            can_take_calls=can_take_calls,
            seats=seats,
            coffee_price=coffee_price,
        )
        print(cafe.as_dict())

        db.session.add(cafe)
        db.session.commit()
        return redirect("/")

    return render_template("add.html")


app.run(port=5050, debug=True)
