# Contact Data Cleaner - Web Version 🌐

A web-based application for converting PST files and Excel files to clean contact data, accessible from anywhere.

## 🚀 Quick Start

### Option 1: Run Locally

1. Install dependencies:
```bash
pip install -r requirements-web.txt
```

2. Run the app:
```bash
streamlit run app.py
```

3. Open your browser to: `http://localhost:8501`

### Option 2: Deploy to Streamlit Cloud (FREE!)

1. **Push to GitHub:**
   - Create a new GitHub repository
   - Push this folder to the repository

2. **Deploy to Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file: `app.py`
   - Click "Deploy"

3. **Your app will be live at:**
   - `https://[your-app-name].streamlit.app`
   - Share this URL with anyone!

## 📦 What's Included

- `app.py` - Main Streamlit web application
- `requirements-web.txt` - Python dependencies
- `packages.txt` - System packages for Streamlit Cloud
- `.streamlit/config.toml` - Streamlit configuration

## 🎯 Features

- ✅ Upload files from anywhere (Excel, CSV, PST)
- ✅ Automatic contact extraction
- ✅ Duplicate removal
- ✅ Email validation
- ✅ Domain extraction
- ✅ Download cleaned contacts as Excel
- ✅ Preview results before downloading
- ✅ Progress tracking
- ✅ Mobile-friendly interface

## 🔧 Configuration

### File Size Limit

Default: 500MB. To change, edit `.streamlit/config.toml`:

```toml
[server]
maxUploadSize = 1000  # Change to 1GB
```

### Theme Colors

Edit `.streamlit/config.toml` to customize colors:

```toml
[theme]
primaryColor = "#27ae60"
backgroundColor = "#f8f9fa"
textColor = "#2c3e50"
```

## 🐳 Docker Deployment (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    pst-utils \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements-web.txt .
RUN pip install --no-cache-dir -r requirements-web.txt

# Copy app files
COPY . .

# Expose port
EXPOSE 8501

# Run the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t contact-cleaner .
docker run -p 8501:8501 contact-cleaner
```

## 🌍 Alternative Hosting Options

### Railway.app (Free Tier)
1. Connect your GitHub repo
2. Add environment variable: `PORT=8501`
3. Deploy!

### Render.com (Free Tier)
1. Connect your GitHub repo
2. Set start command: `streamlit run app.py --server.port=$PORT`
3. Deploy!

### Heroku
1. Create `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```
2. Push to Heroku
3. Deploy!

## 📊 Usage Statistics

The app includes usage tracking by default. To disable, edit `.streamlit/config.toml`:

```toml
[browser]
gatherUsageStats = false
```

## 🔒 Security Notes

- Files are processed in temporary storage and deleted after conversion
- No data is stored on the server
- All processing happens server-side (files are not processed in browser)

## 🆘 Troubleshooting

### libpff-python installation fails

If you get errors installing `libpff-python`, you may need to install it manually:

**Mac:**
```bash
brew install libpff
pip install libpff-python
```

**Linux:**
```bash
sudo apt-get install libpff-dev
pip install libpff-python
```

**Windows:**
- libpff-python is difficult to install on Windows
- The app will fall back to `readpst` method if available
- Or use Docker for Windows

### PST files not processing

Make sure you have either:
- `libpff-python` installed, OR
- `readpst` (pst-utils) installed on your system

## 📝 License

Same as original Contact Data Cleaner

## 🙏 Support

For issues or questions, please open an issue on GitHub.

---

Made with ❤️ | Contact Data Cleaner Web v2.0

