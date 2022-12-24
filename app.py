"""
A simple guestbook flask app.
"""
import flask
from flask.views import MethodView
from index import Index
from add_groceries import AddGroceries
from del_grocery import DeleteGrocery


app = flask.Flask(__name__)       # our Flask app

app.add_url_rule('/',
                 view_func=Index.as_view('index'),
                 methods=["GET"])

app.add_url_rule('/add_groceries',
                 view_func=AddGroceries.as_view('add_groceries'),
                 methods=['GET', 'POST'])

app.add_url_rule('/del_grocery',
                 view_func=DeleteGrocery.as_view('del_grocery'),
                 methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
