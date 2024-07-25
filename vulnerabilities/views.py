from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.http import Http404
from rest_framework.decorators import api_view
from vulnerabilities.interface_adapters.controller.VulnerabilityControl import ControlVulnerability
from vulnerabilities.serializers.serializers import VulnerabilityDataClassSerializer, CountVulnerabilityDataClassSerializer


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi 
from vulnerabilities.interface_adapters.dependencies import openapidoc
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

import logging
from logging.handlers import TimedRotatingFileHandler

# Configuración del logger
log_formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
log_handler = TimedRotatingFileHandler(
    filename='logs/vulnerability/vulnerability.log',
    when='D',
    interval=1,
)
log_handler.setFormatter(log_formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)

notfound_message = "No vulnerabilities found."


@swagger_auto_schema(
    method='get',
    responses={
        200: openapi.Response(
            description="Lista de vulnerabilidades",
            examples={ 
                "application/json":  openapidoc.vulnerability_responses
            }
        ),
        status.HTTP_404_NOT_FOUND: notfound_message
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all(request):
    control = ControlVulnerability()
    try:
        vulnerabilities = control.get_all_vulnerability()
        serializer = VulnerabilityDataClassSerializer(vulnerabilities, many=True)
        logger.info("Solicitud a la ruta /vulnerabilities.\n")
        return Response(serializer.data)
    except Http404:
        logger.error(notfound_message)
        raise NotFound(notfound_message)


@swagger_auto_schema(
    method='get',
    description="Lista de vulnerabilidades que excluyen las fijadas",
    responses={
        200: openapi.Response(
            description="Lista de vulnerabilidades que excluyen las fijadas",
            examples={ 
                "application/json":  openapidoc.vulnerability_excluding_fixed
            }
        ),
        status.HTTP_404_NOT_FOUND: notfound_message
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_queryset(request):
    control = ControlVulnerability()
    try:
        vulnerabilities = control.get_queryset()
        serializer = VulnerabilityDataClassSerializer(vulnerabilities, many=True)
        logger.info("Solicitud a la ruta /vulnerabilities/excluding-fixed.\n")
        return Response(serializer.data)
    except Http404:
        logger.error(notfound_message)
        raise NotFound(notfound_message)



@swagger_auto_schema(
    method='get',
    responses={
        200: openapi.Response(
            description="Lista de vulnerability severity summary",
            examples={ 
                "application/json":  openapidoc.vulnerabilities_summary
            }
        ),
        status.HTTP_404_NOT_FOUND: notfound_message
    }
)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vulnerability_severity_summary(request):
    control = ControlVulnerability()
    try:
        vulnerabilities = control.get_count_vulnerability()
        serializer = CountVulnerabilityDataClassSerializer(vulnerabilities, many=True)
        logger.info("Solicitud a la ruta /vulnerabilities/summary.\n")
        return Response(serializer.data)
    except Http404:
        logger.error(notfound_message)
        raise NotFound(notfound_message)
