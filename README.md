# 📧 Contact Data Cleaner - Web Version

Professional web application for converting PST files and Excel files to clean, deduplicated contact data.

**Live Demo:** *Coming soon - Deploy to Streamlit Cloud*

---

## 🚀 Features

- ✅ Upload Excel files (.xlsx, .xls, .csv)
- ✅ Upload PST files (.pst)
- ✅ Automatic duplicate removal
- ✅ Email validation
- ✅ Domain extraction
- ✅ Download cleaned contacts as Excel
- ✅ Live preview of results
- ✅ Progress tracking
- ✅ Mobile-friendly interface

---

## 🎯 Quick Deploy to Streamlit Cloud

### Step 1: Access Streamlit Cloud
Go to: **https://share.streamlit.io**

### Step 2: Sign in with GitHub
Click "Sign in with GitHub"

### Step 3: Deploy
1. Click **"New app"**
2. Configure:
   - **Repository:** `Raztsook/contact-data-cleaner-web`
   - **Branch:** `main`
   - **Main file path:** `app.py`
3. Click **"Deploy"**

### Step 4: Done! 🎉
Your app will be live in 2-5 minutes at:
```
https://[your-chosen-name].streamlit.app
```

---

## 💻 Run Locally

### Requirements
- Python 3.8+

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Raztsook/contact-data-cleaner-web.git
cd contact-data-cleaner-web
```

2. Install dependencies:
```bash
pip install -r requirements-web.txt
```

3. Run the app:
```bash
streamlit run app.py
```

4. Open your browser to: **http://localhost:8501**

---

## 📊 Output Format

The application exports contacts in the following format:

| Column | Description |
|--------|-------------|
| Full Name | Complete name of the contact |
| First Name | First name extracted |
| Last Name | Last name extracted |
| Email | Valid email address |
| Domain | Email domain (e.g., gmail.com) |

---

## 🔒 Privacy & Security

- Files are processed in temporary storage
- All data is deleted after conversion
- No information is stored permanently
- Secure file upload and download

---

## 🛠️ Technologies Used

- **Streamlit** - Web framework
- **Pandas** - Data processing
- **openpyxl** - Excel handling
- **libpff-python** - PST file processing
- **Python 3** - Backend logic

---

## 📝 Supported File Formats

### Input:
- Excel: `.xlsx`, `.xls`
- CSV: `.csv`
- Outlook PST: `.pst`

### Output:
- Excel: `.xlsx` (cleaned and deduplicated)

---

## 🎨 Configuration

### Change Upload Size Limit

Edit `.streamlit/config.toml`:

```toml
[server]
maxUploadSize = 1000  # MB (default: 500)
```

### Customize Theme

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#27ae60"
backgroundColor = "#f8f9fa"
textColor = "#2c3e50"
```

---

## 📖 Documentation

- **Full Documentation:** See `README-WEB.md`
- **Deployment Guide:** Contact repository owner

---

## 🐛 Troubleshooting

### Issue: File too large
**Solution:** Increase `maxUploadSize` in `.streamlit/config.toml`

### Issue: PST files not processing
**Solution:** Ensure `libpff-python` is installed. The app will fallback to alternative methods if needed.

### Issue: Deployment fails
**Solution:** Check that all files are committed to the repository:
- `app.py`
- `requirements-web.txt`
- `packages.txt`
- `.streamlit/config.toml`

---

## 📧 Contact

For issues or questions, please open an issue on GitHub.

---

## 📄 License

[Your License Here]

---

## 🙏 Credits

Created by Raztsook

Built with ❤️ using Streamlit

---

**Ready to deploy?** → https://share.streamlit.io

**Repository:** https://github.com/Raztsook/contact-data-cleaner-web

