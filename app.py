from flask import Flask, request, render_template
from pickle import load

app = Flask(__name__)
model = load(open("C:\\Users\\isabel\\Desktop\\Isa-Flask\\models\\Reg-Lin_5vars.sav", "rb"))


@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        
        age = float(request.form["age"])
        smoke = request.form["smoke"]
        sex = request.form["sex"]
        reg = request.form["reg"]
        kg = float(request.form["kg"])
        cm = float(request.form["cm"])

        smoke_n= 0 if smoke == 'yes' else 1
        sex_n= 0 if sex== 'female' else 1

        if reg == 'southwest':
            reg_n = 0
        elif reg == 'southeast':
            reg_n = 1
        elif reg == 'northwest':
            reg_n = 2
        else:
            reg_n = 3

        bmi=kg/((cm/100)**2)

        
        data = [[smoke_n, age, bmi, sex_n,reg_n]]
        
        prediction = str(round(model.predict(data)[0]/10))
        pred_price = f"\nEl precio de su seguro será de: {prediction} €"
    else:
        pred_price = None
    
    return render_template("index.html", prediction = pred_price)