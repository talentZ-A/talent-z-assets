import wikipediaapi
import requests
import os
import re
from PIL import Image
from io import BytesIO
import json
import time

# Set up Wikipedia API
wiki_wiki = wikipediaapi.Wikipedia(
    language="en",
    user_agent="TalentZ/1.0 (tutoparty0@gmail.com)"
)

def get_actor_image(actor_name):
    """
    Gets the main image URL for an actor using MediaWiki API.
    """
    # Format the actor name for the API query
    query_name = actor_name.replace(" ", "_")
  
    # MediaWiki API endpoint
    url = "https://en.wikipedia.org/w/api.php"
  
    # Parameters for the API request
    params = {
        "action": "query",
        "format": "json",
        "titles": query_name,
        "prop": "pageimages",
        "piprop": "original",
        "formatversion": "2"
    }
  
    try:
        response = requests.get(url, params=params)
        data = response.json()

        # Extract the image URL from the response
        pages = data["query"]["pages"]
        if pages and "original" in pages[0]:
            return pages[0]["original"]["source"]
    except Exception as e:
        print(f"Error fetching image for {actor_name}: {e}")
    
    return None

def download_and_convert_to_png(url, actor_name, output_folder):
    """
    Downloads an image and converts it to PNG format.
    """
    try:
        # Download the image
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to download image for {actor_name}")
            return False

        # Open the image with Pillow
        image = Image.open(BytesIO(response.content))

        # Convert to RGBA if necessary
        if image.mode != 'RGBA':
            image = image.convert('RGBA')

        # Create the output filename
        filename = f"{actor_name.replace(' ', '-').lower()}.png"
        filepath = os.path.join(output_folder, filename)

        # Save as PNG
        image.save(filepath, 'PNG')
        print(f"✅ Successfully downloaded and converted: {filename}")
        return True

    except Exception as e:
        print(f"❌ Error processing {actor_name}: {e}")
        return False

def main():
    # List of actors
    actors = [
        "Morgan Freeman", "Sandra Bullock", "Denzel Washington", "Nicole Kidman",
        "Leonardo DiCaprio", "Meryl Streep", "Tom Hanks", "Angelina Jolie",
        "Brad Pitt", "Viola Davis", "Chris Hemsworth", "Scarlett Johansson",
        "Robert Downey Jr.", "Zendaya", "Joaquin Phoenix", "Natalie Portman",
        "Keanu Reeves", "Margot Robbie", "Henry Cavill", "Florence Pugh"
    ]

    # Create output directory
    output_folder = "actors_images"
    os.makedirs(output_folder, exist_ok=True)

    # Process each actor
    for actor in actors:
        print(f"\nProcessing {actor}...")
        
        # Get the image URL
        image_url = get_actor_image(actor)
        
        if image_url:
            # Download and convert the image
            download_and_convert_to_png(image_url, actor, output_folder)
        else:
            print(f"❌ No image found for {actor}")
        
        # Add a small delay to avoid hitting rate limits
        time.sleep(1)

if __name__ == "__main__":
    main()
