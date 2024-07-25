import requests
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
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
        
        baseseveritys = cve.get('metrics', {}).get('cvssMetricV2', [])
         
        if baseseveritys:
            for baseSeverity in baseseveritys:
                severity = baseSeverity["baseSeverity"]
                exploitability_score = baseSeverity["exploitabilityScore"]
                impact_score = baseSeverity["impactScore"]
        else:
            severity = 'UNKNOWN'
            exploitability_score = 0
            impact_score = 0

        base_score = metrics.get('baseScore', 0)
        

        try:
            published_date = parse_datetime(cve.get('published', ''))
            last_modified_date = parse_datetime(cve.get('lastModified', ''))

            if published_date:
                published_date = make_aware(published_date)
            if last_modified_date:
                last_modified_date = make_aware(last_modified_date)

            Vulnerability.objects.update_or_create(
                cve_id=cve.get('id', ''),
                defaults={
                    'source_identifier': cve.get('sourceIdentifier', ''),
                    'published': published_date,
                    'last_modified': last_modified_date,
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
