from flask import render_template
from flask.views import MethodView
import gbmodel

class Index(MethodView):
    def get(self):
        model = gbmodel.get_model()
        groceries = model.select()
        entries = []
        cols = ['product', 'category', 'location', 'description', 'image']

        entries = [dict(\
            product=row[0], \
            category=row[1], \
            location=row[2], \
            description=row[3], \
            image=row[4] \
            ) for row in groceries]
        
        return render_template('index.html', entries=entries)
