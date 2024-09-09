import sys
import os
from flask import Flask, request, jsonify
import time
import Main06 as apriori

app = Flask(__name__)

# @app.route('/long_task', methods=['GET'])
# def long_task():
#     time.sleep(10)  # Simulates a long-running task
#     return jsonify({"message": "Task completed!"})

# if __name__ == "__main__":
#     app.run()


app = Flask(__name__)

@app.route('/webApriori', methods=['POST'])
def webApriori():
    
    a = request.form.get('a')
    b = request.form.get('b')
    print(f"Received: a={a}, b={b}")
    time.sleep(8)  # Simulates a long-running task
    # return jsonify({"result": "Task completed!"})
    return f"Task completed! Received a={a}, b={b}"

@app.route('/run-script', methods=['POST'])
def run_script():
    # Perform some long-running task
    # result = some_long_running_function()
    # return jsonify({"result": result})
    a = request.form.get('a')
    b = request.form.get('b')
    print(f"Received: a={a}, b={b}")
    time.sleep(8)  # Simulates a long-running task
    # return jsonify({"result": "Task completed!"})
    return f"Task completed! Received a={a}, b={b}"

@app.route('/run-script1', methods=['POST'])
def run_script1():
    # Perform some long-running task
    # result = some_long_running_function()
    # return jsonify({"result": result})
    a = request.form.get('a')
    b = request.form.get('b')
    print(f"Received: a={a}, b={b}")
    time.sleep(2)  # Simulates a long-running task
    # return jsonify({"result": "Task completed!"})
    return f"Task completed! Received a={b}, b={a}"

@app.route('/retrieveRules', methods=['POST'])
def retrieveRules():

    identity = request.form.get('identity')
    filename = request.form.get('filename')
    isPublic = request.form.get('isPublic')
    if isPublic is None:
        return ("An error occurred: isPublic not given!") 
    else:
        isPublic=int(isPublic)
    callType = request.form.get('callType')
    if callType is None:
        callType=0
    arg1     = request.form.get('arg1')
    arg2     = request.form.get('arg2')

    # return(f"identity={identity}, filename={filename}, isPublic={isPublic}, callType={callType}, arg1={arg1}, arg2={arg2}")


    WAInst=apriori.webApriori(identity,filename,isPublic,callType,arg1,arg2)
    # current_directory = os.getcwd()
    # return(f"Current Working Directory: {current_directory}")
    return WAInst.runWebApriori()

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8081)