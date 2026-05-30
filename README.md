# YouTube Random QR Code App

Scan the QR code → goes to a random YouTube video every time.

## Run Locally

```bash
pip install flask gunicorn
python app.py
```
Open http://localhost:5000

## Deploy FREE on Railway (24/7)

1. Go to https://railway.app and sign up (free)
2. Click "New Project" → "Deploy from GitHub repo"
3. Upload these files to a GitHub repo first, then connect it
   OR use "Deploy from local" with the Railway CLI:

```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

4. Railway gives you a public URL like:
   `https://your-app.up.railway.app`

5. The QR code on your dashboard will automatically use that URL.
   Share the QR — anyone anywhere can scan it 24/7!

## Deploy FREE on Render

1. Go to https://render.com and sign up
2. New → Web Service → connect your GitHub repo
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn app:app`
5. Done — free 24/7 hosting!

## How It Works

- `/`     → Dashboard to manage your YouTube links
- `/go`   → Picks a random video and redirects the scanner
- QR code always points to `/go`
