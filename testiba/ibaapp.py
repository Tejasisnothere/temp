from flask import Flask, jsonify, request, render_template
import random
import hashlib
app = Flask(__name__)

@app.route("/")
def get_home_page():
    return render_template("home.html")
@app.route('/get-images', methods=['GET'])
def get_images():
    gen_imgs = generate_fixed_image_links(9)
    return jsonify({"images": gen_imgs})

@app.route('/submit-order', methods=['POST'])
def submit_order():
    data = request.json
    print("Clicked Order:", data["order"])
    return jsonify({"message": "Order received"}), 200

def generate_fixed_image_links(n):
    links = []
    for _ in range(n):
        random_number = random.randint(1, 10000)  # Generate a random number
        unique_hash = hashlib.md5(str(random_number).encode()).hexdigest()[:8]  # Create a hash
        fixed_url = f"https://picsum.photos/seed/{unique_hash}/200"  # Use seed-based URL
        links.append(fixed_url)
    return links


if __name__ == '__main__':
    app.run(debug=True)
