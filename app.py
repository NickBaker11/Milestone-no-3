import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env  # noqa: F401


app = Flask(__name__)


secret_key = os.environ.get('secret_key')

app.config['MONGO_DBNAME'] = 'dino-index'
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')

mongo = PyMongo(app)


@app.route('/')
@app.route('/index')
def index():
    info = mongo.db.dinoInfo.find_one({"name": "Tyrannosaurus Rex"})
    return render_template('index.html', info=info)


@app.route('/main_page')
def main_page():
    return render_template(
        'main_page.html', dinoInfo=mongo.db.dinoInfo.find())


@app.route('/cretaceous')
def cretaceous():
    return render_template(
        'cretaceous.html', dinoInfo=mongo.db.dinoInfo.find(
            {"time_period": "Cretaceous"}))


@app.route('/jurassic')
def jurassic():
    return render_template(
        'jurassic.html', dinoInfo=mongo.db.dinoInfo.find(
            {"time_period": "Jurassic"}))


@app.route('/triassic')
def triassic():
    return render_template(
        'triassic.html', dinoInfo=mongo.db.dinoInfo.find(
            {"time_period": "Triassic"}))


@app.route('/final_page')
def final_page():
    return render_template(
        'final_page.html', dinoInfo=mongo.db.dinoInfo.find())


@app.route('/add_info', methods=["GET", "POST"])
def add_info():
    if request.method == "POST":
        info = {
            "name": request.form.get("name"),
            "time_period": request.form.get("time_period"),
            "diet": request.form.get("diet"),
            "length": request.form.get("length"),
            "speed": request.form.get("speed"),
            "discovered_in": request.form.get("discovered_in"),
            "extra_information": request.form.get("extra_information")
        }
        mongo.db.dinoInfo.insert_one(info)
        return redirect(url_for("main_page"))

    return render_template('add_info.html', dinoInfo=mongo.db.dinoInfo.find())


@app.route("/edit_info/<info_id>", methods=["GET", "POST"])
def edit_info(info_id):
    info = mongo.db.dinoInfo.find_one({"_id": ObjectId(info_id)})
    return render_template('edit_info.html', info=info)


@app.route('/update_info/<info_id>', methods=["POST"])
def update_info(info_id):
    info = mongo.db.dinoInfo
    info.update({'_id': ObjectId(info_id)},
                {
        'name': request.form.get('name'),
        'time_period': request.form.get('time_period'),
        'diet': request.form.get('diet'),
        'length': request.form.get('length'),
        'speed': request.form.get('speed'),
        'discovered_in': request.form.get('discovered_in'),
        'extra_information': request.form.get('extra_information')
    })
    return redirect(url_for('main_page'))


@app.route('/delete_info/<info_id>')
def delete_info(info_id):
    mongo.db.dinoInfo.remove({'_id': ObjectId(info_id)})
    return redirect(url_for('main_page'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=False)
