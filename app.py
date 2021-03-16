from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
from pprint import pprint

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
# Create connection variable
#conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
#client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
#db = client.mars_db

# Drops collection if available to remove duplicates
#db.mars.drop()



# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    # Store the entire team collection in a list
    #marslist = list(db.mars.find())
    #print(marslist)

    # Find one record of data from the mongo database
    marslist = mongo.db.collection.find_one()
    #print(marslist["featured_img_url"])
    #pprint(marslist)
    # Return the template with the teams list passed in
    return render_template('index.html', marslist=marslist)
    #table_html = table_df.to_html(classes='data', header="true", index="false")
    # Find one record of data from the mongo database
    #destination_data = mongo.db.collection.find_one()



# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
