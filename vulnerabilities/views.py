from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.http import Http404
from rest_framework.decorators import api_view
from vulnerabilities.interface_adapters.controller.VulnerabilityControl import ControlVulnerability
from vulnerabilities.serializers.serializers import VulnerabilityDataClassSerializer, CountVulnerabilityDataClassSerializer
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

@api_view(['POST'])
def create_vulnerability(request):
    control = ControlVulnerability()
    item = request.data  # Cambiado a request.data para obtener datos del cuerpo de la solicitud
    logger.info(f"Solicitud a la ruta /create_vulnerability.\nData enviada: {item}\n")
    return control.agg_vulnerability(item.get('cve', {}))

@api_view(['GET'])
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

@api_view(['GET'])
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

@api_view(['GET'])
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
