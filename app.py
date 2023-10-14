from flask import Flask,render_template,redirect,request
import jinja2 
from model import predictor
import warnings
warnings.filterwarnings('ignore')
app = Flask(__name__)

result = 2
start = False
@app.route("/")
def Home():
    return render_template("index.html",result=result,start=start)
    
@app.route("/msg_process/", methods=['POST','GET'])
def Process():
    if request.method == 'POST':
        SMS = request.form.get('exampleFormControlTextarea1')
        global result
        result = predictor(str(SMS))
        global start
        start = True
        return redirect('/')
    else:
        result = 2
        start = False
        return render_template('index.html',result=2,start=False)

if __name__ == "__main__":
    app.run(debug=True,port=8000)