from django.urls import path
from . import api

urlpatterns = [
    path('protein/', api.protein_add, name='protein_add_api'),
    path('protein/<str:protein_id>', api.protein_detail, name='protein_api'),
    path('pfam/<str:domain_id>', api.pfam_detail, name='pfam_api'),
    path('proteins/<int:taxonomy_id>', api.proteins_list, name='proteins_api'),
    path('pfams/<int:taxonomy_id>', api.domains_list, name='pfams_api'),
    path('coverage/<str:protein_id>', api.domain_coverage, name='coverage_api'),
]
