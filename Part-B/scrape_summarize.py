#!/usr/bin/env python3

import os
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(" GEMINI_API_KEY not found in .env file!")

GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={API_KEY}"

if not os.path.exists("urls.txt"):
    raise FileNotFoundError(" Please create 'urls.txt' with URLs (one per line).")

with open("urls.txt", "r") as f:
    urls = [u.strip() for u in f.readlines() if u.strip()]

data = []

for url in urls:
    print(f"\n🔍 Processing: {url}")
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")
        title = soup.title.string.strip() if soup.title and soup.title.string else "No title found"

        meta_tag = soup.find("meta", attrs={"name": "description"})
        meta_desc = meta_tag["content"].strip() if meta_tag and meta_tag.get("content") else "No meta description"

        paragraph = ""
        for p in soup.find_all("p"):
            text = p.get_text().strip()
            if len(text) > 40:
                paragraph = text
                break

        if paragraph:
            prompt = f"Summarize the following webpage content in 3 concise sentences:\n\n{paragraph[:2000]}"
            body = {"contents": [{"parts": [{"text": prompt}]}]}

            summary = None
            for attempt in range(3):  
                response = requests.post(GEMINI_ENDPOINT, json=body)
                if response.status_code == 200:
                    summary = response.json()["candidates"][0]["content"]["parts"][0]["text"]
                    break
                elif response.status_code == 503:
                    time.sleep(3)
                else:
                    summary = f"Gemini error: {response.text}"
                    break

            if not summary:
                summary = "Gemini unavailable after multiple attempts."
        else:
            summary = "No meaningful paragraph found to summarize."


        data.append({
            "url": url,
            "title": title,
            "meta_description": meta_desc,
            "ai_summary": summary
        })

    except Exception as e:
        print(f"⚠️ Error processing {url}: {e}")
        data.append({
            "url": url,
            "title": "Error",
            "meta_description": "Error",
            "ai_summary": str(e)
        })

df = pd.DataFrame(data)
df.to_csv("scraped_summary.csv", index=False, encoding="utf-8")

print("\n Done! Summaries saved in 'scraped_summary.csv'.")


