# 🧠 SimplifiIQ AI Research Intern Assessment

This repository contains all three parts of the SimplifiIQ AI Research Intern Assessment.  
Each part demonstrates a different stage of automation, AI integration, and data visualization.

---

## 📂 Folder Structure

```
SimplifiIQ-assessment/
│
├── Part-A/                # Data Cleaning
│   ├── task_logs.csv
│   ├── clean_data.py
│   └── output_summary.csv
│
├── Part-B/                # Web Scraping + Gemini API Summarization
│   ├── scrape_summarize.py
│   ├── urls.txt
│   ├── scraped_summary.csv
│   ├── .env
│   
│
├── part-c-frontend/       # React Visualization Dashboard
│   ├── public/
│   │   └── scraped_summary.csv
│   ├── src/
│   │   └── App.js
│   ├── package.json
│   ├── package-lock.json
│   └── node_modules/
│
├── .gitignore
└── README.md
```

---

## 🧩 PART A — Data Cleaning (Python)

### 🎯 Objective
Clean raw task log data (e.g., invalid timestamps, negative durations) and produce a summary.

### 🧰 Dependencies
Install once (in your terminal):
```bash
pip install pandas
```

### ▶️ How to Run
1. Place your CSV file (`task_logs.csv`) in the `Part-A` folder.  
2. Run the script:
   ```bash
   cd Part-A
   python3 clean_data.py
   ```
3. The cleaned and summarized output will be saved as:
   ```
   output_summary.csv
   ```

### 🧠 Assumptions
- The input CSV contains columns:  
  `user, task_type, start, duration_min`
- Invalid timestamps or negative durations are skipped.

---

## 🤖 PART B — AI Summarization (Gemini API + Python)

### 🎯 Objective
Scrape webpage content, summarize it using **Google Gemini API**, and export results to a CSV.

### 🧰 Dependencies
```bash
pip install requests beautifulsoup4 pandas python-dotenv
```

### ⚙️ Environment Setup
Create a `.env` file **inside `Part-B/`** .  
Add your Gemini API key:
```
GEMINI_API_KEY=your_actual_api_key_here
```

### ▶️ How to Run
1. Add URLs in `urls.txt` (one per line).  
2. Run:
   ```bash
   cd Part-B
   python3 scrape_summarize.py
   ```
3. Output file:  
   ```
   scraped_summary.csv
   ```

### 🧠 Assumptions
- A valid Gemini API key is available via Google AI Studio.  
- The script uses **Gemini 2.5 Flash** model .  
- Internet connection is required for both scraping and summarization.

### ⚡ Error Handling  
- Stores all summaries or error messages in the output CSV.

---

## 🌐 PART C — React Frontend Visualization

### 🎯 Objective
Build a simple React dashboard to view and filter the summarized CSV data.

### 🧰 Dependencies
Make sure Node.js and npm are installed.  
Inside `part-c-frontend/`, install required packages:
```bash
cd part-c-frontend
npm install
npm install papaparse
```

### ▶️ How to Run
```bash
npm start
```
Then open your browser at:
👉 http://localhost:3000

### 📊 Features
- Displays CSV data in a clean table format  
- Includes a search/filter box  
- Has a refresh button to reload CSV data  
- Loads `scraped_summary.csv` from `/public` folder

### 🧠 Assumptions
- The CSV (`scraped_summary.csv`) generated from Part B is copied to:
  ```
  part-c-frontend/public/
  ```

---

## 🔒 Security Notes

- The `.env` file (containing the API key) **is not uploaded**.  
- Sensitive and rebuildable files are excluded using `.gitignore`:
  ```
  .env
  venv/
  node_modules/
  __pycache__/
  package-lock.json
  package.json
  ```

---

## ✅ Summary of Deliverables

| Part | Description | Output File |
|------|--------------|--------------|
| A | Data Cleaning & Validation | `output_summary.csv` |
| B | Web Scraping + Gemini Summarization | `scraped_summary.csv` |
| C | React Dashboard Visualization | Web UI (localhost:3000) |

---

## 💬 Author
**Palak Gupta**  
AI Research Intern Candidate — SimplifiIQ (2025)
