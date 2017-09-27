from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
from flask.ext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '12345'
app.config['MYSQL_DATABASE_DB'] = 'ItemListDb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

# Initalize the mySql instance
mysql.init_app(app)

# we later add the api routes
api = Api(app)

# Creation of our Class / Method
class CreateUser(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()

            # Help = error message when a type error is raised while parsing it
            parser.add_argument('email', type=str, help='Email address to create user')
            parser.add_argument('password', type=str, help='Password to create user')
            args = parser.parse_args()

            # Variables referencing the dict ['email'] or ['password']
            _userEmail = args['email']
            _userPassword = args['password']

            conn = mysql.connect()
            # In computer science and technology, a database cursor is a control structure
            # that enables traversal over the records in a database.
            # Cursors facilitate subsequent processing in conjunction with the traversal,
            # such as retrieval, addition and removal of database records. The database cursor characteristic
            # of traversal makes cursors akin to the programming language concept of iterator.

            cursor = conn.cursor()

            # This calls the stored procedures.
            cursor.callproc('spCreateUser', (_userEmail, _userPassword))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return {'StatusCode': '200', 'Message': 'User creation success'}
            else:
                return {'StatusCode': '1000', 'Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}

api.add_resource(CreateUser, '/CreateUser')

if __name__ == '__main__':
    app.run(debug=True)