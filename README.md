AI-Powered Forensic Audit Engine
Detecting financial fraud in today’s digital world is like finding a needle in a haystack. I built this project to provide auditors with a "Smart Assistant" that can scan thousands of transactions in seconds and highlight suspicious patterns that manual checks often miss.

This tool doesn't just display data; it uses Machine Learning to pinpoint transactions that are "outliers" or abnormal based on historical patterns.
Key Highlights
Smart Red-Flagging: I implemented the Isolation Forest algorithm, which is highly effective at spotting outliers in financial datasets.

Explainable AI (XAI): Flagging a fraud isn't enough; you need to know why. I integrated SHAP to provide transparency into which features (like amount, location, or frequency) triggered the alert.

Live CSV Analysis: You can drag-and-drop any financial CSV into the sidebar. The FastAPI backend processes it instantly and updates the dashboard in real-time.

One-Click Excel Reports: Once the audit is done, you can export all findings into a professional Excel (.xlsx) report for management or senior stakeholders.
Tech Stack
I kept the architecture modular to ensure the system remains scalable:

Frontend: Streamlit (For a clean, interactive UI)

Backend: FastAPI (For high-speed, asynchronous processing)

Database: MongoDB (To store and manage audit logs)

AI/ML: Scikit-Learn & SHAP

DevOps: Docker (For easy, "plug-and-play" local setup)
