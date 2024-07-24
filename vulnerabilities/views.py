from django.shortcuts import render
from rest_framework.response import Response
# Create your views here.
from rest_framework.exceptions import NotFound
from django.http import Http404

from django.db.models import Count

from rest_framework.decorators import api_view
from vulnerabilities.interface_adapters.controller.VulnerabilityControl  import ControlVulnerability
from vulnerabilities.serializers.serializers import VulnerabilityDataClassSerializer, CountVulnerabilityDataClassSerializer


notfound= "No vulnerabilities found."

@api_view(['POST'])
async def create_vulnerability(request):
    control = ControlVulnerability()
    item = request
    return await control.agg_vulnerability(item.get('cve', {}))


@api_view(['GET'])
def get_all(request):
    control = ControlVulnerability()
    try:

        vulnerabilities = control.get_all_vulnerability()

        # Serializa los datos usando el serializador para dataclasses
        serializer = VulnerabilityDataClassSerializer(vulnerabilities, many=True)
        return Response(serializer.data)
    except Http404:
        raise NotFound(notfound)

@api_view(['GET'])
def get_queryset(request):
    control = ControlVulnerability()
    try:

        vulnerabilities = control.get_queryset()

        # Serializa los datos usando el serializador para dataclasses
        serializer = VulnerabilityDataClassSerializer(vulnerabilities, many=True)
        return Response(serializer.data)
    except Http404:
        raise NotFound(notfound)
    

@api_view(['GET'])
def vulnerability_severity_summary(request):
    control = ControlVulnerability()
    try:
        vulnerabilities = control.get_count_vulnerability()
        serializer = CountVulnerabilityDataClassSerializer(vulnerabilities, many=True)
        return Response(serializer.data)
    except Http404:
        raise NotFound(notfound)

