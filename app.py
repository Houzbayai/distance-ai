from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

GOOGLE_MAPS_API_KEY = "AIzaSyA2v3Y8xRWq-3F_ukFuKct8qKlXw1EF86A"  # 🔁 Replace with your real key

@app.route("/get-distance", methods=["GET"])
def get_distance():
    from_lat = request.args.get("from_lat")
    from_lng = request.args.get("from_lng")
    to_lat = request.args.get("to_lat")
    to_lng = request.args.get("to_lng")

    if not all([from_lat, from_lng, to_lat, to_lng]):
        return jsonify({"error": "Missing parameters"}), 400

    url = (
        f"https://maps.googleapis.com/maps/api/distancematrix/json"
        f"?origins={from_lat},{from_lng}&destinations={to_lat},{to_lng}"
        f"&key={GOOGLE_MAPS_API_KEY}"
    )

    response = requests.get(url)
    data = response.json()

    if data["status"] != "OK":
        return jsonify({"error": "Google API error", "details": data}), 500

    try:
        element = data["rows"][0]["elements"][0]
        if element["status"] == "OK":
            distance_text = element["distance"]["text"]
            distance_value = element["distance"]["value"] / 1000  # meters to km
            return jsonify({
                "distance_km": round(distance_value, 1),
                "distance_text": distance_text
            })
        else:
            return jsonify({"error": "No route found"}), 404
    except Exception as e:
        return jsonify({"error": "Parsing error", "message": str(e)}), 500

# Start server
if __name__ == "__main__":
    app.run(debug=True, port=5000)

