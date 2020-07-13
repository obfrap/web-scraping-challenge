# import Flask and pymongo
from flask import Flask, render_template
from flask_pymongo import PyMongo

# import scrape_mars.py
import scrape_mars


#  Create an app, being sure to pass __name__
app = Flask(__name__)


# Create connection variable to load in
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_info")


#  Define app route
@app.route("/")
def index(): 
    mars = mongo.db.collection.find_one()
    return render_template("index.html", mars_data=mars)


#  Define what to do when a user hits the /scrape route
@app.route("/scrape")
def scrape():
    mars=mongo.db.collection
    mars_data = scrape_mars.scrape()
    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)
   
    
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
