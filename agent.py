"""
Photography Business - WhatsApp Booking Agent
Using: Twilio (WhatsApp) + Anthropic Claude API
"""

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import anthropic
import json
import os
from datetime import datetime

app = Flask(__name__)

# ============================================================
# CONFIGURATION - Apni details yahan bharo
# ============================================================
ANTHROPIC_API_KEY = "your_anthropic_api_key_here"
TWILIO_ACCOUNT_SID = "your_twilio_account_sid"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"  # Twilio sandbox number

# ============================================================
# PHOTOGRAPHY BUSINESS DETAILS - Customize karo
# ============================================================
BUSINESS_INFO = """
Business Name: [Tumhara Studio Name]
Photographer: [Tumhara Naam]
Location: [Tumhari City]

PACKAGES:
1. Basic Package - ₹15,000
   - 2 hours shoot
   - 50 edited photos
   - 1 location

2. Standard Package - ₹25,000
   - 4 hours shoot
   - 100 edited photos
   - 2 locations
   - 1 outfit change

3. Premium Package - ₹45,000
   - Full day shoot (8 hours)
   - 200+ edited photos
   - Multiple locations
   - Unlimited outfit changes
   - Same day preview (5 photos)

4. Wedding Package - ₹80,000
   - 2 photographers
   - Full day coverage
   - 500+ edited photos
   - Wedding album (20 pages)
   - Highlight reel video

PHOTOGRAPHY TYPES:
- Wedding Photography
- Pre-Wedding / Engagement
- Portrait & Family
- Birthday & Events
- Corporate & Professional
- Product Photography

DELIVERY TIME: 7-10 business days
ADVANCE PAYMENT: 30% booking amount required

CONTACT: [Your Phone] | [Your Email]
"""

# ============================================================
# CONVERSATION MEMORY (In-memory - production mein database use karo)
# ============================================================
conversations = {}  # {phone_number: [messages]}
bookings = {}       # {phone_number: booking_details}

# ============================================================
# ANTHROPIC CLIENT
# ============================================================
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = f"""
Tu ek professional photography business ka WhatsApp booking agent hai.
Tumhara kaam clients ki help karna aur bookings lena hai.

{BUSINESS_INFO}

TUMHARI PERSONALITY:
- Friendly aur professional
- Hindi aur English dono mein baat karo (Hinglish ok hai)
- Short aur clear messages bhejo (WhatsApp ke liye)
- Emojis use karo (kam, lekin relevant)

BOOKING PROCESS:
1. Client ka naam puchho
2. Photography type puchho (wedding, portrait, event, etc.)
3. Date aur location puchho
4. Package suggest karo budget ke hisaab se
5. Confirm karo aur advance payment info do

IMPORTANT RULES:
- Agar date available hai toh confirm karo
- Agar client budget pooche toh packages clearly explain karo
- Booking confirm hone par BOOKING_CONFIRMED: naam, date, package, amount likho
- Har message short rakho (3-4 lines max for WhatsApp)
- Agar koi question hai jo tum answer nahi kar sakte, photographer se baat karne ko kaho
"""

# ============================================================
# WEBHOOK - WhatsApp se message aata hai yahan
# ============================================================
@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    from_number = request.values.get("From", "")
    
    print(f"\n📱 Message from {from_number}: {incoming_msg}")
    
    # Conversation history maintain karo
    if from_number not in conversations:
        conversations[from_number] = []
    
    # User message add karo
    conversations[from_number].append({
        "role": "user",
        "content": incoming_msg
    })
    
    # Claude se response lo
    try:
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=500,
            system=SYSTEM_PROMPT,
            messages=conversations[from_number]
        )
        
        reply = response.content[0].text
        
        # Booking confirm hua? Save karo
        if "BOOKING_CONFIRMED:" in reply:
            save_booking(from_number, reply)
            reply = reply.replace("BOOKING_CONFIRMED:", "").strip()
        
        # Assistant response save karo
        conversations[from_number].append({
            "role": "assistant", 
            "content": reply
        })
        
        print(f"🤖 Agent reply: {reply}")
        
    except Exception as e:
        reply = "Sorry, abhi technical problem hai. Thodi der mein try karein. 🙏"
        print(f"❌ Error: {e}")
    
    # WhatsApp par reply bhejo
    resp = MessagingResponse()
    resp.message(reply)
    return str(resp)

# ============================================================
# BOOKING SAVE FUNCTION
# ============================================================
def save_booking(phone, confirmation_text):
    booking = {
        "phone": phone,
        "timestamp": datetime.now().isoformat(),
        "details": confirmation_text,
        "status": "confirmed"
    }
    bookings[phone] = booking
    
    # File mein save karo
    with open("bookings.json", "a") as f:
        f.write(json.dumps(booking) + "\n")
    
    print(f"✅ Booking saved for {phone}")

# ============================================================
# BOOKINGS DEKHO (Admin endpoint)
# ============================================================
@app.route("/bookings", methods=["GET"])
def view_bookings():
    return json.dumps(bookings, indent=2, ensure_ascii=False)

# ============================================================
# HEALTH CHECK
# ============================================================
@app.route("/", methods=["GET"])
def home():
    return "📸 Photography Booking Agent is running!"

# ============================================================
# RUN
# ============================================================
if __name__ == "__main__":
    print("📸 Photography Booking Agent starting...")
    print("✅ Webhook URL: http://localhost:5000/webhook")
    print("📋 Bookings URL: http://localhost:5000/bookings")
    app.run(debug=True, port=5000)
