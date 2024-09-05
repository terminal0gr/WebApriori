from flask import Flask, request, jsonify
import time
import Main05

# app = Flask(__name__)

# @app.route('/long_task', methods=['GET'])
# def long_task():
#     time.sleep(10)  # Simulates a long-running task
#     return jsonify({"message": "Task completed!"})

# if __name__ == "__main__":
#     app.run()


app = Flask(__name__)

@app.route('/run-script', methods=['POST'])
def run_script():
    # Perform some long-running task
    # result = some_long_running_function()
    # return jsonify({"result": result})
    a = request.form.get('a')
    b = request.form.get('b')
    print(f"Received: a={a}, b={b}")
    time.sleep(6)  # Simulates a long-running task
    # return jsonify({"result": "Task completed!"})
    return f"Task completed! Received a={a}, b={b}"

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8081)