import json, os

def update_synthesis(drift):
    if not drift:
        return

    trend = sum(drift[-10:])/len(drift[-10:]) if len(drift)>=10 else sum(drift)/len(drift)

    os.makedirs('tesseract/synthesis', exist_ok=True)
    with open('tesseract/synthesis/heuristics.json','w') as f:
        json.dump({'recent_drift_average':trend},f,indent=2)
