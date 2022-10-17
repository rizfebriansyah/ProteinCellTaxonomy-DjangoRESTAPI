from django.contrib import admin

# Register your models here.
from .models import Protein, Organism, Domain, Pfam


class DomainAdmin(admin.ModelAdmin):
    pass


class ProteinAdmin(admin.ModelAdmin):
    pass


class OrganismAdmin(admin.ModelAdmin):
    pass


class PfamAdmin(admin.ModelAdmin):
    pass


admin.site.register(Organism, OrganismAdmin)
admin.site.register(Domain, DomainAdmin)
admin.site.register(Protein, ProteinAdmin)
admin.site.register(Pfam, PfamAdmin)
