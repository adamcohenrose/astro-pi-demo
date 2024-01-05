#!/usr/bin/python3

from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return '''
<html>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <body>
        <h2>Paste Trinket URL</h2>
		<form method="POST">
		  <input name="url" type="text" size="40"></input></br>
		  <button type="submit" name="submit">Submit</button>
		</form>
    </body>
</html>'''

@app.route('/', methods=["POST"])
def getTrinket():
    url = request.form.get('url').rstrip('/') #incase of trailing slash
    r = requests.get(url + '/main.py', allow_redirects=True)    #retrieve main.py
    print(r.text)
    exec(r.text)    #execute main.py
    return '''
<html>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <body>
        <a href="/">All done</a>
    </body>
</html>'''

if __name__ == '__main__':
    # yes I know app.run() is the old way of running Flask, but it fits in one file
    # host=0.0.0.0 is to accept all IP addresses, else defaults to just localhost
    # add port=xx to change port from 5000.  80 will require sudo
    app.run(host='0.0.0.0')
