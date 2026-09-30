import os
import google.generativeai as genai
from dotenv import load_dotenv

# .env ஃபைலில் உள்ள கீ-ஐ லோடு செய்தல்
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    print("Error: API Key இல்லை! உங்கள் .env ஃபைலை சரிபார்க்கவும்.")
else:
    # ஜெமினி ஏஐ செட்டப் செய்தல் (Milestone 1)
    genai.configure(api_key=API_KEY)
    
    # டாக்குமெண்டில் உள்ளபடி மாடலை அழைத்தல்
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    try:
        # மாதிரி கேள்வி அனுப்பி இணைப்பைச் சோதித்தல் (Activity 1.3)
        response = model.generate_content("Say 'PocketSmart AI Gemini Connection Successful' in English")
        print("\n--- GEMINI API TEST RESULT ---")
        print(response.text)
        print("------------------------------\n")
    except Exception as e:
        print(f"இணைப்பில் பிழை ஏற்பட்டுள்ளது: {e}")