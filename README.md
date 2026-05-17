<div align="center">

<!-- Replace this with your bot's pfp when you have one -->
<img src="https://images.steamusercontent.com/ugc/1756947933468891271/9C46692343C4182043FC8EA2991E2124A0F32E23/?imw=512&&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=false" width="120" height="120" style="border-radius: 50%"/> 



# 🍅 Pomu
### *Pomodoro timer bot for some discord server*

![Python](https://img.shields.io/badge/Python-3.10+-8b5cf6?style=for-the-badge&logo=python&logoColor=white)
![discord.py](https://img.shields.io/badge/discord.py-2.3+-8b5cf6?style=for-the-badge&logo=discord&logoColor=white)
![Status](https://img.shields.io/badge/status-hosted-10b981?style=for-the-badge)

 *stay focused ✨*

**Made with 💜 by rusty.fae**

</div>

---

## ✨ What is Pomu?

Pomu is a simple yet powerful Pomodoro timer bot built for focused study sessions. Start a timer, take breaks, and stay productive — all from your Discord server!

- 🍅 Customizable study and break durations
- 🔁 Looping pomodoro cycles
- ⏸️ Pause and resume anytime
- 🛑 Auto stops if you leave the voice channel
- 📊 Live embed that updates every 5 seconds

---

## 🎛️ Commands

All commands use the `!pomo` prefix.

| Command | Description |
|---|---|
| `!pomo 25 5` | Start a 25 min study + 5 min break session |
| `!pomo 25 5 4` | Start 4 looping pomodoro cycles |
| `!pause` | Pause the current timer |
| `!resume` | Resume the paused timer |
| `!stop` | Stop the current session |
| `!status` | Check current timer status |
| `!pomo help` | Show the help menu |

 ⚠️ You must be in a voice channel to start a session!

---

## ⚙️ Setup

### Prerequisites
- Python 3.10+
- A Discord bot token

### 1. Clone the repo
```bash
git clone https://github.com/rustyfae/pomu.git
cd pomu
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
Create a `.env` file:
```env
TOKEN=your_bot_token_here
```

### 5. Run!
```bash
python main.py
```

---

## 📁 Project Structure

```
pomu/
├── main.py             ← main bot code
├── requirements.txt    ← dependencies
└── .env                ← your secrets (never give this to anyone!)
```

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---|---|
| Bot not responding | Make sure you're in a voice channel first |
| Timer not updating | Discord can be slow, wait a few seconds |
| Bot goes offline | Check your hosting panel and restart |

---

<div align="center">

*built for* **some discord server** 🌙

</div>
