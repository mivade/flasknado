"""Flasknado! - A simple example of using Flask and Tornado
together.

"""

from __future__ import print_function
from flask import Flask, render_template
from tornado.wsgi import WSGIContainer
from tornado.web import Application, FallbackHandler
from tornado.websocket import WebSocketHandler
from tornado.ioloop import IOLoop

class WebSocket(WebSocketHandler):
    def open(self):
        print("Socket opened.")

    def on_message(self, message):
        self.write_message("Received: " + message)
        print("Received message: " + message)

    def on_close(self):
        print("Socket closed.")

app = Flask('flasknado')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    container = WSGIContainer(app)
    server = Application([
        (r'/websocket/', WebSocket),
        (r'.*', FallbackHandler, dict(fallback=container))
    ])
    server.listen(8080)
    IOLoop.instance().start()
