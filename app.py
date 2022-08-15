import numpy as np
import pandas as pd
from flask import Flask, request,render_template, make_response
import pickle
from datetime import datetime
import csv
import io
from io import StringIO
from sklearn.ensemble import RandomForestClassifier




app = Flask(__name__)

model = pickle.load(open('modele_randomforest.pkl', 'rb')) #import du model

def transform(text_file_contents):
    return text_file_contents.replace("=",",")


@app.context_processor 
def inject_now():
    return {"now":datetime.now()}

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/predict')
def acceuil():
    return render_template('prediction.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    Pour le rendu des résultats sur l'interface graphique HTML
    '''
    int_features = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = round(prediction[0], 2)
    if output == 0:
        return render_template('prediction.html', prediction_text= " Il n'y a pas de suspicion de fraude.")
    else:
        return render_template('prediction.html', prediction_text= " Attention, il y'a suspicion de fraude.")
   
@app.route("/chargement")
def acceuil_chargement():
    return render_template("chargement.html")

@app.route('/chargement',methods=["POST"])
def chargement():
    f=request.files("fichier_csv")
    if not f:
        return "Pas de fichier"
    
    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)
    print(csv_input)
    for row in csv_input:
        print(row)
        
    stream.seek(0)
    result = transform(stream.read())
    
    df=pd.read_csv(StringIO(result))
    
    #Prediction
    df["Prediction"] = model.predict(df)
    
    response=make_response(df.to_csv())
    response.headers["Content-Disposition"]="attachement; filename=result.csv"
    return response

    #return render_template("chargement.html")
    
   

@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"),404



if __name__ == "__main__":
    
    app.run()
    
    
    
    
    
        