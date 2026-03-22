#!/usr/bin/python3

from flask import Flask, request
import requests
import time

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return '''
<html>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <body>
        <h2>Paste Python code</h2>
		<form method="POST"> 
		  <textarea name="code" type="text" rows="10" cols="120"></textarea></br>
		  <button type="submit" name="submit">Submit</button>
		</form>
    </body>
</html>'''
    
@app.route('/', methods=["POST"])
def runPythonCode():
    code = request.form.get('code')
    start = time.perf_counter()
    exec(code)
    duration = time.perf_counter() - start
    return (
        '<html>\n'
        '    <meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '    <body>\n'
       f'        <p>Code took {duration:0.1f} seconds</p>\n'
        '        <a href="/">Start again</a>\n'
        '    </body>\n'
        '</html>'
    )

if __name__ == '__main__':
    # yes I know app.run() is the old way of running Flask, but it fits in one file
    # host=0.0.0.0 is to accept all IP addresses, else defaults to just localhost 
    # add port=xx to change port from 5000.  80 will require sudo
    app.run(host='0.0.0.0') 
