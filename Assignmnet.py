from pymongo import MongoClient
from flask import Flask,request,jsonify

main = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
database = client["movies_db"]
movie_collection = database["movies"]

@main.route("/movies",methods = ["POST"])
def create_movie():
    data = request.json
    movie = {
        "name": data["name"],
        "img": data["img"],
        "summary": data["summary"]
    }
    movie_collection.insert_one(movie)
    return jsonify({"message": "Movie added successfully"})

@main.route("/movies", methods=["GET"])
def get_movies():
    movies = list(movie_collection.find({},{"_id":0}))
    return jsonify(movies)

@main.route("/movies/<movie_name>",methods = ["PUT"])
def update_movie(movie_name):
    data = request.json
    movie_collection.update_one({"name": movie_name},{"$set": data})
    return jsonify({"message": "Movie updated successfully"})

@main.route("/movies/<movie_name>", methods=["DELETE"])
def delete_movie(movie_name):
    movie_collection.delete_one({"name": movie_name})
    return jsonify({"message": "Movie deleted successfully"})

if __name__ == "__main__":
    main.run(debug=True)