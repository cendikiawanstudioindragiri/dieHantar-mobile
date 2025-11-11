# Informasi Proyek dieHantar

Dokumen ini menyediakan ringkasan informasi penting tentang proyek dieHantar.

## 📁 1. Struktur/Daftar File Proyek

### Struktur Direktori Utama
```
dieHantar-mobile/
├── .github/              # GitHub Actions workflows
├── .idx/                 # Project IDX configuration
│   └── dev.nix          # Nix environment setup
├── .tours/              # CodeTour guides
│   ├── project_orientation.tour
│   └── locust_beginner.tour
├── blueprints/          # Flask Blueprints (modular components)
│   ├── auth.py         # Authentication
│   ├── rides.py        # Transportation service
│   ├── orders.py       # Food orders
│   ├── drivers.py      # Driver management
│   ├── chats.py        # Chat system
│   ├── payments.py     # Payment processing
│   └── data_catalog.py # Data catalog
├── seed_data/          # Initial database data
├── tests/              # Unit tests
├── main.py             # Application entry point
├── dev_server.py       # Development server
├── devserver.sh        # Dev server startup script
├── requirements.txt    # Python dependencies
├── firebase_config.py  # Firebase configuration
└── README.md          # Main documentation
```

### Perintah untuk Melihat Struktur
```bash
# List semua file
ls -la

# Tree view (jika tersedia)
tree

# Cari semua file Python
find . -type f -name "*.py" | grep -v __pycache__ | sort

# Count files by type
find . -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn
```

## 💻 2. Membuka Proyek di Editor/IDE

### A. Project IDX (Google Cloud IDE)
Project IDX adalah cloud-based IDE dari Google yang sudah dikonfigurasi untuk proyek ini.

**Konfigurasi:** `.idx/dev.nix`
- Python 3 environment
- Virtual environment otomatis di `.venv/`
- Auto-install dependencies
- Extensions: Python, Thunder Client

**URL:** https://idx.google.com/

### B. Visual Studio Code (Lokal)

#### Instalasi
1. Download dan install VS Code: https://code.visualstudio.com/

2. Clone repository:
```bash
git clone https://github.com/cendikiawanstudios/dieHantar-mobile.git
cd dieHantar-mobile
```

3. Buka di VS Code:
```bash
code .
```

#### Extensions yang Direkomendasikan
- **Python** (ms-python.python) - Python language support
- **Thunder Client** (rangav.vscode-thunder-client) - API testing
- **CodeTour** (vsls-contrib.codetour) - Interactive guided tours

