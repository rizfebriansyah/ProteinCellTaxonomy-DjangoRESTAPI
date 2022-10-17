from rest_framework import serializers
from .models import Pfam, Protein, Domain, Organism


class PfamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pfam
        fields = ['domain_id', 'domain_description']


class DomainSerializer(serializers.ModelSerializer):
    pfam_id = PfamSerializer()

    class Meta:
        model = Domain
        fields = ['pfam_id', 'description', 'start', 'stop']


class DomainConciseSerializer(serializers.ModelSerializer):
    pfam_id = PfamSerializer()

    class Meta:
        model = Domain
        fields = ['id', 'pfam_id']


class OrganismSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organism
        fields = ['taxa_id', 'clade', 'genus', 'species']
        extra_kwargs = {'taxa_id': {'validators': []}}


class ProteinSerializer(serializers.ModelSerializer):
    domains = DomainSerializer(source='domain_set', many=True)
    taxonomy = OrganismSerializer()

    class Meta:
        model = Protein
        fields = ['protein_id', 'sequence', 'taxonomy', 'length', 'domains']


class ProteinListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Protein
        fields = ['id', 'protein_id']


class ProteinCreationSerializer(serializers.ModelSerializer):
    taxonomy = OrganismSerializer()

    class Meta:
        model = Protein
        fields = ['protein_id', 'sequence', 'taxonomy', 'length']

    def create(self, validated_data):
        organism_data = validated_data.pop('taxonomy')
        protein = Protein(taxonomy=Organism.objects.get(taxa_id=organism_data['taxa_id']), **validated_data)
        protein.save()
        return protein
