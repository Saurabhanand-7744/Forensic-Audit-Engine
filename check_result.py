import pymongo
import pandas as pd

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["ForensicAuditDB"]
flagged = db["flagged_anomalies"]

results = flagged.find().limit(5)

print(f"{'Make':<10} | {'Model':<15} | {'MSRP':<10} | {'Audit Reason'}")
print("-" * 60)
for res in results:
    print(f"{res['Make']:<10} | {res['Model']:<15} | {res['MSRP']:<10} | {res['audit_reason']}")
