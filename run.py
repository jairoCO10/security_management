import requests
from django.utils.dateparse import parse_datetime
from vulnerabilities.models import Vulnerability

def fetch_and_save_vulnerabilities():
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    params = {"resultsPerPage": 2000}
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Error: No se pudo obtener datos. Código de estado: {response.status_code}")
        return

    data = response.json()

    for item in data.get('vulnerabilities', []):
        cve = item.get('cve', {})
        metrics = cve.get('metrics', {}).get('cvssMetricV2', [{}])[0].get('cvssData', {})
        descriptions = cve.get('descriptions', [])

        description_en = next((desc['value'] for desc in descriptions if desc['lang'] == 'en'), '')
        description_es = next((desc['value'] for desc in descriptions if desc['lang'] == 'es'), '')

        # Extraer datos con un manejo de excepciones
        severity = metrics.get('baseSeverity', 'UNKNOWN')
        base_score = metrics.get('baseScore', 0)
        exploitability_score = metrics.get('exploitabilityScore', 0)
        impact_score = metrics.get('impactScore', 0)

        try:
            Vulnerability.objects.update_or_create(
                cve_id=cve.get('id', ''),
                defaults={
                    'source_identifier': cve.get('sourceIdentifier', ''),
                    'published': parse_datetime(cve.get('published', '')),
                    'last_modified': parse_datetime(cve.get('lastModified', '')),
                    'vuln_status': cve.get('vulnStatus', ''),
                    'description_en': description_en,
                    'description_es': description_es,
                    'severity': severity,
                    'base_score': base_score,
                    'exploitability_score': exploitability_score,
                    'impact_score': impact_score,
                }
            )
        except Exception as e:
            print(f"Error al guardar CVE {cve.get('id', '')}: {e}")

fetch_and_save_vulnerabilities()
