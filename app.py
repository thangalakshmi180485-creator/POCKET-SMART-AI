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

# 💾 பயனர்களின் விபரங்களை நிரந்தரமாகச் சேமிக்கும் JSON ஃபைல் செட்டப்
DB_FILE = "users_db.json"

def load_users():
    default_list = ["sai", "admin", "user123", "aswathi", "sumathi", "sankari"]
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(default_list, f)
        return default_list
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default_list

def save_user(username: str):
    users = load_users()
    if username not in users:
        users.append(username)
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f)

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
        def make_links(item_query):
            q = urllib.parse.quote_plus(item_query)
            return {
                "amazon": f"https://amazon.in{q}",
                "flipkart": f"https://flipkart.com{q}",
                "ikea": f"https://ikea.com{q}"
            }
        return {
            "status": "success",
            "budget_summary": {"total_budget": total, "remaining_budget": total * 0.1},
            "categories": [
                {"name": "Lighting", "allocation": total * 0.3, "items": [{"name": "LED Bulb", "price": 100.0, "quantity": data.num_lights, "links": make_links("led bulb")}]},
                {"name": "Ceiling_fans", "allocation": total * 0.4, "items": [{"name": "Havells Fan", "price": 500.0, "quantity": data.num_fans, "links": make_links("havells fan")}]},
                {"name": "Furniture", "allocation": total * 0.2, "items": [{"name": "Plastic Chair", "price": 250.0, "quantity": data.num_furniture, "links": make_links("plastic chair")}]}
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def load_html_page(page_name: str) -> str:
    file_path = os.path.join("templates", page_name)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return f"<h1>Error: templates/{page_name} file is missing.</h1>"

# --- 🔐 லாகின் சரிபார்ப்பு எண்ட்பாயிண்ட் (GET & POST இரண்டையும் ஏற்கும் வண்ணம் மாஸ்டர் செட்டப்) ---
@app.api_route("/login-check", methods=["GET", "POST"])
async def login_check(username: str = Form(None), password: str = Form(None)):
    if not username:
        return RedirectResponse(url="/login", status_code=303)
    
    current_users = load_users()
    if username not in current_users:
        error_html = load_html_page("login.html").replace(
            'Sign In</h3>',
            'Sign In</h3><div class="alert alert-danger text-center" style="font-size:0.85rem; padding:10px; margin-bottom:15px; border-radius:6px;">Access Denied! Account not found. Please click Create Account first.</div>'
        )
        return HTMLResponse(content=error_html)
    return RedirectResponse(url=f"/dashboard?user={username}", status_code=303)

# --- 🎯 புதிய கணக்கு பதிவு செய்யும் எண்ட்பாயிண்ட் (GET & POST இரண்டையும் ஏற்கும் வண்ணம் மாஸ்டர் செட்டப்) ---
@app.api_route("/register-save", methods=["GET", "POST"])
async def register_save(username: str = Form(None), password: str = Form(None), email: str = Form(None)):
    if not username:
        return RedirectResponse(url="/register", status_code=303)
        
    save_user(username)
    
    success_html = load_html_page("login.html").replace(
        'Sign In</h3>',
        'Sign In</h3><div class="alert alert-success text-center" style="font-size:0.85rem; padding:10px; margin-bottom:15px; border-radius:6px;">Registration Successful! Please Sign In with your new account.</div>'
    )
    return HTMLResponse(content=success_html)

# --- 🔗 வெப் முகவரிகள் அலைன்மென்ட் மேப்பிங் ---
@app.get("/", response_class=HTMLResponse)
async def serve_landing_page(): return load_html_page("index.html")

@app.get("/login", response_class=HTMLResponse)
async def serve_login_page(): return load_html_page("login.html")

@app.get("/register", response_class=HTMLResponse)
async def serve_register_page(): return load_html_page("register.html")

@app.get("/dashboard", response_class=HTMLResponse)
@app.get("/index", response_class=HTMLResponse)
async def serve_dashboard_page(): return load_html_page("dashboard.html")

@app.get("/home", response_class=HTMLResponse)
async def serve_home_planner(): return load_html_page("home_planner.html")

@app.get("/party", response_class=HTMLResponse)
async def serve_party_planner(): return load_html_page("party_planner.html")

@app.get("/jewelry", response_class=HTMLResponse)
async def serve_jewelry_planner(): return load_html_page("jewelry_planner.html")

@app.get("/history", response_class=HTMLResponse)
async def serve_history_page(): return load_html_page("history.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)