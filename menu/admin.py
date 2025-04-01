from django.contrib import admin
from .models import *

admin.site.register(Restaurant)
admin.site.register(Plat)
admin.site.register(CategoriePlat)
admin.site.register(Menu)
admin.site.register(Boisson)
admin.site.register(CategorieBoisson)
admin.site.register(AccompagnementBoisson)
admin.site.register(AccompagnementPlat)


