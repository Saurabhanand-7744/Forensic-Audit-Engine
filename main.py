import logging
from src.etl_pipeline import run_etl
from src.ml_engine import detect_and_explain_anomalies


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def start_audit_pipeline():
    logging.info("--- Phase 1: Ingesting Data into MongoDB ---")
    run_etl('Cars_data.csv')

    logging.info("--- Phase 2: Running ML Audit & Explainability ---")
    detect_and_explain_anomalies()

    logging.info("--- Forensic Audit System Task Completed ---")

if __name__ == "__main__":
    start_audit_pipeline()
