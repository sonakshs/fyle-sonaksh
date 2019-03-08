from flask import Flask, request, jsonify, render_template, json
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
                bank = Banks.query.filter_by(name=name.upper()).first()
                if not bank:
                    return "Invalid request"
                bank_id = bank.id
                branches = Branches.query.filter_by(bank_id=bank_id, city=city.upper()).all()
                if len(branches) > 0:
                    result = ([branch.to_dict() for branch in branches])
                else:
                    result = "No data found"
            except Exception as e:
                result = (str(e))
        elif ifsc:
            from models.branches import Branches
            try:
                branch = Branches.query.filter_by(ifsc=ifsc.upper()).first()
                if branch:
                    result = [branch.to_dict()]
                else:
                    result = "No data found"
            except Exception as e:
                result = (str(e))
        return render_template('index.html', result=json.dumps(result, sort_keys=False, indent=2))
    return render_template("index.html")

if __name__ == '__main__':
    app.run()