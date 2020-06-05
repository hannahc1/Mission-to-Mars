from flask import Flask, render_template
# Use PyMongo to interact with the Mongo db.
from flask_pymongo import PyMongo
# Convert from Jupyter notebook to Python.
import scraping
# Set up Flask.
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Set up Flask routes.
@app.route("/") # The homepage
def index():
# Find mars collection in db
    mars = mongo.db.mars.find_one()
    # Return HTML template using index.html file using mars collection.
    return render_template("index.html", mars=mars)

# Set up scraping route
@app.route("/scrape")
def scrape():
    # Assign a new variable to point to the mongo db
    mars = mongo.db.mars
    # Use scraping.py
    mars_data = scraping.scrape_all()
    # Update the DB and create a new doc if one doesn't exist already.
    mars.update({}, mars_data, upsert=True)
    return "Scraping Successful!"


if __name__ == "__main__":
    app.run(debug=True)