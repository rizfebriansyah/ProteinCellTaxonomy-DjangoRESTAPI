from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Protein, Pfam, Domain, Organism
from .serializers import ProteinSerializer, PfamSerializer, ProteinListSerializer, DomainConciseSerializer, \
    ProteinCreationSerializer


@api_view(['GET'])
def protein_detail(request, protein_id):
    if request.method == 'GET':
        # get the protein using the protein_id
        try:
            protein = Protein.objects.get(protein_id=protein_id)
        except Protein.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        # serialize protein
        serializer = ProteinSerializer(instance=protein)

        # return the response
        return Response(serializer.data)


@api_view(['POST'])
def protein_add(request):
    if request.method == 'POST':
        serializer = ProteinCreationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def pfam_detail(request, domain_id):
    if request.method == 'GET':
        # get the pfam using the domain_id
        try:
            pfam = Pfam.objects.get(domain_id=domain_id)
        except Pfam.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        # serialize the pfam
        serializer = PfamSerializer(instance=pfam)

        # return the response
        return Response(serializer.data)


@api_view(['GET'])
def proteins_list(request, taxonomy_id):
    if request.method == 'GET':
        # get the organism using the taxonomy_id
        try:
            organism = Organism.objects.get(taxa_id=taxonomy_id)
        except Organism.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        # get the proteins that belong to the organism
        proteins = Protein.objects.filter(taxonomy=organism)

        # serialize the proteins
        serializer = ProteinListSerializer(instance=proteins, many=True)

        # return the response
        return Response(serializer.data)


@api_view(['GET'])
def domains_list(request, taxonomy_id):
    if request.method == 'GET':
        # get the organism using the taxonomy_id
        try:
            organism = Organism.objects.get(taxa_id=taxonomy_id)
        except Organism.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        # get the proteins that belong to the organism
        proteins = Protein.objects.filter(taxonomy=organism)

        # get all the domains that are part of the proteins
        domains = Domain.objects.filter(protein_id__in=proteins)

        # serialize the domains
        serializer = DomainConciseSerializer(instance=domains, many=True)

        # return the response
        return Response(serializer.data)


@api_view(['GET'])
def domain_coverage(request, protein_id):
    if request.method == 'GET':
        # get the protein using the protein_id
        try:
            protein = Protein.objects.get(protein_id=protein_id)
        except Protein.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        # return the response with the protein's coverage
        return Response({'coverage': protein.coverage})
