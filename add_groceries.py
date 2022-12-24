from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import gbmodel
from api import kroger as kapi
from api.cloudVision import detect_handwriting_gs as writing_api


class AddGroceries(MethodView):
    def get(self):
        return render_template('add_groceries.html')


    def get_many_product_info(self, *products, category='none', zipcode=97216, radius=1):
        import os

        client_id = os.environ["CLIENT_ID"]
        client_secret = os.environ["CLIENT_SECRET"]

        bearer = kapi.get_bearer(client_id, client_secret)
        
        """
        TODO: Indicate which store we are searching at.
        TODO: enable user to choose a different Kroger store.
        Can adapt this code from my api code:

        print(f"Searching for {product} at the {location['name']} store id# {location['locationId']} located at:")
        for key in location['address']:
            print(f"{location['address'][key]}")
        """

        locations = kapi.get_location_near(bearer, str(zipcode), radius)
        store_id = kapi.choose_location(locations, 0) 

        if len(products) == 0:
            products = ('bananas')

        # multi part
        new_products = []
        for product in products:
            product = product.lower()
            #TODO get a list of options, display to user, let them choose.

            product_json = kapi.get_products(bearer, str(store_id), product)
            product_data = product_json['data'][0]

            # Can pull more items out of response if desired.
            if category == 'none':
                category = product_data['categories'][0]
            aisle = product_data['aisleLocations'][0]

            location = aisle['number'] + ', ' + aisle['description'].lower()
            description = product_data['description']

            # TODO select only front image.
            biggest_pic_id = len(product_data['images'][0]['sizes'])
            if biggest_pic_id >= 3:
                image = product_data['images'][0]['sizes'][2]['url']
            else:
                image = product_data['images'][0]['sizes'][biggest_pic_id]['url']

            new_products.append({'product': product, 'category': category, 'location': location, 'description': description, 'image': image})
        return new_products



    def post(self):
        """
        Accepts POST requests, and processes the form;
        Redirect to index when completed.
        """
        def send_to_datastore(product_details):
            for detail in product_details:
                model.insert(\
                    detail['product'], \
                    detail['category'], \
                    detail['location'], \
                    detail['description'], \
                    detail['image'] \
                    )


        def already_in_DB(product):
            my_products = model.filtered_select('product', product)
            return len(my_products) > 0


        model = gbmodel.get_model()

        # multi part
        if 'product' in request.form and len(request.form['product']) > 0:
            product = request.form['product']

            # First check if it is already in the DB
            # It is faster to query the DB than to call the API and overwrite the product.
            if not already_in_DB(product): 
                product_details = self.get_many_product_info(product)
                send_to_datastore(product_details)

        elif 'bucket' in request.form and len(request.form['bucket']) > 0:
            file_name = ''
            if 'fileName' in request.form and len(request.form['fileName']) > 0:
                file_name = request.form['fileName']
            bucket_name = request.form['bucket']

            uri = 'gs://' + bucket_name + '/' + file_name
            new_groceries = writing_api.detect_document_uri(uri)
            new_groceries = new_groceries.split("\n")
            temp = []

            # Clear out short typos from vision.
            for banana in new_groceries:
                if len(banana) >= 3:
                    temp.append(banana)
            new_groceries = temp

            # TODO handle error in get_many_product_info if no data returned
            # TODO is there a way to send a list to the api so we don't call once for each product?
            for grocery in new_groceries:
                if grocery != 'Groceries':
                    if not already_in_DB(grocery):
                        product_details = self.get_many_product_info(grocery)
                        send_to_datastore(product_details)

        return redirect(url_for('index'))
