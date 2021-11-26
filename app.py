from flask import Flask, render_template, jsonify, request
from flask_debugtoolbar import DebugToolbarExtension
from models import Cupcake, db, connect_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


app.debug = DebugToolbarExtension
app.debug = True
toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.route("/api/cupcakes")
def json_all_cupcakes():
    """Returns json with all cupcakes"""
    all_cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in all_cupcakes]
    return jsonify(cupcakes=serialized)

@app.route("/api/cupcakes", methods=["POST"])
def post_one_cupcake():
    """POST request to create a new cupcake"""
    data = request.json
    new_cupcake = Cupcake(flavor=data["flavor"], rating=float(data["rating"]), size=data["size"], image=data["image"] or None)
    db.session.add(new_cupcake)
    db.session.commit()

    return (jsonify(cupcake=new_cupcake.serialize()), 201)

@app.route("/api/cupcakes/<int:id>")
def json_one_cupcake(id):
    """Returns json with cupcake info"""
    c = Cupcake.query.get_or_404(id)
    serialized = c.serialize()
    return jsonify(cupcake=serialized)


@app.route("/api/cupcakes/<int:id>", methods=["PATCH"])
def patch_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)  
    cupcake.size = request.json.get('size', cupcake.size)  
    cupcake.rating = request.json.get('rating', cupcake.rating)  
    cupcake.image = request.json.get('image', cupcake.image)
    db.session.commit()  
    return jsonify(cupcake=cupcake.serialize())

@app.route("/api/cupcakes/<int:id>", methods=["DELETE"])
def delete_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify({"message": "Deleted"})

@app.route("/")
def home():
    """show static page to perform requests via AJAX (Axios)"""
    return render_template("home.html")