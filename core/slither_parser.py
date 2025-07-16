from typing import Dict, List, Any

def extract_findings_from_slither_json(slither_json: Dict[str, Any]) -> Dict[str, List[Dict]]:
    severity_buckets = {
        "High": [],
        "Medium": [],
        "Low": [],
        "Info": [],
        "Unknown": []
    }

    detectors = slither_json.get("results", {}).get("detectors", [])
    for item in detectors:
        title = item.get("check") or item.get("name", "Unknown Detector")
        impact = item.get("impact", "unknown").lower()
        confidence = item.get("confidence", "unknown")

        severity_map = {
            "high": "High",
            "medium": "Medium",
            "low": "Low",
            "informational": "Info"
        }
        severity = severity_map.get(impact, "Unknown")

        elements = item.get("elements", [])
        locations = []
        if elements:
            for elem in elements:
                source_mapping = elem.get("source_mapping", {})
                file_path = source_mapping.get("filename_short")
                lines = source_mapping.get("lines", [])
                locations.append(f"{file_path}:{lines[0] if lines else 'N/A'}")

        finding_info = {
            "title": title,
            "severity": severity,
            "confidence": confidence,
            "description": item.get("description", "").strip(),
            "location": ", ".join(locations) if locations else "N/A"
        }

        severity_buckets[severity].append(finding_info)

    return severity_buckets
