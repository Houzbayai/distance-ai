from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

GOOGLE_API_KEY = "AIzaSyA2v3Y8xRWq-3F_ukFuKct8qKlXw1EF86A"

@app.route("/get-distance", methods=["POST"])
def get_distance():
    data = request.get_json()
    user_lat = data.get("userLat")
    user_lng = data.get("userLng")
    property_lat = data.get("propertyLat")
    property_lng = data.get("propertyLng")

    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={user_lat},{user_lng}&destinations={property_lat},{property_lng}&key={GOOGLE_API_KEY}"
    res = requests.get(url)
    info = res.json()

    if info["status"] == "OK" and info["rows"][0]["elements"][0]["status"] == "OK":
        distance = info["rows"][0]["elements"][0]["distance"]["text"]
        duration = info["rows"][0]["elements"][0]["duration"]["text"]
        return jsonify({"distance": distance, "duration": duration})
    else:
        return jsonify({"error": "Unable to fetch distance"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

