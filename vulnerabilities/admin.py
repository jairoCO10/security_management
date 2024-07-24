from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Vulnerability

@admin.register(Vulnerability)
class VulnerabilityAdmin(admin.ModelAdmin):
    list_display = ('cve_id', 'source_identifier', 'published', 'last_modified', 'vuln_status', 'severity', 'base_score',)
    search_fields = ('cve_id', 'description_en', 'description_es')
    list_filter = ('severity', 'vuln_status')
    # prepopulated_fields = {'slug': ('cve_id',)}
