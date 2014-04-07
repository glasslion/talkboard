import logging
import os.path
import re
import subprocess

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket


def get_wifi_ip():
    p = subprocess.Popen('ipconfig', shell = True, stdout = subprocess.PIPE)
    p.wait()
    stdout = p.stdout.read()
    return re.findall(r'IPv4.* (192\.168\.1.\d+)',stdout)[0]

WIFI_IP = get_wifi_ip()
PORT = 15801


def send_message(message):
    for handler in ChatSocketHandler.socket_handlers:
        try:
            handler.write_message(message)
        except:
            logging.error('Error sending message', exc_info=True)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html', port=PORT, wifi_ip=WIFI_IP)


class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    socket_handlers = set()

    def open(self):
        ChatSocketHandler.socket_handlers.add(self)

    def on_close(self):
        ChatSocketHandler.socket_handlers.remove(self)
        

    def on_message(self, message):
        send_message(message)

def main():
    print "Open this url: http://%s:%s" % (WIFI_IP, PORT)

    settings = {
        'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
        'static_path': os.path.join(os.path.dirname(__file__), 'static')
    }
    application = tornado.web.Application([
        ('/', MainHandler),
        ('/new-msg/socket', ChatSocketHandler)
    ], **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
