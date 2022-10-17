from django.db import models
from django.db.models import F, Sum


class Organism(models.Model):
    taxa_id = models.IntegerField(unique=True)
    clade = models.CharField(max_length=1)
    genus = models.CharField(max_length=256)
    species = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.taxa_id}"


class Protein(models.Model):
    protein_id = models.CharField(max_length=256, unique=True)
    sequence = models.CharField(max_length=40000, null=True)
    taxonomy = models.ForeignKey('Organism', null=True, on_delete=models.SET_NULL)
    length = models.IntegerField()

    @property
    def coverage(self):
        domains = self.domain_set
        return domains.annotate(coverage=(F('stop')-F('start'))).aggregate(total=Sum('coverage'))['total']/self.length

    def __str__(self):
        return self.protein_id


class Domain(models.Model):
    pfam_id = models.ForeignKey('Pfam', on_delete=models.CASCADE)
    description = models.CharField(max_length=256)
    start = models.IntegerField()
    stop = models.IntegerField()
    protein_id = models.ForeignKey('Protein', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.protein_id.protein_id} - {self.pfam_id}"


class Pfam(models.Model):
    domain_id = models.CharField(max_length=256, unique=True)
    domain_description = models.CharField(max_length=256)

    def __str__(self):
        return self.domain_id
