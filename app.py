import os
from flask import Flask
from flask import render_template, send_from_directory, request
from use import classify

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def twss():
    if request.method == 'POST':
        return twss_classify(request.values['string'])
    else:
        return render_template("twss.html")

@app.route('/<path:name>')
def hello(name):
    return send_from_directory(app.static_folder,name)

def twss_classify(text):
    sentences = text.split('.')
    output = [(s,classify(s)) for s in sentences]
    print output
    return render_template('twss.html',output=output)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port,debug=True)
