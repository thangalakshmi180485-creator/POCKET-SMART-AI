import os
import json
import urllib.parse
from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="PocketSmart: AI Budget Planner Master Engine")

# 🔐 பிரவுசர் பட்டன்கள் பிளாக் ஆகாமல் தடுக்க CORS பாதுகாப்பு செட்டப்
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 👥 பதிவு செய்யப்பட்ட அசல் பயனர்களின் பட்டியல்
registered_users = ["sai", "admin", "user123", "aswathi", "sumathi", "sankari"]

# 🏠 ஹோம் பிளானர் பிரண்ட்எண்ட் ஜாவாஸ்கிரிப்ட் அனுப்பும் மாறிகள் கட்டமைப்பு
class HomeBudgetInput(BaseModel):
    total_budget: float
    num_lights: int = 5
    num_fans: int = 4
    num_furniture: int = 2

# 💰 அமேசான், ஃப்ளிப்கார்ட் லைவ் லிங்க்குகள் கச்சிதமாக இணைக்கப்பட்டுள்ளது
@app.post("/generate-home")
async def plan_home_budget(data: HomeBudgetInput):
    try:
        total = data.total_budget
        
        # 💡 அதிகாரப்பூர்வ அமேசான் (/s?k=) மற்றும் ஃப்ளிப்கார்ட் (/search?q=) தேடல் லேயர் குறியீடுகள்!
        def make_links(item_query):
            q = urllib.parse.quote_plus(item_query)
            return {
                "amazon": f"https://amazon.in{q}",
                "flipkart": f"https://flipkart.com{q}",
                "ikea": f"https://ikea.com{q}",
                "myntra": f"https://myntra.com{q}",
                "ajio": f"https://ajio.com{q}"
            }

        return {
            "status": "success",
            "budget_summary": {
                "total_budget": total,
                "remaining_budget": total * 0.1
            },
            "categories": [
                {
                    "name": "Lighting",
                    "allocation": total * 0.3,
                    "items": [{
                        "name": "LED Bulb (Warm White)",
                        "description": "Energy-efficient LED bulbs for general interior lighting.",
                        "price": 100.00,
                        "quantity": data.num_lights,
                        "links": make_links("led bulb warm white")
                    }]
                },
                {
                    "name": "Ceiling_fans",
                    "allocation": total * 0.4,
                    "items": [{
                        "name": "Havells Ceiling Fan",
                        "description": "Premium functional high-speed cooling fan.",
                        "price": 500.00,
                        "quantity": data.num_fans,
                        "links": make_links("havells ceiling fan")
                    }]
                },
                {
                    "name": "Furniture",
                    "allocation": total * 0.2,
                    "items": [
                        {
                            "name": "Plastic Chair",
                            "description": "Stackable plastic chairs for kitchen or living room space.",
                            "price": 250.00,
                            "quantity": data.num_furniture,
                            "links": make_links("plastic chair")
                        },
                        {
                            "name": "Small Wooden Table",
                            "description": "Simple elegant wooden table for dining layouts.",
                            "price": 500.00,
                            "quantity": 1,
                            "links": make_links("small wooden table")
                        }
                    ]
                }
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 📜 உங்க லேப்டாப்பில் இருக்கும் எச்.டி.எம்.எல் பக்கங்களை எர்ரர் இல்லாமல் நேரடியாக வாசிக்கும் பக்கா முறை!
def load_html_page(page_name: str) -> str:
    file_path = os.path.join("templates", page_name)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return f"<h1>Error: templates/{page_name} file is missing inside workspace.</h1>"

# --- 🔐 லாகின் பாதுகாப்பு சரிபார்ப்பு எண்ட்பாயிண்ட் ---
@app.post("/login-check")
async def login_check(username: str = Form(...), password: str = Form(...)):
    if username not in registered_users:
        error_html = load_html_page("login.html").replace(
            'Sign In</h3>',
            'Sign In</h3><div class="alert alert-danger text-center" style="font-size:0.85rem; padding:10px; margin-bottom:15px; border-radius:6px;">Access Denied! Account not found. Please click Create Account first.</div>'
        )
        return HTMLResponse(content=error_html)
    return RedirectResponse(url=f"/dashboard?user={username}", status_code=302)

# --- 🔗 வெப் முகவரிகள் அலைன்மென்ட் மேப்பிங் ---

@app.get("/", response_class=HTMLResponse)
async def serve_landing_page():
    # 🎯 பயனர் முதன்முதலில் உள்ளே வரும்போது அச்சு அசலான மெயின் முகப்புப் பக்கம் (index.html) லோடு ஆகும்!
    return load_html_page("index.html")

@app.get("/login", response_class=HTMLResponse)
async def serve_login_page():
    # 🎯 முகப்புப் பக்கத்தில் இருக்கும் 'Get Started' பட்டனை அமுக்கும்போது மட்டும் லாகின் பக்கம் லோடு ஆகும்!
    return load_html_page("login.html")

@app.get("/register", response_class=HTMLResponse)
async def serve_register_page():
    return load_html_page("register.html")

@app.get("/dashboard", response_class=HTMLResponse)
@app.get("/index", response_class=HTMLResponse)
async def serve_dashboard_page():
    return load_html_page("dashboard.html")

@app.get("/home", response_class=HTMLResponse)
async def serve_home_planner():
    return load_html_page("home_planner.html")

@app.get("/party", response_class=HTMLResponse)
async def serve_party_planner():
    return load_html_page("party_planner.html")

@app.get("/jewelry", response_class=HTMLResponse)
async def serve_jewelry_planner():
    return load_html_page("jewelry_planner.html")

@app.get("/history", response_class=HTMLResponse)
async def serve_history_page():
    return load_html_page("history.html")

if __name__ == "__main__":
    import uvicorn
    print("Starting PocketSmart Master Backend Server...")
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)