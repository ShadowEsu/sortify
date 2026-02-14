import sys
import os
from google import genai
from PIL import Image
from dotenv import load_dotenv  # <--- Import this

# 1. Load environment variables from the .env file
load_dotenv()

# 2. Get the key securely
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    print("❌ Error: GOOGLE_API_KEY not found. Please check your .env file.")
    sys.exit(1)

def classify_waste_secure(image_path):
    
    # Initialize Client with the secure key
    client = genai.Client(api_key=API_KEY)

    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"❌ Error loading image file: {e}")
        return

    prompt_text = """
    You are a waste sorting expert. Analyze the image and determine if the subject is:
    1. COMPOST
    2. RECYCLE
    3. TRASH
    
    Format your response exactly like this:
    DECISION: [One of the 3 categories]
    REASON: [Short explanation]
    """

    print("Analyzing image with Gemini...")

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=[image, prompt_text]
        )
        print("\n" + "-"*30)
        print(response.text)
        print("-"*30)

    except Exception as e:
        print(f"❌ API Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python smart_sorter_v2.py <path_to_image>")
    else:
        classify_waste_secure(sys.argv[1])