# vulnerabilities/serializers.py
from rest_framework import serializers

class VulnerabilityDataClassSerializer(serializers.Serializer):
    cve_id = serializers.CharField()
    source_identifier = serializers.CharField()
    published = serializers.DateTimeField()
    last_modified = serializers.DateTimeField()
    vuln_status = serializers.CharField()
    description_en = serializers.CharField()
    description_es = serializers.CharField(allow_blank=True)
    severity = serializers.CharField()
    base_score = serializers.FloatField()
    exploitability_score = serializers.FloatField()
    impact_score = serializers.FloatField()
    created_at = serializers.DateTimeField()

class CountVulnerabilityDataClassSerializer(serializers.Serializer):
    severity = serializers.CharField()
    count = serializers.IntegerField()

