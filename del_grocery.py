from flask import redirect, request, url_for, render_template
from flask.views import MethodView
from datetime import date
import gbmodel

class DeleteGrocery(MethodView):
    def get(self):
        return render_template('del_grocery.html', todayDate=date.today())

    def post(self):
        """
        Accepts POST requests, and processes the form;
        Redirect to index when completed.
        """
        model = gbmodel.get_model()

        model.delete(\
            request.form['product'], \
            )
        return redirect(url_for('index'))


