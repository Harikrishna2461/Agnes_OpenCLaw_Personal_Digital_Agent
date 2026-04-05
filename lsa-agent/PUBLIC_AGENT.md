# 🚀 Agnes LSA - Public Web Agent

Your personal **Life Simulation Agent** accessible from anywhere on any device!

## ⚡ Quick Start (30 seconds)

```bash
cd /Users/HariKrishnaD/Downloads/Agnes_AI/lsa-agent
./run_public.sh
```

That's it! You'll see a public URL like:
```
https://abc123-def456.ngrok.io
```

Open that URL on **any phone/tablet/laptop** and start using Agnes!

---

## 🎯 What You Get

✅ **Modern Web Interface** - Beautiful, mobile-responsive chat interface
✅ **Instant Analysis** - Ask any decision question and get LSA analysis
✅ **Multiple Scenarios** - See A/B/C options with scoring
✅ **Public Access** - Works from anywhere in the world
✅ **No Installation** - Works in any browser

---

## 📱 How to Use Agnes

### From Your Phone

1. **Get the URL** - Run `./run_public.sh` on your computer
2. **Open in Browser** - Paste the URL in your mobile browser
3. **Ask a Question** - Type any decision question:
   - "Should I go to the gym?"
   - "Can I skip class today?"
   - "Is it a good time to study?"
4. **Get Analysis** - Agnes shows 3 options (A/B/C) with scores

### From Desktop

Simply visit `http://localhost:5001/` while the server is running

---

## 🎨 Interface Features

### Quick Options
Start with pre-made questions:
- 📚 Can I skip class today?
- 💪 Should I go to the gym?
- 📖 Is it a good time to study?
- 🌴 Can I take a break today?

### Ask Anything
Type your own decision question for custom analysis

### Instant Responses
Agnes analyzes within seconds showing:
- **A: Minimal Effort** - Conservative approach
- **B: Balanced** - RECOMMENDED middle ground (often best)
- **C: Maximum Effort** - Ambitious approach

Each option includes:
- Description of the option
- Risk level (low/medium/high)
- Confidence percentage
- Score (higher is better)

---

## 🌐 Making it Public

### Option 1: ngrok (Automatic - Easiest)
```bash
./run_public.sh
```
- Automatically starts ngrok tunnel
- Shows you a public URL
- Works for 2 hours (free tier)
- Just run the script again to get new URL

### Option 2: Manual ngrok
```bash
/Terminal 1:
./run_public.sh  # or manually: python3 whatsapp_server.py --port 5001

Terminal 2:
ngrok http 5001
```

### Option 3: Deploy to Cloud (Later)
- Heroku, Railway, Render, Fly.io - all support Flask
- Just point to this repo and it runs

---

## 🔧 Technical Details

### Architecture
```
Mobile Browser → HTTPS Tunnel (ngrok) → Flask Server (Port 5001) → LSA Engine
```

### Files
- `static/index.html` - Web interface (modern + mobile-responsive)
- `whatsapp_server.py` - Flask API + static file serving
- `main.py` - LSA Decision Engine
- `run_public.sh` - One-command public setup

### API Endpoint
```
POST /webhook/whatsapp
{
  "from": "+1234567890",
  "message": "Should I go to the gym?",
  "token": "lsa_secure_token"
}

Returns:
{
  "status": "ok",
  "response": "🤖 LSA Decision Analysis...",
  "sent": true
}
```

---

## 🎓 Examples

### Example 1: Should I go to the gym?
```
🤖 LSA Decision Analysis

📌 Decision:
Should I go to the gym?

🎯 Your Options (7 days):

A️⃣ Minimal Effort 
   Skip exercise entirely. Stay home, relax...
   Risk: low | Confidence: 85%
   Score: 101

B️⃣ Balanced ✨ RECOMMENDED
   30-minute workout instead of full session...
   Risk: low | Confidence: 88%
   Score: 159

C️⃣ Maximum Effort
   Full 90-minute workout + stretching...
   Risk: high | Confidence: 72%
   Score: 196

✅ Best Choice: C: Maximum Effort / Ambitious
💡 Higher score = Better long-term outcome
```

