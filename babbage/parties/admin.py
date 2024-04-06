from django.contrib import admin

from .models import Person
admin.site.register(Person)

from .models import Source
admin.site.register(Source)

from .models import Party
admin.site.register(Party)

from .models import Guest
admin.site.register(Guest)

