from django.db import models
from django.utils import timezone
# Create your models here.

class Vulnerability(models.Model):
    cve_id = models.CharField(max_length=20, unique=True)
    source_identifier = models.CharField(max_length=100)
    published = models.DateTimeField()
    last_modified = models.DateTimeField()
    vuln_status = models.CharField(max_length=50)
    description_en = models.TextField()
    description_es = models.TextField(null=True, blank=True)
    severity = models.CharField(max_length=20)
    base_score = models.FloatField()
    exploitability_score = models.FloatField()
    impact_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deactivate_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.cve_id
    
    def publish(self):
        self.last_modified = timezone.now()
        self.save()

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Vulnerability'
        verbose_name_plural = 'Vulnerabilitys'