#### Setup Virtual Environment
```bash
# Buat virtual environment
python3 -m venv .venv

# Aktifkan (Linux/Mac)
source .venv/bin/activate

# Aktifkan (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### C. PyCharm
1. Open → Select folder dieHantar-mobile
2. Configure Python Interpreter → Add → Virtualenv
3. Install requirements dari requirements.txt

### D. Vim/Neovim
```bash
cd dieHantar-mobile
vim .
# Gunakan plugin seperti coc.nvim untuk Python support
```

## 🌐 3. Menjalankan Proyek di Browser

### Prasyarat
1. Virtual environment aktif
2. Dependencies terinstall
3. Firebase credentials dikonfigurasi (file .env)

### Langkah-langkah

#### 1. Setup Environment Variables
Buat file `.env` di root folder:
```bash
touch .env
```

Tambahkan kredensial Firebase:
```env
FIREBASE_CREDENTIALS_JSON='{"type": "service_account", "project_id": "...", ...}'
```

Atau gunakan path ke file:
```env
GOOGLE_APPLICATION_CREDENTIALS=/path/to/serviceAccountKey.json
```

#### 2. Jalankan Server

**Metode 1: Development Server**
```bash
source .venv/bin/activate
python dev_server.py
```

**Metode 2: DevServer Script (Project IDX)**
```bash
./devserver.sh
```

**Metode 3: Flask CLI**
```bash
export FLASK_APP=main.py
flask run
```

#### 3. Akses di Browser

Server akan berjalan di:
- **Default:** http://localhost:8080
- **Port custom:** Set via environment variable `PORT`

#### 4. Test Endpoints

**Health Check:**
```
GET http://localhost:8080/
```

Response:
```json
{
  "status": "ok",
  "service": "dieHantar Super-App API"
}
```

**API Endpoints:**
- `/api/v1/auth/*` - Authentication
- `/api/v1/rides/*` - Transportation services
- `/api/v1/orders/*` - Food orders
- `/api/v1/drivers/*` - Driver management
- `/api/v1/chats/*` - Chat functionality
- `/api/v1/payments/*` - Payment processing
- `/api/v1/catalog/*` - Data catalog

#### 5. Testing dengan Tools

**cURL:**
```bash
curl http://localhost:8080/
curl http://localhost:8080/api/v1/catalog/foods
```

**Thunder Client (VS Code Extension):**
1. Open Thunder Client
2. New Request
3. Set URL: http://localhost:8080/
4. Send

**Browser Developer Tools:**
- Chrome/Firefox DevTools
- Network tab untuk melihat requests
- Console untuk debugging

## 🔍 4. Informasi Proyek (Git/GitHub/GCP)

### A. Git Repository

#### Remote Information
```bash
# Lihat remote repositories
git remote -v

# Output:
# origin  https://github.com/cendikiawanstudios/dieHantar-mobile (fetch)
# origin  https://github.com/cendikiawanstudios/dieHantar-mobile (push)
```

#### Branch Information
```bash
# Lihat semua branches
git branch -a

# Lihat current branch
git branch --show-current

# Lihat remote branches
git branch -r
```

#### Commit History
```bash
# Last 10 commits
git log --oneline -10

# Detailed log
git log --graph --decorate --all

# Commits by author
git log --author="nama"
```

#### Status & Changes
```bash
# Status file
git status

# Lihat changes
git diff

# Staged changes
git diff --staged
```

### B. GitHub Repository

#### Repository Details
- **Organization:** cendikiawanstudios
- **Repository Name:** dieHantar-mobile
- **Full URL:** https://github.com/cendikiawanstudios/dieHantar-mobile
- **Clone URL (HTTPS):** https://github.com/cendikiawanstudios/dieHantar-mobile.git
- **Clone URL (SSH):** git@github.com:cendikiawanstudios/dieHantar-mobile.git

#### Akses via Browser
1. Buka https://github.com/cendikiawanstudios/dieHantar-mobile
2. Explore:
   - Code tab - source code
   - Issues - bug tracking
   - Pull Requests - code reviews
   - Actions - CI/CD workflows

#### GitHub CLI (gh)
```bash
# Install gh (jika belum)
# Mac: brew install gh
# Linux: apt install gh / yum install gh

# Login
gh auth login

# View repo info
gh repo view cendikiawanstudios/dieHantar-mobile

# Open in browser
gh repo view --web

# Clone
gh repo clone cendikiawanstudios/dieHantar-mobile

# Create issue
gh issue create

# List PRs
gh pr list
```

### C. Google Cloud Platform (GCP)

#### Firebase Integration
Proyek ini menggunakan **Firebase** (platform development dari Google, bagian dari GCP).

**Services yang digunakan:**
- **Firestore** - NoSQL database
- **Firebase Storage** - File storage
- **Firebase Authentication** - User authentication
- **Firebase Admin SDK** - Server-side integration

#### Firebase Console
**URL:** https://console.firebase.google.com

**Akses:**
1. Login dengan Google account
2. Pilih project dieHantar
3. Navigate ke:
   - Firestore Database
   - Storage
   - Authentication
   - Project Settings

#### GCP Console
**URL:** https://console.cloud.google.com

**Services terkait:**
- Firestore
- Cloud Storage
- IAM & Admin
- APIs & Services

#### gcloud CLI
```bash
# Install gcloud CLI
# https://cloud.google.com/sdk/docs/install

# Login
gcloud auth login

# Set project
gcloud config set project PROJECT_ID

# List projects
gcloud projects list

# View current config
gcloud config list

# Firestore operations
gcloud firestore databases list
gcloud firestore indexes list
```

#### Environment Variables untuk GCP/Firebase

**Method 1: JSON String**
```env
FIREBASE_CREDENTIALS_JSON='{"type":"service_account","project_id":"...","private_key_id":"...","private_key":"...","client_email":"...","client_id":"...","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url":"..."}'
```

**Method 2: File Path**
```env
GOOGLE_APPLICATION_CREDENTIALS=/path/to/serviceAccountKey.json
```

#### Mendapatkan Service Account Key
1. Buka Firebase Console
2. Project Settings → Service Accounts
3. Generate New Private Key
4. Download JSON file
5. **JANGAN commit ke Git!**

---

## 📚 Resources Tambahan

### Dokumentasi
- **Flask:** https://flask.palletsprojects.com/
- **Firebase Admin Python SDK:** https://firebase.google.com/docs/admin/setup
- **pytest:** https://docs.pytest.org/

### CodeTour
Untuk panduan interaktif lengkap, install CodeTour extension dan buka:
- `.tours/project_orientation.tour` - Panduan orientasi proyek (BARU!)
- `.tours/locust_beginner.tour` - Load testing dengan Locust

### File Konfigurasi Penting
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (local, tidak di-commit)
- `.gitignore` - File yang diabaikan Git
- `.idx/dev.nix` - Project IDX configuration
- `firebase_config.py` - Firebase initialization

### Support
Untuk pertanyaan atau issues, buat issue di:
https://github.com/cendikiawanstudios/dieHantar-mobile/issues
