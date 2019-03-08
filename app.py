from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route("/", methods=['GET','POST'])
def hello():
    if request.method == 'POST':
        city = request.form.get('city')
        name = request.form.get('name')
        ifsc = request.form.get('ifsc')
        result = {}
        if city and name:
            from models.branches import Branches
            from models.banks import Banks
            try:
                bank = Banks.query.filter_by(name=name).first()
                if not bank:
                    return "Invalid request"
                bank_id = bank.id
                branches = Branches.query.filter_by(bank_id=bank_id, city=city)
                if branches:
                    result = ([branch.to_dict() for branch in branches])
                else:
                    result = "No data found"
            except Exception as e:
                result = (str(e))
        elif ifsc:
            from models.branches import Branches
            try:
                branch = Branches.query.filter_by(ifsc=ifsc).first()
                if branch:
                    result = branch.to_dict()
                else:
                    result = "No data found"
            except Exception as e:
                result = (str(e))
        return render_template('index.html', result=result)

    return render_template("index.html")


@app.route("/getall")
def get_all():
    from models.branches import Branches
    try:
        branches = Branches.query.first()
        return jsonify(branches.to_dict())
        # return jsonify([branch.to_dict() for branch in branches])
    except Exception as e:
        return(str(e))


@app.route("/getByIfsc/<ifsc>")
def get_branch_by_ifsc(ifsc):
    from models.branches import Branches
    try:
        branch = Branches.query.filter_by(ifsc=ifsc).first()
        if branch:
            return jsonify(branch.to_dict())
        return {}
    except Exception as e:
        return(str(e))


@app.route("/branches")
def get_bank_branches():
    from models.branches import Branches
    from models.banks import Banks
    name = request.args.get('name')
    city = request.args.get('city')
    try:
        bank = Banks.query.filter_by(name=name).first()
        if not bank:
            return "Invalid request"
        bank_id = bank.id
        branches = Branches.query.filter_by(bank_id=bank_id, city=city)
        return jsonify([branch.to_dict() for branch in branches])
    except Exception as e:
        return(str(e))


if __name__ == '__main__':
    app.run()