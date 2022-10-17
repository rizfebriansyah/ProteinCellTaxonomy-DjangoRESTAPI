import json

from django.urls import reverse
from rest_framework.test import APITestCase

from .models import *
from .model_factories import ProteinFactory, PfamFactory, OrganismFactory, DomainFactory
from .serializers import PfamSerializer, DomainSerializer, DomainConciseSerializer, OrganismSerializer, \
    ProteinSerializer, ProteinListSerializer


# test API endpoints
class ProteinDetailTest(APITestCase):
    def setUp(self):
        ProteinFactory.create(protein_id="protein1")
        self.good_url = reverse("protein_api", kwargs={"protein_id": "protein1"})
        self.bad_url = reverse("protein_api", kwargs={"protein_id": "blah-blah-blah"})

    def tearDown(self):
        Organism.objects.all().delete()
        Protein.objects.all().delete()
        Domain.objects.all().delete()
        Pfam.objects.all().delete()

    def test_proteinDetailReturnSuccess(self):
        response = self.client.get(self.good_url)
        data = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertTrue("protein_id" in data)
        self.assertEquals(data["protein_id"], "protein1")

    def test_proteinDetailReturnFailure(self):
        response = self.client.get(self.bad_url)
        self.assertEquals(response.status_code, 404)


class PfamDetailTest(APITestCase):
    def setUp(self):
        PfamFactory.create(domain_id="domain123")
        self.good_url = reverse("pfam_api", kwargs={"domain_id": "domain123"})
        self.bad_url = reverse("pfam_api", kwargs={"domain_id": "domain999"})

    def tearDown(self):
        Organism.objects.all().delete()
        Protein.objects.all().delete()
        Domain.objects.all().delete()
        Pfam.objects.all().delete()

    def test_pfamDetailReturnSuccess(self):
        response = self.client.get(self.good_url)
        data = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertTrue("domain_id" in data)
        self.assertEquals(data["domain_id"], "domain123")

    def test_pfamDetailReturnFailure(self):
        response = self.client.get(self.bad_url)
        self.assertEquals(response.status_code, 404)


class ProteinsListTest(APITestCase):
    def setUp(self):
        organism = OrganismFactory.create(taxa_id=1234)
        ProteinFactory.create(taxonomy=organism, protein_id="protein1")
        ProteinFactory.create(taxonomy=organism, protein_id="protein2")

        self.good_url = reverse("proteins_api", kwargs={"taxonomy_id": 1234})
        self.bad_url = reverse("proteins_api", kwargs={"taxonomy_id": 9999})

    def tearDown(self):
        Organism.objects.all().delete()
        Protein.objects.all().delete()
        Domain.objects.all().delete()
        Pfam.objects.all().delete()

    def test_proteinListReturnSuccess(self):
        response = self.client.get(self.good_url)
        data = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(len(data), 2)
        self.assertEquals(data[0]["protein_id"], "protein1")
        self.assertEquals(data[1]["protein_id"], "protein2")

    def test_proteinListReturnFailure(self):
        response = self.client.get(self.bad_url)
        self.assertEquals(response.status_code, 404)


class DomainsListTest(APITestCase):
    def setUp(self):
        organism = OrganismFactory.create(taxa_id=1234)
        protein1 = ProteinFactory.create(taxonomy=organism, protein_id="protein1")
        protein2 = ProteinFactory.create(taxonomy=organism, protein_id="protein2")
        pfam1 = PfamFactory(domain_id="domain1")
        pfam2 = PfamFactory(domain_id="domain2")
        DomainFactory.create(protein_id=protein1, pfam_id=pfam1)
        DomainFactory.create(protein_id=protein2, pfam_id=pfam2)

        self.good_url = reverse("pfams_api", kwargs={"taxonomy_id": 1234})
        self.bad_url = reverse("pfams_api", kwargs={"taxonomy_id": 9999})

    def tearDown(self):
        Organism.objects.all().delete()
        Protein.objects.all().delete()
        Domain.objects.all().delete()
        Pfam.objects.all().delete()

    def test_proteinListReturnSuccess(self):
        response = self.client.get(self.good_url)
        data = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(len(data), 2)
        self.assertEquals(data[0]["pfam_id"]["domain_id"], "domain1")
        self.assertEquals(data[1]["pfam_id"]["domain_id"], "domain2")

    def test_proteinListReturnFailure(self):
        response = self.client.get(self.bad_url)
        self.assertEquals(response.status_code, 404)


