from flask import Flask, request, jsonify
import time
import Main06

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

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8081)