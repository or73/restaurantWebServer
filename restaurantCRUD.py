import cgi
import re

from BaseHTTPServer import BaseHTTPRequestHandler
from restaurantDB import connect_db, create_restaurant, delete_restaurant, edit_restaurant, read_restaurant

DB_NAME = 'restaurantmenu.db'
DB = connect_db(DB_NAME)

class webServerHandler(BaseHTTPRequestHandler):
    # A DBSession() instance establishes all conversations with the database
    # and represents a "staging zone" for all the objects loaded into the
    # database session object. Any change made against the objects in the
    # session won't be persisted into the database until you call
    # session.commit(). If you're not happy about the changes, you can
    # revert all of them back to the last commit by calling
    # session.rollback()


    def do_GET(self):
        """
            Handler Method
            Indicates what code to execute based on the type
                of HTTP request that is sent to the server
        """
        try:
            if self.path.endswith('/delete'):
                restaurant_name = self.path.split('/')[2]
                restaurantNamePath = (restaurant_name).replace('%20', ' ')
                restaurantNamePath = (restaurantNamePath).replace('%27', "'")
                print('\n------- QUERY - GET /restaurants/' + restaurant_name + '/delete')
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                message = ''
                message += '<html><body>'
                message += '<h1>Are you sure you want do delete %s?' % restaurantNamePath
                message += '<form method="POST" enctype="multipart/form-data" action="/restaurants/%s/delete">' % restaurant_name
                message += '<input type="submit" value="Delete"/>'
                message += '</form></body></html>'
                self.wfile.write(message)
                print('------- END QUERY - GET /restaurants/<some restaurant name>/delete\n')
                return
            if self.path.endswith('/edit'):
                restaurant_name = self.path.split('/')[2]
                restaurantNamePath = (restaurant_name).replace('%20', ' ')
                restaurantNamePath = (restaurantNamePath).replace('%27', "'")
                print('\n------- QUERY - GET /restaurants/' + restaurant_name + '/edit')

                restaurant_edit = read_restaurant(DB, 'one', restaurantNamePath)

                if restaurant_edit:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    message = ''
                    message += '<html><body>'
                    message += ('<h1>' + restaurant_edit.name + '</h1>')
                    message += '<form method="POST" enctype="multipart/form-data" action="/restaurants/%s/edit">' % restaurantNamePath
                    message += '<input name="newRestaurantName" type="text" placeholder="%s"/>' % restaurant_edit.name
                    message += '<input type="submit" value="Rename"/>'
                    message += '</form></body></html>'
                    self.wfile.write(message)
                print('------- END QUERY - GET /restaurants/<some restaurant name>/edit\n')
                return
            if self.path.endswith('/restaurants'):
                print('\n------- QUERY - GET /restaurants')
                """
                Read all restaurants from DB
                """
                restaurants = read_restaurant(DB)
                print('--------------- All Restaurants:')
                print('|----> %s' % type(restaurants))
                print(restaurants)

                for restaurant in restaurants:
                    print(restaurant)

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                message = ''
                message += '<html><head><script>'
                message += '\nfunction edit_restaurant(restaurant) {'
                message += 'alert("Restaurant to edit: ", restaurant)'
                message += '}'
                message += '\nfunction del_restaurant(restaurant) {'
                message += 'alert("Restaurant to delete: ", restaurant)'
                message += '}'
                message += '</script></head><body>'
                message += '<h1>Restaurants</h1>'
                message += '<ul>'
                for restaurant in restaurants:
                    restaurant_name = ((re.sub('[^A-Za-z0-9\' ]+', '', restaurant)).replace(' ', '%20')).replace("'", '%27')
                    message += '<li>'
                    message += restaurant
                    message += '\t\t<a href="/restaurants/%s/edit">Edit</a>\t' % restaurant_name
                    message += '<a href="/restaurants/%s/delete">Delete</a>' % restaurant_name
                    message += '</li>'
                message += '</ul>'
                message += '</body></html>'
                self.wfile.write(message)
                print('------- END QUERY - GET /restaurants\n')
                return

            if self.path.endswith('/restaurants/new'):
                print('\n------- QUERY - GET /restaurants/new')
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                message = ''
                message += '<html>'
                message += '<body>'
                message += '<h1>Create a New Restaurant</h1>'
                message += '<form method="POST" enctype="multipart/form-data" action="/restaurants/new">'
                message += '<input name="newRestaurantName" type="text" placeholder="New Restaurant Name"/>'
                message += '<input type="submit" value="Submit"/>'
                message += '</form>'
                message += '</body>'
                message += '</html>'
                self.wfile.write(message)
                print('------- END QUERY - GET /restaurants/new\n')
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith('/delete'):
                print('\n------- QUERY - POST /restaurants/delete')
                ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    restaurant_name = self.path.split('/')[2]
                    restaurantNamePath = (restaurant_name).replace('%20', ' ')
                    restaurantNamePath = (restaurantNamePath).replace('%27', "'")
                    print('messagecontent: ', messagecontent)
                    print('restaurantNamePath: ', restaurantNamePath)
                    delete_restaurant_query = delete_restaurant(DB, restaurantNamePath)
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                print('------- END QUERY - POST /restaurants/delete\n')

            if self.path.endswith('/edit'):
                print('\n------- QUERY - POST /restaurants/edit')
                ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    restaurant_name = self.path.split('/')[2]
                    restaurantNamePath = (restaurant_name).replace('%20', ' ')
                    restaurantNamePath = (restaurantNamePath).replace('%27', "'")
                    edit_restaurant_query = edit_restaurant(DB, restaurantNamePath, messagecontent[0])

                    if edit_restaurant_query:
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()
                    else:
                        self.send_error(404, 'Operation not available: %s' % self.path)
                print('------- END QUERY - POST /restaurants/edit\n')

            if self.path.endswith('/restaurants/new'):
                print('\n------- QUERY - POST /restaurants/new')
                ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    create_restaurant(DB, messagecontent[0])
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                print('------- END QUERY - GET /restaurants/new\n')
        except:
            pass
