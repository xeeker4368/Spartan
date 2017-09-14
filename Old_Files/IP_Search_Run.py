from flask import request, redirect, Flask
app = Flask(__name__)

@app.route('/')
@app.route('/results', methods = ['POST'])
def Blacklist_Search_Post ():
    IP =request.form['IP']
    print "You searched IP %s " % (IP)
    return redirect('/')

app.run(debug=True)