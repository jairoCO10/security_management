from django.shortcuts import render
from rest_framework.response import Response
# Create your views here.

from rest_framework.decorators import api_view
from vulnerabilities.interface_adapters.controller.VulnerabilityControl  import ControlVulnerability
from vulnerabilities.serializers.serializers import VulnerabilityDataClassSerializer



@api_view(['POST'])
async def create_vulnerability(request):
    control = ControlVulnerability()
    item = request
    return await control.agg_vulnerability(item.get('cve', {}))


@api_view(['GET'])
def get_all(request):
    control = ControlVulnerability()
    vulnerabilities = control.get_all_vulnerability()

    # Serializa los datos usando el serializador para dataclasses
    serializer = VulnerabilityDataClassSerializer(vulnerabilities, many=True)
    return Response(serializer.data)


