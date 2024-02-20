from flask import Flask, request, render_template
from pickle import load
from sklearn.preprocessing import StandardScaler
import joblib
import os

app = Flask(__name__)

model = load(open("/workspaces/Isa-Flask/src/Reg-Lin_5vars.sav", "rb"))

scaler = joblib.load('/workspaces/Isa-Flask/models/scaler_model.joblib')



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

        
        data_for_norm=[[age, bmi,0, sex_n,smoke_n,reg_n]]
        data_norm = scaler.transform(data_for_norm)
        data = [[data_norm[0][4], data_norm[0][0], data_norm[0][1], data_norm[0][3],data_norm[0][5]]]
        
        prediction = str(round(model.predict(data)[0]))
        pred_price = f"\nEl precio de su seguro será de: {prediction} €"
    else:
        pred_price = None
    
    return render_template("index.html", prediction = pred_price)