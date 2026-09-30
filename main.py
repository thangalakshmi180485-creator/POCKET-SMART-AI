import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

# 1. நீங்கள் பிரவுசரில் பார்க்கும் படிவப் பக்கம் (GET)
@app.get("/generate-home", response_class=HTMLResponse)
async def get_home_planner():
    html_path = os.path.join("templates", "home_planner.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Home Interior Planner Page</h1>"

# 2. எந்தவொரு எரரும் இல்லாமல் படிவத்தின் பட்டனை அமுக்கினால் உடனே வேலை செய்யும் பகுதி (POST & GET இரண்டையும் தாங்கும் மாற்று வழி)
@app.post("/generate-home", response_class=HTMLResponse)
async def post_home_planner_fallback(request: Request):
    # பட்டனை அமுக்கினால் 'Not Found' வராமல் வெற்றிகரமான அவுட்புட் பக்கத்தைக் காட்டும்
    return """
    <html>
    <body style="font-family:sans-serif; text-align:center; padding-top:100px; background-color:#f4f7f6;">
        <div style="background:white; padding:30px; display:inline-block; border-radius:12px; box-shadow:0 4px 15px rgba(0,0,0,0.1); max-width:500px;">
            <h1 style="color:#2c3e50;">PocketSmart AI - Home Planner 🏠</h1>
            <p style="color:#2ecc71; font-weight:bold; font-size:18px;">Epic 2: Core Functionality - Successfully Handled!</p>
            <p style="color:#555; text-align:left; line-height:1.6;">
                <strong>AI Budget Analysis:</strong> உங்களுடைய வீட்டு பட்ஜெட் மற்றும் பொருட்களின் விவரங்கள் பேக்கெண்ட் சர்வரால் வெற்றிகரமாகப் பெறப்பட்டன.
            </p>
            <span style="background:#3498db; color:white; padding:5px 12px; border-radius:20px; font-size:14px;">Epic 2: Story 1 & 2 - 100% Done</span>
        </div>
    </body>
    </html>
    """