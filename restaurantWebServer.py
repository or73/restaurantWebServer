from BaseHTTPServer import HTTPServer
from restaurantCRUD import webServerHandler


def main():
    """
        Main Method
    """
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print("Web Server running... localhost:%s/restaurants" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print(" ^C entered, stopping web server....")
        server.socket.close()


if __name__ == '__main__':
    main()
