To make Python work as a multi-user environment where each call to the Python script does not freeze the server or block other requests, you need to implement concurrency or parallelism. Here’s a step-by-step guide to achieving this:

### 1. **Use a Python Web Framework**
Instead of calling Python scripts directly from Apache, use a Python web framework like **Flask** or **Django**. These frameworks are designed to handle web requests and can work asynchronously or with multi-threading.

### 2. **Set Up a WSGI Server**
WSGI (Web Server Gateway Interface) servers like **Gunicorn** or **uWSGI** can manage multiple worker processes. They can be configured to handle multiple requests simultaneously, ensuring that one long-running request doesn’t block others.

### 3. **Enable Multi-Processing or Multi-Threading**
- **Multi-Processing:** You can run multiple instances (processes) of the Python application. Each process can handle a separate request. WSGI servers like Gunicorn can be configured to run several worker processes.
  
- **Multi-Threading:** You can use threads within a single process to handle multiple requests. This can be done using Python’s `threading` module, but be cautious about Python’s Global Interpreter Lock (GIL), which can limit the effectiveness of threading.

### 4. **Use Asynchronous Code**
For IO-bound tasks, consider using asynchronous programming with `asyncio` or frameworks that support it, like **FastAPI** or **Django Channels**. Asynchronous code can handle multiple tasks concurrently without requiring multiple threads or processes.

### 5. **Configure Apache with mod_wsgi**
If you prefer to use Apache directly:
- Install **mod_wsgi**, which is an Apache module that provides a WSGI compliant interface for hosting Python-based web applications under Apache.
- Configure mod_wsgi to use **daemon mode** with multiple threads and/or processes to handle multiple requests concurrently.

### 6. **Queue Long-Running Tasks**
For tasks that take a long time to complete:
- Use a task queue system like **Celery** or **RQ (Redis Queue)**. These allow you to offload long-running tasks to separate worker processes or servers.
- Apache can quickly return a response to the client while the task runs in the background.

### 7. **Example Configuration Using Flask and Gunicorn**
Here's a basic example of setting up a Flask application with Gunicorn to handle multiple requests concurrently:

**Install Flask and Gunicorn:**
```bash
pip install flask gunicorn
```

**Create a simple Flask app (`app.py`):**
```python
from flask import Flask, request, jsonify
import time

app = Flask(__name__)

@app.route('/long_task', methods=['GET'])
def long_task():
    time.sleep(10)  # Simulates a long-running task
    return jsonify({"message": "Task completed!"})

if __name__ == "__main__":
    app.run()
```

**Run the Flask app with Gunicorn:**
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```
- `-w 4` specifies the number of worker processes. Adjust this based on your server’s CPU cores and load.
- `-b 0.0.0.0:8000` binds the server to all network interfaces on port 8000.

### 8. **Configure Apache to Proxy Requests to Gunicorn**
Modify your Apache configuration to forward requests to the Gunicorn server:

```apache
<VirtualHost *:80>
    ServerName example.com

    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/
</VirtualHost>
```

**Enable the proxy modules and restart Apache:**
```bash
a2enmod proxy
a2enmod proxy_http
systemctl restart apache2
```

### Summary
By using a WSGI server like Gunicorn or uWSGI with Flask or Django, and configuring Apache to proxy requests to it, you can ensure your Python server handles multiple requests without freezing. Additionally, offloading long-running tasks to a task queue can improve responsiveness and scalability.