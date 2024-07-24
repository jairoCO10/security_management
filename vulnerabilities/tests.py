from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from vulnerabilities.models import Vulnerability
import requests
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware

class VulnerabilityTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vulnerability_url = reverse('vulnerability-list')
        self.vulnerability_sumary_url = reverse('vulnerability-summary')
        self.vulnerability_excluding_fixed_url = reverse('vulnerability-excluding-fixed')

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
            # print("baseSeverity",metrics.get('baseSeverity'))
            
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

    def test_get_all_vulnerabilities(self):
        response = self.client.get(self.vulnerability_url)
        print(f"Status Code: {response.status_code}")
        print(f"Length of Response Data: {len(response.data)}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2000)


    def test_get_vulnerability_excluding(self):
        response = self.client.get(self.vulnerability_excluding_fixed_url)
        print(f"Status Code: {response.status_code}")
        print(f"Length of Response Data Excluding: {len(response.data)}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2000)
    

    def test_get_sumary(self):
        response = self.client.get(self.vulnerability_sumary_url)
        print("data",response.data )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