class DomainCoverageTest(APITestCase):
    def setUp(self):
        protein = ProteinFactory.create(protein_id="protein123", length=100)
        DomainFactory.create(protein_id=protein, start=0, stop=10)
        self.good_url = reverse("coverage_api", kwargs={"protein_id": "protein123"})
        self.bad_url = reverse("coverage_api", kwargs={"protein_id": "protein999"})

    def tearDown(self):
        Organism.objects.all().delete()
        Protein.objects.all().delete()
        Domain.objects.all().delete()
        Pfam.objects.all().delete()

    def test_proteinListReturnSuccess(self):
        response = self.client.get(self.good_url)
        data = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(data["coverage"], 0.1)

    def test_proteinListReturnFailure(self):
        response = self.client.get(self.bad_url)
        self.assertEquals(response.status_code, 404)


# test serializers
class PfamSerializerTest(APITestCase):
    def setUp(self):
        pfam1 = PfamFactory.create(domain_id="domain123", domain_description="desc123")
        serializer = PfamSerializer(instance=pfam1)
        self.data = serializer.data

    def tearDown(self):
        Organism.objects.all().delete()
        Protein.objects.all().delete()
        Domain.objects.all().delete()
        Pfam.objects.all().delete()

    def test_pfamSerializerKeys(self):
        self.assertEquals(set(self.data.keys()), {"domain_id", "domain_description"})

    def test_pfamSerializerDomainId(self):
        self.assertEquals(self.data["domain_id"], "domain123")

    def test_pfamSerializerDomainDesc(self):
        self.assertEquals(self.data["domain_description"], "desc123")


class DomainSerializerTest(APITestCase):
    def setUp(self):
        domain1 = DomainFactory.create()
        serializer = DomainSerializer(instance=domain1)
        self.data = serializer.data

    def tearDown(self):
        Organism.objects.all().delete()
        Protein.objects.all().delete()
        Domain.objects.all().delete()
        Pfam.objects.all().delete()

    def test_domainSerializerKeys(self):
        self.assertEquals(set(self.data.keys()), {"pfam_id", "description", "start", "stop"})

    def test_domainSerializerPfamId(self):
        self.assertEquals(self.data["pfam_id"]["domain_id"], "PF02800")
        self.assertEquals(self.data["pfam_id"]["domain_description"],
                          "Glyceraldehyde 3-phosphate dehydrogenase catalytic domain")

    def test_domainSerializerDesc(self):
        self.assertEquals(self.data["description"], "Glyceraldehyde3-phosphatedehydrogenase: C-terminaldomain")

    def test_domainSerializerStartStop(self):
        self.assertEquals(self.data["start"], 1)
        self.assertEquals(self.data["stop"], 3)


class DomainConciseSerializerTest(APITestCase):
    def setUp(self):
        domain1 = DomainFactory.create(id=1)
        serializer = DomainConciseSerializer(instance=domain1)
        self.data = serializer.data

    def tearDown(self):
        Organism.objects.all().delete()
        Protein.objects.all().delete()
        Domain.objects.all().delete()
        Pfam.objects.all().delete()

    def test_domainConciseSerializerKeys(self):
        self.assertEquals(set(self.data.keys()), {"id", "pfam_id"})

    def test_domainSerializerId(self):
        self.assertEquals(self.data["id"], 1)

    def test_domainSerializerPfamId(self):
        self.assertEquals(self.data["id"], 1)
        self.assertEquals(self.data["pfam_id"]["domain_id"], "PF02800")
        self.assertEquals(self.data["pfam_id"]["domain_description"],
                          "Glyceraldehyde 3-phosphate dehydrogenase catalytic domain")


