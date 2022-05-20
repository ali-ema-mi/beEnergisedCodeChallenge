from django.contrib import admin

from .models import *


class BaseAdmin(admin.ModelAdmin):
    """
    Defines common admin features among all models
    """
    save_on_top = True
    abstract = True
    list_per_page = 10

    def get_list_display_links(self, request, list_display):
        """
        Defines all models presented fields as clickable fields
        :return: all models presented fields
        """
        return self.get_list_display(request)


@admin.register(Invoice)
class InvoiceAdmin(BaseAdmin):
    list_display = ['meterStart', 'timestampStart', 'meterStop', 'timestampStop', 'price']
    list_filter = ['timestampStart', 'timestampStop']
    readonly_fields = ['price', ]
