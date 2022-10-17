import os
import sys
import django
import csv

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, "bioweb"))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bioweb.settings')
django.setup()

from api.models import Organism, Protein, Domain, Pfam

# clear existing data in the models
Organism.objects.all().delete()
Protein.objects.all().delete()
Domain.objects.all().delete()
Pfam.objects.all().delete()
print('[!] Deleted existing data in model')

# to contain the information from the csv files
pfams = []
sequences = {}
organisms = {}
proteins = {}
domains = []

# read csv files
with open('pfam_descriptions.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        pfams.append(row)

with open('data_sequences.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        sequences[row[0]] = row[1]

with open('data_set.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        organisms[row[1]] = ([row[2], row[3].split()[0], row[3].split()[1]])
        proteins[row[0]] = [sequences.get(row[0]), row[1], row[8]]
        domains.append([row[5], row[4], row[6], row[7], row[0]])
print('[!] Completed reading csv files!')

# save to database
Pfam.objects.bulk_create([Pfam(domain_id=x[0], domain_description=x[1]) for x in pfams])
Organism.objects.bulk_create([Organism(taxa_id=k, clade=v[0], genus=v[1], species=v[2]) for k, v in organisms.items()])
Protein.objects.bulk_create([Protein(protein_id=k, sequence=v[0], taxonomy=Organism.objects.filter(taxa_id=v[1]).first(), length=v[2]) for k, v in proteins.items()])
Domain.objects.bulk_create([Domain(pfam_id=Pfam.objects.filter(domain_id=x[0]).first(), description=x[1], start=x[2], stop=x[3], protein_id=Protein.objects.get(protein_id=x[4])) for x in domains])
print('[!] Completed inserting data to database!')