class OrganismSerializerTest(APITestCase):
    def setUp(self):
        organism1 = OrganismFactory.create()
        serializer = OrganismSerializer(instance=organism1)
        self.data = serializer.data

    def tearDown(self):
        Organism.objects.all().delete()
        Protein.objects.all().delete()
        Domain.objects.all().delete()
        Pfam.objects.all().delete()

    def test_OrganismSerializerKeys(self):
        self.assertEquals(set(self.data.keys()), {"taxa_id", "clade", "genus", "species"})

    def test_OrganismSerializerTaxaId(self):
        self.assertEquals(self.data["taxa_id"], 568076)

    def test_OrganismSerializerClade(self):
        self.assertEquals(self.data["clade"], "E")

    def test_OrganismSerializerGenus(self):
        self.assertEquals(self.data["genus"], "Metarhizium")

    def test_OrganismSerializerSpecies(self):
        self.assertEquals(self.data["species"], "robertsii")


class ProteinSerializerTest(APITestCase):
    def setUp(self):
        protein1 = ProteinFactory.create()
        DomainFactory(protein_id=protein1)
        serializer = ProteinSerializer(instance=protein1)
        self.data = serializer.data

    def tearDown(self):
        Organism.objects.all().delete()
        Protein.objects.all().delete()
        Domain.objects.all().delete()
        Pfam.objects.all().delete()

    def test_ProteinSerializerKeys(self):
        self.assertEquals(set(self.data.keys()), {"protein_id", "sequence", "taxonomy", "length", "domains"})

    def test_ProteinSerializerProteinId(self):
        self.assertEquals(self.data["protein_id"], "A0A014PQC0")

    def test_ProteinSerializerSequence(self):
        self.assertEquals(self.data["sequence"], "MAPVKVGINGFGRIGRIVFRNAAEHPEIEV")

    def test_ProteinSerializerTaxonomy(self):
        self.assertEquals(self.data["taxonomy"]["taxa_id"], 568076)
        self.assertEquals(self.data["taxonomy"]["clade"], "E")
        self.assertEquals(self.data["taxonomy"]["genus"], "Metarhizium")
        self.assertEquals(self.data["taxonomy"]["species"], "robertsii")

    def test_ProteinSerializerLength(self):
        self.assertEquals(self.data["length"], 30)

    def test_ProteinSerializerDomains(self):
        self.assertEquals(len(self.data["domains"]), 1)
        self.assertEquals(self.data["domains"][0]["pfam_id"]["domain_id"], "PF02800")
        self.assertEquals(self.data["domains"][0]["pfam_id"]["domain_description"],
                          "Glyceraldehyde 3-phosphate dehydrogenase catalytic domain")
        self.assertEquals(self.data["domains"][0]["description"],
                          "Glyceraldehyde3-phosphatedehydrogenase: C-terminaldomain")
        self.assertEquals(self.data["domains"][0]["start"], 1)
        self.assertEquals(self.data["domains"][0]["stop"], 3)


class ProteinListSerializerTest(APITestCase):
    def setUp(self):
        organism1 = OrganismFactory.create()
        protein1 = ProteinFactory.create(id=1, protein_id="protein1", taxonomy=organism1)
        serializer = ProteinListSerializer(instance=[protein1], many=True)
        self.data = serializer.data

    def tearDown(self):
        Organism.objects.all().delete()
        Protein.objects.all().delete()
        Domain.objects.all().delete()
        Pfam.objects.all().delete()

    def test_ProteinListSerializerLength(self):
        self.assertEquals(len(self.data), 1)

    def test_ProteinListSerializerKeys(self):
        self.assertEquals(set(self.data[0].keys()), {"id", "protein_id"})

    def test_ProteinListSerializerId(self):
        self.assertEquals(self.data[0]["id"], 1)

    def test_ProteinListSerializerProteinId(self):
        self.assertEquals(self.data[0]["protein_id"], "protein1")


