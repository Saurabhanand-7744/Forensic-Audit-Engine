An automated financial anomaly detection system built with FastAPI, MongoDB, and Scikit-Learn.

- **Anomaly Detection:** Uses Isolation Forest to find outliers in transaction data.
- **Explainable AI (XAI):** Integrated SHAP to explain *why* a transaction was flagged.
- **Async API:** High-performance endpoints built with FastAPI.
- **Containerized:** Fully Dockerized for "plug-and-play" deployment.
- **Tested:** Robust test suite using Pytest.

- **Backend:** Python (FastAPI)
- **Database:** MongoDB
- **AI/ML:** Scikit-Learn, SHAP
- **DevOps:** Docker, Pytest

1. **Docker:** `docker build -t forensic-auditor-app .`
2. **Run:** `docker run -p 8000:8000 forensic-auditor-app`
3. **Docs:** Access `http://localhost:8000/docs` for interactive API testing.