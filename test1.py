from flask import Flask,render_template,request
app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        #Fetch form data
        userDetails = request.form
        name=userDetails['name']
        email=userDetails['email']
        with open('text1.txt','a') as f:
            f.write("".join(name))
    return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True,host='localhost',port=5000)
