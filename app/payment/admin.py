import csv
import datetime
from django.http import HttpResponse

from django.contrib import admin

# Register your models here.
from .models import Transaction, Payment


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = f"attachment; filename={opts.verbose_name}.csv"
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = content_disposition
    writer = csv.writer(response)
    fields = [
        field
        for field in opts.get_fields()
        if not field.many_to_many and not field.one_to_many
    ]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime("%d/%m/%Y")
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = "Export to CSV"


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["agent", "account", "concept", "amount", "kind", "timestamp"]
    actions = [export_to_csv]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["business", "card", "amount", "kind", "timestamp"]
    actions = [export_to_csv]
