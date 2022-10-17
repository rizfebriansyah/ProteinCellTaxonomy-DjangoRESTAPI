import factory.django

from .models import *


class PfamFactory(factory.django.DjangoModelFactory):
    domain_id = "PF02800"
    domain_description = "Glyceraldehyde 3-phosphate dehydrogenase catalytic domain"

    class Meta:
        model = Pfam


class OrganismFactory(factory.django.DjangoModelFactory):
    taxa_id = 568076
    clade = "E"
    genus = "Metarhizium"
    species = "robertsii"

    class Meta:
        model = Organism


class ProteinFactory(factory.django.DjangoModelFactory):
    protein_id = "A0A014PQC0"
    sequence = "MAPVKVGINGFGRIGRIVFRNAAEHPEIEV"
    taxonomy = factory.SubFactory(OrganismFactory)
    length = len(sequence)

    class Meta:
        model = Protein


class DomainFactory(factory.django.DjangoModelFactory):
    pfam_id = factory.SubFactory(PfamFactory)
    description = "Glyceraldehyde3-phosphatedehydrogenase: C-terminaldomain"
    start = 1
    stop = 3
    protein_id = factory.SubFactory(ProteinFactory)

    class Meta:
        model = Domain
