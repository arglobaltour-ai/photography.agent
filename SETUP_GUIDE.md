# 📸 Photography WhatsApp Booking Agent - Setup Guide

## Step 1: Install karo
```bash
pip install -r requirements.txt
```

## Step 2: API Keys lo

### Anthropic API Key:
1. https://console.anthropic.com par jao
2. Account banao
3. API Keys section mein jaake key copy karo
4. agent.py mein `your_anthropic_api_key_here` ki jagah paste karo

### Twilio WhatsApp Setup:
1. https://twilio.com par free account banao
2. Console mein Account SID aur Auth Token copy karo
3. agent.py mein paste karo
4. Twilio Console → Messaging → Try it out → Send a WhatsApp message
5. Sandbox activate karo (join [word] bhejo given number par)

## Step 3: Business Details Update karo
agent.py mein `BUSINESS_INFO` section mein:
- Apna studio naam
- Apna naam
- Apni city
- Apne packages aur prices
- Contact details

## Step 4: Agent Run karo
```bash
python agent.py
```

## Step 5: ngrok se Public URL banao
```bash
# ngrok install karo: https://ngrok.com
ngrok http 5000
```
Tumhe milega: `https://abc123.ngrok.io`

## Step 6: Twilio mein Webhook set karo
1. Twilio Console → WhatsApp Sandbox Settings
2. "When a message comes in" field mein:
   `https://abc123.ngrok.io/webhook`
3. Save karo

## Step 7: Test karo!
WhatsApp par Twilio sandbox number par message bhejo aur agent se baat karo!

---

## Bookings Kaise Dekhen?
Browser mein jao: `http://localhost:5000/bookings`

---

## Production ke liye (Later):
- ngrok ki jagah Railway/Render/Heroku use karo (free hosting)
- In-memory storage ki jagah PostgreSQL/MongoDB use karo
- Twilio ka proper WhatsApp Business account lo

---

## Help chahiye?
Koi bhi step mein problem ho toh poochho! 🙏
