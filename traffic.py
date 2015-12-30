import tornado.httpserver
import tornado.ioloop
import tornado.websocket
import tornado.web
import tornado.escape
import tornado.options

class ReportTrafficHandler(tornado.web.RequestHandler):
    #code
    def post(self):
        request_body = tornado.escape.json_decode(self.request.body)
        area_name = request_body['area']
        if area_name not in traffic_list:
            traffic_list.append(area_name)
        for client in client_list:
            client.write_message({"traffic_add":area_name})
        print(traffic_list)
        
class RemoveHandler(tornado.web.RequestHandler):
    def post(self):
        request_body = tornado.escape.json_decode(self.request.body)
        area_name = request_body['area']
        if area_name in traffic_list:
            traffic_list.remove(area_name)
        for client in client_list:
            client.write_message({"traffic_remove":area_name})
        print(traffic_list)
    


client_list = [] #Client List
traffic_list = []

class TrafficSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True
    
    def open(self):
        print("New Client")
        for area in traffic_list:
            self.write_message({"traffic_add":area})
        client_list.append(self)
    def on_message(self, msg):
        pass
    def on_close(self):
        client_list.remove(self)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/report", ReportTrafficHandler), 
            (r"/trafficsock", TrafficSocketHandler),
            (r"/remove", RemoveHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()