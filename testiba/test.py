import random
import hashlib

# Function to generate unique but consistent image links
def generate_fixed_image_links(n):
    links = []
    for _ in range(n):
        random_number = random.randint(1, 10000)  # Generate a random number
        unique_hash = hashlib.md5(str(random_number).encode()).hexdigest()[:8]  # Create a hash
        fixed_url = f"https://picsum.photos/seed/{unique_hash}/200"  # Use seed-based URL
        links.append(fixed_url)
    return links

# Generate and store in a list
image_links = generate_fixed_image_links(5)  # Change '5' for more images

# Print the stored links
print("Stored Image Links:", image_links)
