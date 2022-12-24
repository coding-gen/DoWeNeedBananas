#! /usr/bin/python3

"""
DoWeNeedBananas
Author: Genevieve LaLonde
email: sgl@pdx.edu

A shopping list helper. Lists the product aisle location in the selected store.

See Kroger API docs:
https://developer.kroger.com/
https://developer.kroger.com/reference/#tag/Locations
https://developer.kroger.com/reference/#tag/Products
"""

import requests
import argparse
import os

def getArgs():
	parser = argparse.ArgumentParser(description='Ask the Kroger API where to locate a product within a particular store.')
	parser.add_argument('-o',
		'--output-bearer-token',
		default = False,
		dest='output_bearer',
		action='store_true',
		help=argparse.SUPPRESS)
	parser.add_argument('-p',
		'--product',
		default = 'bananas',
		dest='product',
		type=str,
		help='The grocery item you want to locate.')
	parser.add_argument('-r',
		'--radius',
		default = 1,
		dest='radius',
		type=int,
		help="Radius in miles to search for a store")
	# Todo define more valid options in the help text.
	parser.add_argument('-t',
		'--store-type',
		default = 'Fred',
		dest='store_type',
		type=str,
		help="The type of store name to search for, eg: 'Fred' for Fred Meyer")
	parser.add_argument('-v',
		'--verbose',
		default = False,
		dest='verbose',
		action='store_true',
		help="Zip code of the store where you're shopping")
	parser.add_argument('-z',
		'--zip-code',
		default = 97216,
		dest='zip',
		type=int,
		help="Zip code of the store where you're shopping")

	return parser.parse_args()


def get_bearer(client_id, client_secret, products=True):
	# Obtain authorization to the Kroger API
	url = 'https://api.kroger.com/v1/connect/oauth2/token' 
	data={"grant_type": "client_credentials"}

	# It does no harm to include the product scope when querying for locations, 
	# and is required for products.
	# So I'll just include it in the token all the time.
	# That way I don't need to request the token twice on such short notice when calling both endpoints.
	if products:
		data['scope'] = 'product.compact'

	response = requests.post(
        url,
        data=data,
        auth=(client_id, client_secret),
    )
	return response.json()["access_token"]


def get_location_near(bearer, zipcode, radius):
	# Find locations near the provided zip code.

	url = "https://api.kroger.com/v1/locations"
	headers = {
		"Accept": "application/json",
		"Authorization": f"Bearer {bearer}"
	}
	params = {
	"filter.zipCode.near": zipcode,
	"filter.chain": "Fred",
	"filter.radiusInMiles": radius
	}
	"""
	Other filters:
	"filter.zipCode.near": "97214"
	"filter.latLong.near": "39.306346,-84.278902
	filter.lat.near
	filter.lon.near
	filter.radiusInMiles
	filter.limit 
	"locationId": "01400376" # Hawthorne Fred Meyer: 70100135
	"""

	response = requests.request("GET", url, headers=headers, params=params)
	return response.json()


def choose_location(locations, verbose):
	# This will be replaced in the real app.
	for location in locations['data']:
		if verbose:
			print(f"Searching at the {location['name']} store id# {location['locationId']} located at:")
		for key in location['address']:
			if verbose:
				print(f"{location['address'][key]}")
	return locations['data'][0]['locationId']


def get_products(bearer, store_id, product='bananas', options_count=1):
	# Find aisle locations of the product in the provided store.

	url = "https://api.kroger.com/v1/products"
	headers = {
		'Accept': 'application/json',
		'Authorization': f"Bearer {bearer}"
	}
	params = {
		"filter.locationId": store_id,
		"filter.term": product,
		"filter.limit": options_count,
		'filter.fulfillment': 'ais' # available in store
	}
	"""
	Other filters:
	"filter.brand": "Kroger"
	"filter.term": "milk"
	"filter.term": "fat%20free%20milk"
	"filter.locationId": "01400441"
	"filter.productId": '0001111041700' or '0001111060903'
	'filter.fulfillment': 'ais' # available in store
	filter.limit
	filter.start
	"""

	response = requests.request("GET", url, headers=headers, params=params)
	return response.json()

"""
equivalent curl:

curl -X GET \
  'https://api.kroger.com/v1/products?filter.locationId=01400441&filter.productId=0001111041700&filter.limit=1' \
  -H 'Accept: application/json' \
  -H 'Authorization: Bearer BEARER_HERE'

"""


def choose_product(products):
	# This will be replaced in the real app.
	for product in products['data']:
		print(f"Results for {product}:")
		print(f"{product['description']} is in the {product['categories'][0]} category.")

		# For now this is just taking the first product option.
		# TODO add option button at the end: "did you mean: list of other more granular option names".
		# cache the names and product ids locally so they can be easily retrieved for requerying.

		#print(f"description: {product['aisleLocations'][0]['description']}")
		aisle = product['aisleLocations'][0]
		print(f"It is located in aisle: {aisle['number']}, {aisle['description'].lower()}")
		#print(product['aisleLocations'])

		if 'bayNumber' in product['aisleLocations'][0]:
			print(f"in bay number: {product['aisleLocations'][0]['bayNumber']}")

		if 'side' in product['aisleLocations'][0]:
			side = None
			if product['aisleLocations'][0]['side'] == 'R':
				side = 'right'
			elif product['aisleLocations'][0]['side'] == 'L':
				side = 'left'
			if side:
				print(f"on the {side} side")
		biggest_pic_id = len(product['images'][0]['sizes'])
		if biggest_pic_id >= 3:
			print(f"Here is a picture: {product['images'][0]['sizes'][2]}")
		else:
			print(f"Here is a picture: {product['images'][0]['sizes'][biggest_pic_id]}")

	return products['data'][0]['productId']


if __name__ == "__main__":
	client_id = os.environ["CLIENT_ID"]
	client_secret = os.environ["CLIENT_SECRET"]

	args = getArgs()

	product = args.product
	zipcode = args.zip
	radius = args.radius
	verbose = args.verbose

	bearer = get_bearer(client_id, client_secret)
	if args.output_bearer:
		print(bearer)
	locations = get_location_near(bearer, zipcode, radius)
	store_id = choose_location(locations, product, verbose) 
	products = get_products(bearer, str(store_id), product)
	if verbose:
		product_id = choose_product(products)

"""
# javascript

var settings = {
  "async": true,
  "crossDomain": true,
  "url": "https://api.kroger.com/v1/locations/{{LOCATION_ID}}",
  "method": "GET",
  "headers": {
    "Accept": "application/json",
    "Authorization": "Bearer {{TOKEN}}",
  }
}

$.ajax(settings).done(function (response) {
  console.log(response);
});
"""


	