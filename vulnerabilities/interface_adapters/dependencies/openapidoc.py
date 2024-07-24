from drf_yasg import openapi

create_fixed_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'cve_id': openapi.Schema(type=openapi.TYPE_STRING, description='ID de la vulnerabilidad')
    },
    required=['cve_id']
)

vulnerability_responses = {
    201: openapi.Response(
        description="Vulnerabilidad fijada creada exitosamente",
        examples=
            [
    {
        "cve_id": "CVE-2000-0564",
        "source_identifier": "cve@mitre.org",
        "published": "2000-05-29T04:00:00Z",
        "last_modified": "2008-09-10T19:05:03.040000Z",
        "vuln_status": "Analyzed",
        "description_en": "The guestbook CGI program in ICQ Web Front service for ICQ 2000a, 99b, and others allows remote attackers to cause a denial of service via a URL with a long name parameter.",
        "description_es": "",
        "severity": "MEDIUM",
        "base_score": 5.0,
        "exploitability_score": 10.0,
        "impact_score": 2.9,
        "created_at": "2024-07-24T16:58:07.852063Z"
    },
    {
        "cve_id": "CVE-2000-0461",
        "source_identifier": "cve@mitre.org",
        "published": "2000-05-29T04:00:00Z",
        "last_modified": "2008-09-10T19:04:43.587000Z",
        "vuln_status": "Analyzed",
        "description_en": "The undocumented semconfig system call in BSD freezes the state of semaphores, which allows local users to cause a denial of service of the semaphore system by using the semconfig call.",
        "description_es": "",
        "severity": "LOW",
        "base_score": 2.1,
        "exploitability_score": 3.9,
        "impact_score": 2.9,
        "created_at": "2024-07-24T16:58:07.848739Z"
    }
        ]
        
    ),
    400: "Error de validación"
}



vulnerability_excluding_fixed = {
    201: openapi.Response(
        description="Vulnerabilidad fijada  exitosamente",
        examples=
            [
    {
        "cve_id": "CVE-2000-0461",
        "source_identifier": "cve@mitre.org",
        "published": "2000-05-29T04:00:00Z",
        "last_modified": "2008-09-10T19:04:43.587000Z",
        "vuln_status": "Analyzed",
        "description_en": "The undocumented semconfig system call in BSD freezes the state of semaphores, which allows local users to cause a denial of service of the semaphore system by using the semconfig call.",
        "description_es": "",
        "severity": "LOW",
        "base_score": 2.1,
        "exploitability_score": 3.9,
        "impact_score": 2.9,
        "created_at": "2024-07-24T16:58:07.848739Z"
    }
        ]
        
    ),
    400: "Error de validación"
}


vulnerabilities_summary = {
    201: openapi.Response(
        description="Vulnerabilidad fijada creada exitosamente",
        examples=[
    {
        "severity": "HIGH",
        "count": 999
    },
    {
        "severity": "MEDIUM",
        "count": 747
    },
    {
        "severity": "LOW",
        "count": 220
    },
    {
        "severity": "UNKNOWN",
        "count": 34
    }
]
            
    ),
    400: "Error de validación"
}


