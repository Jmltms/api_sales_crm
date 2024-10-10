"""
Django admin customization.
"""
import csv
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.models import LogEntry
from django.http import HttpResponse
from core import models


class ExportCsvMixin:

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response[
            'Content-Dispostion'
        ] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow(
                [getattr(obj, field) for field in field_names]
            )
            print(row)

        return response

    export_as_csv.short_description = "Export Selected"


class LogEntryAdmin(admin.ModelAdmin):
    list_display = [
        'content_type',
        'user',
        'action_time',
        'object_id',
        'object_repr',
        'action_flag',
        'change_message'
    ]

    readonly_fields = (
        'content_type',
        'user',
        'action_time',
        'object_id',
        'object_repr',
        'action_flag',
        'change_message'
    )
    search_fields = [
        'object_id',
        'object_repr',
        'change_message'
    ]

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def get_actions(self, request):
        actions = super(LogEntryAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


class UserAdmin(BaseUserAdmin):

    ordering = ['id']
    list_display = ['first_name', 'last_name', 'email', 'username']
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Personal Info'), {
            'fields': (
                'first_name',
                'middle_name',
                'last_name',
            )}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (
            _('Important dates'), {'fields': ('last_login',)},
        ),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'username',
                'password1',
                'password2',
                'first_name',
                'first_name',
                'last_name',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )


class AccountAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'first_name',
        'last_name',
        'employee_id',
        'email',
        'status',
        'type'
    ]

    raw_id_fields = ['user']

    search_fields = [
        'user__first_name',
        'user__last_name',
    ]

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    def email(self, obj):
        return obj.user.email


class IndustryAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'field'
    ]
    search_fields = [
        'name',
    ]


class CompanyInformationAdmin(admin.ModelAdmin):
    list_display = [
            'id',
            'industry',
            'name',
            'address',
            'company_size'
        ]

    search_fields = [
        'name'
    ]


class ClientAdmin(admin.ModelAdmin):
    list_display = [
            'id',
            'company',
            'first_name',
            'last_name',
            'phone_num',
            'tel_num',
            'email',
            'job_title',
            'department',
        ]

    search_fields = [
        'company__name',
        'first_name',
        'last_name',
    ]

    # def company(self, obj):
    #     return obj.company.name


class LeadInformationAdmin(admin.ModelAdmin):
    list_display = [
            'id',
            'client',
            'status',
            'lead_score',
            'status_label',
            'type',
            'source',
            'date_contacted',
            'date_close_deal',
            'remarks',
            'condition'
        ]

    search_fields = [
        'client__first_name',
        'client__last_name',
        'status',
    ]

    def client(obj, self):
        return "%s %s" % (
            obj.client.first_name,
            obj.client.first_name
        )


class LeadOwnernAdmin(admin.ModelAdmin):
    list_display = [
            'id',
            'account',
            'lead',
            'status',
            'date_handle',
            'date_completed',
        ]

    def lead(obj, self):
        return "%s %s" % (
            obj.lead.client.first_name,
            obj.lead.client.first_name
        )


class OwnerHistoryAdmin(admin.ModelAdmin):
    list_display = [
            'id',
            'last_owner',
            'lead_owner',
            'status',
            'date_handle',
            'date_transfer',
        ]

    def lead(obj, self):
        return "%s %s" % (
            obj.lead.client.first_name,
            obj.lead.client.first_name
        )


class NotesAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'lead_info',
        'status',
        'date_noted',
        'message'
    ]


class ActivityAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'lead_info',
        'status',
        'date_generated',
        'message',
        'owner'
    ]


class ServiceOfferedAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'description',
        'status'
    ]


class LeadServicesAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'service',
        'lead_info',
        'otf',
        'msf',
        'status',
        'revenue',
        'otf_payment'
    ]

    search_fields = [
        'lead_info__client__first_name'
    ]


class MonthlyTermsAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'lead_service',
        'month_start',
        'month_end',
        'date_start',
        'date_end'
    ]


class TermStatusAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'lead_service',
        'months',
        'date_pay',
        'date_unpay',
        'year',
        'status',
        'msf'
    ]


class ServiceHistoryAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'lead_service',
        'projected_otf',
        'projected_msf'
    ]


class ArchiveAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'lead_info',
        'date_deleted',
        'deleted_by'
    ]


class AattachmentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'lead_info',
        'date_inserted',
        'label',
        'status',
        'file',
        'uploaded_by'
    ]


class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'sender',
        'receiver',
        'status',
        'message',
        'subject',
        'date_deliver',
        'date_seen',
        'is_seen'
    ]


admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Account, AccountAdmin)
admin.site.register(models.Industry, IndustryAdmin)
admin.site.register(
    models.CompanyInformation,
    CompanyInformationAdmin
)
admin.site.register(models.Client, ClientAdmin)
admin.site.register(
    models.LeadInformation,
    LeadInformationAdmin
)
admin.site.register(
    models.LeadOwner,
    LeadOwnernAdmin
)
admin.site.register(
    models.OwnerHistory,
    OwnerHistoryAdmin
)
admin.site.register(
    models.Notes,
    NotesAdmin
)
admin.site.register(
    models.Activity,
    ActivityAdmin
)
admin.site.register(
    models.ServiceOffered,
    ServiceOfferedAdmin
)
admin.site.register(
    models.LeadServices,
    LeadServicesAdmin
)
admin.site.register(
    models.MonthlyTerms,
    MonthlyTermsAdmin
)
admin.site.register(
    models.TermStatus,
    TermStatusAdmin
)
admin.site.register(
    models.ServiceHistory,
    ServiceHistoryAdmin
)
admin.site.register(
    models.Archive,
    ArchiveAdmin
)
admin.site.register(
    models.Attachment,
    AattachmentAdmin
)
admin.site.register(
    models.Notification,
    NotificationAdmin
)