### Example 2: Can I skip class today?
```
A️⃣ Minimal Effort - Score: 88
   (Sleep in, skip, no commitment)

B️⃣ Balanced ✨ RECOMMENDED - Score: 148
   (Attend but 30 min late/early)

C️⃣ Maximum Effort - Score: 172
   (Full attendance + review notes)
```

---

## ⚙️ Commands

### Start Public Agent
```bash
./run_public.sh
```

### Start Local Only
```bash
python3 whatsapp_server.py --port 5001
```

### Check if Server is Running
```bash
curl http://localhost:5001/health
```

### View Logs
```bash
tail -f /tmp/lsa_agent.log
```

### Stop Everything
```bash
pkill -f "whatsapp_server.py"
pkill -f "ngrok http"
```

---

## 🚨 Troubleshooting

### "Connection refused" when accessing URL?
- Check that `./run_public.sh` shows ngrok URL and "✅ YOUR AGENT IS LIVE"
- Wait 10 seconds for ngrok to fully connect
- Try refreshing the page

### "Port 5001 already in use"?
```bash
pkill -f "whatsapp_server.py"
sleep 2
./run_public.sh
```

### ngrok: "connection refused"?
- Make sure server is running (`./run_public.sh` does this automatically)
- Check: `curl http://localhost:5001/health`

### "Agent not responding" in browser?
- Check Flask logs: `tail -f /tmp/lsa_agent.log`
- Ensure sentence-transformers installed: `pip3 install sentence-transformers`

### Want to use your own server?
- Change `server` in `static/index.html` line 285
- Run `./run_public.sh` to deploy

---

## 🎯 Next Steps

1. **Now** → Run `./run_public.sh` and test on your phone
2. **Today** → Try with different decision questions
3. **This Week** → Deploy to a permanent server (Heroku, Railway, etc.)
4. **Later** → Add real WhatsApp integration

---

## 💡 Pro Tips

### Getting Better Answers
- Be specific: "Should I study biology for 3 hours?" (better than "study?")
- Include context: "I have an exam in 2 days and haven't started"
- Ask follow-ups: "What if I study for 1 hour instead of 3?"

### Mobile Experience
- Save URL to home screen for bookmark
- Works offline after first load (cached)
- Dark mode support coming soon

### Permanent Public Access
**Don't have ngrok?** Just deploy to Heroku:
```bash
git add .
git commit -m "Add public web agent"
git push heroku main
```

---

## 📊 Features Coming Soon

- 🌙 Dark mode
- 💾 Decision history
- 📈 Analytics dashboard
- 🔔 Notifications
- 📱 Native apps
- 🎯 Personalized learning path

---

## ❓ FAQ

**Q: Is it secure?**
A: Yes! Uses token validation (`lsa_secure_token`) and HTTPS via ngrok.

**Q: Can multiple people use it?**
A: Yes! Just share the public URL - it works for everyone.

**Q: Will my URL keep working?**
A: Free ngrok URLs last 2 hours. Run the script again for a new one. For permanent URLs, deploy to cloud.

**Q: Can I customize the interface?**
A: Yes! Edit `static/index.html` and refresh.

**Q: Does my data get saved?**
A: Decisions are logged locally but not sent anywhere. Privacy-first!

**Q: Can I add real WhatsApp integration?**
A: Yes! See `WHATSAPP_SETUP.md` for detailed steps.

---

## 🤝 Support

- Having issues? Check `/tmp/lsa_agent.log`
- Questions? Ask Agnes directly in the web interface!
- Want features? Modify `static/index.html` or `whatsapp_server.py`

---

**Made with ❤️ by Agnes AI Team**

Your personal Life Simulation Agent - Always learning, always improving! 🚀
