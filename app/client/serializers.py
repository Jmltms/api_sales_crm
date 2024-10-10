from rest_framework import serializers
from core import models as core_models
from django.db.models import Q
from django.db.models import (
    Count, Case, When, IntegerField, Sum, FloatField
)
from datetime import datetime
from django.utils import timezone


ph_timezone = timezone.get_fixed_timezone(480)
current_time_ph = timezone.localtime(
    timezone.now(), ph_timezone
)


class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.Industry
        fields = '__all__'


class CompanyInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.CompanyInformation
        fields = [
            'id',
            'industry',
            'name',
            'address',
            'company_size'
        ]

    industry = serializers.SerializerMethodField(
        'fetch_industry'
    )

    def fetch_industry(obj):
        return obj.industry.name


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.Client
        fields = [
            'id',
            'company',
            'full_name',
            'phone_num',
            'tel_num',
            'email',
            'job_title',
            'department',
        ]

    company = serializers.SerializerMethodField(
        'fetch_company'
    )
    full_name = serializers.SerializerMethodField(
        'fetch_full_name'
    )

    def fetch_company(self, obj):
        return obj.company.name

    def fetch_full_name(self, obj):
        return "%s %s" % (obj.first_name, obj.last_name)


class LeadOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.LeadOwner
        fields = [
            'id',
            'owner',
            'lead',
            'date_handle',
            'date_completed'
        ]

    owner = serializers.SerializerMethodField(
        'fetch_owner'
    )
    lead = serializers.SerializerMethodField(
        'fetch_lead'
    )

    def fetch_owner(self, obj):
        result = None
        account = core_models.Account.objects.filter(
            account__id=obj.id
        ).first()

        if account.user:
            fname = account.user.first_name
            lname = account.user.last_name
            full_name = "%s %s" % (fname, lname)
            result = full_name
        return result

    def fetch_lead(self, obj):
        result = None
        lead = core_models.LeadInformation.objects.filter(
            lead__id=obj.id
        ).first()

        if lead.user:
            fname = lead.client.first_name
            lname = lead.client.last_name
            full_name = "%s %s" % (fname, lname)
            result = full_name
        return result


class OwnerHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.OwnerHistory
        fields = [
            'id',
            'owner',
            'lead_owner',
            'date_handle',
            'date_transfer',
            'status'
        ]

    owner = serializers.SerializerMethodField(
        'fetch_owner'
    )

    def fetch_owner(self, obj):
        return "%s %s" % (
            obj.user.first_name,
            obj.user.last_name
        )


class ServiceOfferedSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.ServiceOffered
        fields = [
            'id',
            'name',
            'description',
            'status'
        ]


class LeadInformationSerializer(serializers.ModelSerializer):
    full_name = ClientSerializer()
    email = ClientSerializer()
    phone_num = ClientSerializer()
    tel_num = ClientSerializer()
    department = ClientSerializer()
    job_title = ClientSerializer()
    company = ClientSerializer()
    owner = LeadOwnerSerializer()
    address = ClientSerializer()

    class Meta:
        model = core_models.LeadInformation
        fields = [
            'id',
            'full_name',
            'status',
            'lead_score',
            'status_label',
            'date_contacted',
            'date_close_deal',
            'type',
            'source'
        ]

    full_name = serializers.SerializerMethodField(
        'fetch_full_name'
    )

    def fetch_full_name(self, obj):
        return "%s %s" % (
            obj.client.first_name,
            obj.client.last_name
        )


class AllLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.LeadOwner
        fields = [
            'id',
            'client_id',
            'full_name',
            'email',
            'phone_num',
            'tel_num',
            'department',
            'company',
            'job_title',
            'owner',
            'address',
            'status',
            'lead_status',
            'date_completed',
            'remarks',
            'service',
            'rev',
            'lead_id',
        ]

    lead_id = serializers.SerializerMethodField(
        'fetch_lead_id'
    )

    full_name = serializers.SerializerMethodField(
        'fetch_full_name'
    )

    email = serializers.SerializerMethodField(
        'fetch_email'
    )

    phone_num = serializers.SerializerMethodField(
        'fetch_phone_num'
    )

    tel_num = serializers.SerializerMethodField(
        'fetch_tel_num'
    )

    department = serializers.SerializerMethodField(
        'fetch_department'
    )

    job_title = serializers.SerializerMethodField(
        'fetch_job_title'
    )

    company = serializers.SerializerMethodField(
        'fetch_company'
    )

    address = serializers.SerializerMethodField(
        'fetch_address'
    )
    owner = serializers.SerializerMethodField(
        'fetch_owner'
    )
    lead_status = serializers.SerializerMethodField(
        'fetch_lead_status'
    )
    remarks = serializers.SerializerMethodField(
        'fetch_remarks'
    )
    service = serializers.SerializerMethodField(
        'fetch_service'
    )
    rev = serializers.SerializerMethodField(
        'fetch_rev'
    )
    client_id = serializers.SerializerMethodField(
        'fetch_client_id'
    )

    def fetch_full_name(self, obj):
        return "%s %s" % (
            obj.lead.client.first_name,
            obj.lead.client.last_name
        )

    def fetch_email(self, obj):
        return obj.lead.client.email

    def fetch_phone_num(self, obj):
        return obj.lead.client.phone_num

    def fetch_tel_num(self, obj):
        return obj.lead.client.tel_num

    def fetch_department(self, obj):
        return obj.lead.client.department

    def fetch_job_title(self, obj):
        return obj.lead.client.job_title

    def fetch_company(self, obj):
        return obj.lead.client.company.name

    def fetch_address(self, obj):
        return obj.lead.client.company.address

    def fetch_lead_status(self, obj):
        return obj.lead.status

    def fetch_owner(self, obj):
        if obj.account and obj.account.user:
            fname =\
                obj.account.user.first_name\
                if obj.account.user.first_name else ''
            lname =\
                obj.account.user.last_name\
                if obj.account.user.last_name else ''
            return "%s %s" % (fname, lname)
        return ''

    def fetch_remarks(self, obj):
        return obj.lead.remarks

    def fetch_service(self, obj):
        result = ''
        lead_service = core_models.LeadServices.objects.filter(
            lead_info=obj.lead
        ).first()
        if lead_service:
            if lead_service.service:
                result = lead_service.service.id

        return result

    def fetch_rev(self, obj):
        result = 0
        lead_service = core_models.LeadServices.objects.filter(
            lead_info=obj.lead
        )

        for ls in lead_service:
            if ls.revenue is not None:
                result += ls.revenue
        return result or 0

    # def fetch_lead_id(self, obj):
    #     result = 0
    #     if obj.lead:
    #         result = obj.lead.id
    #     return result
    def fetch_lead_id(self, obj):
        return obj.lead.id

    def fetch_client_id(self, obj):
        return obj.lead.client.id


class LeadStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.LeadOwner
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_num',
            'tel_num',
            'department',
            'company',
            'job_title',
            'address',
            'status',
            'date_completed',

            'lead_status',
            'company_size',
            'industry',
            'owner',
            'status_label',
            'lead_type',
            'remarks',
            'status',
            'service',
            'client_id',
            'lead_id',
            'condition',
            'source'
        ]

    first_name = serializers.SerializerMethodField(
        'fetch_first_name'
    )
    last_name = serializers.SerializerMethodField(
        'fetch_last_name'
    )
    email = serializers.SerializerMethodField(
        'fetch_email'
    )
    phone_num = serializers.SerializerMethodField(
        'fetch_phone_num'
    )
    tel_num = serializers.SerializerMethodField(
        'fetch_tel_num'
    )
    department = serializers.SerializerMethodField(
        'fetch_department'
    )
    job_title = serializers.SerializerMethodField(
        'fetch_job_title'
    )
    company = serializers.SerializerMethodField(
        'fetch_company'
    )
    address = serializers.SerializerMethodField(
        'fetch_address'
    )
    owner = serializers.SerializerMethodField(
        'fetch_owner'
    )
    lead_status = serializers.SerializerMethodField(
        'fetch_lead_status'
    )
    company_size = serializers.SerializerMethodField(
        'fetch_company_size'
    )
    lead_type = serializers.SerializerMethodField(
        'fetch_lead_type'
    )
    industry = serializers.SerializerMethodField(
        'fetch_industry'
    )
    status_label = serializers.SerializerMethodField(
        'fetch_status_label'
    )
    remarks = serializers.SerializerMethodField(
        'fetch_remarks'
    )

    service = serializers.SerializerMethodField(
        'fetch_service'
    )

    client_id = serializers.SerializerMethodField(
        'fetch_client_id'
    )

    lead_id = serializers.SerializerMethodField(
        'fetch_lead_id'
    )
    condition = serializers.SerializerMethodField(
        'fetch_condition'
    )

    source = serializers.SerializerMethodField(
        'fetch_source'
    )

    def fetch_first_name(self, obj):
        return obj.lead.client.first_name

    def fetch_last_name(self, obj):
        return obj.lead.client.last_name

    def fetch_email(self, obj):
        return obj.lead.client.email

    def fetch_phone_num(self, obj):
        return obj.lead.client.phone_num\
            if obj.lead.client.phone_num else ''

    def fetch_tel_num(self, obj):
        return obj.lead.client.tel_num\
            if obj.lead.client.tel_num else ''

    def fetch_department(self, obj):
        return obj.lead.client.department\
            if obj.lead.client.department else ''

    def fetch_job_title(self, obj):
        return obj.lead.client.job_title\
            if obj.lead.client.job_title else ''

    def fetch_company(self, obj):
        return obj.lead.client.company.name\
            if obj.lead.client.company.name else ''

    def fetch_address(self, obj):
        return obj.lead.client.company.address\
            if obj.lead.client.company.address else ''

    def fetch_lead_status(self, obj):
        return obj.lead.status

    def fetch_company_size(self, obj):
        return obj.lead.client.company.company_size

    def fetch_type(self, obj):
        return obj.lead.type

    def fetch_industry(self, obj):
        industry_name = (
            obj.lead.client.company.industry.name
            if obj.lead and obj.lead.client
            and obj.lead.client.company
            and obj.lead.client.company.industry
            and obj.lead.client.company.industry.name
            else None
        )
        return industry_name

    def fetch_owner(self, obj):
        if obj.account and obj.account.user:
            fname =\
                obj.account.user.first_name\
                if obj.account.user.first_name else ''
            lname =\
                obj.account.user.last_name\
                if obj.account.user.last_name else ''
            return "%s %s" % (fname, lname)
        return ''

    def fetch_status_label(self, obj):
        return obj.lead.status_label

    def fetch_lead_type(self, obj):
        return obj.lead.type

    def fetch_remarks(self, obj):
        return obj.lead.remarks

    def fetch_service(self, obj):
        result = None
        lead_service = core_models.LeadServices.objects.filter(
            lead_info=obj.lead, status=1
        ).first()
        if lead_service:
            result = lead_service.service.id
            return result
        else:
            result = ''
            return result

    def fetch_client_id(self, obj):
        return obj.lead.client.id

    def fetch_lead_id(self, obj):
        return obj.lead.id

    def fetch_condition(self, obj):
        return obj.lead.condition

    def fetch_source(self, obj):
        return obj.lead.source


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.Notes
        fields = [
            'id',
            'message',
            'lead_info',
            'status',
            'date_noted',
        ]

    lead_info = serializers.SerializerMethodField(
        'fetch_lead_info'
    )

    def fetch_lead_info(self, obj):
        return "%s %s" % (
            obj.lead_info.client.first_name,
            obj.lead_info.client.last_name
        )


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.Activity
        fields = [
            'id',
            'message',
            'lead_info',
            'status',
            'date_generated',
            'owner'
        ]

    lead_info = serializers.SerializerMethodField(
        'fetch_lead_info'
    )

    def fetch_lead_info(self, obj):
        return "%s %s" % (
            obj.lead_info.client.first_name,
            obj.lead_info.client.last_name
        )


class LeadServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.LeadServices
        fields = [
            'id',
            'service',
            'lead_info',
            'otf',
            'msf',
            'status',
            'revenue'
        ]


class MonthlyTermsSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.MonthlyTerms
        fields = [
            'id',
            'lead_service',
            'month-start',
            'month_end',
            'date_start',
            'date_end',
        ]


class TermStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.TermStatus
        fields = [
            'id',
            'lead_service',
            'months',
            'date_pay',
            'date_unpay',
            'status',
            'msf'
        ]


class leadServiceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.LeadServices
        fields = [
            'id',
            'lead_info',
            'status_label',
            'otf',
            'msf',
            'status',
            'revenue',
            'month_start',
            'month_end',
            'date_start',
            'date_end',
            'service'
        ]

    month_start = serializers.SerializerMethodField(
        'fetch_month_start'
    )
    month_end = serializers.SerializerMethodField(
        'fetch_month_end'
    )
    date_start = serializers.SerializerMethodField(
        'fetch_date_start'
    )
    date_end = serializers.SerializerMethodField(
        'fetch_date_end'
    )
    status_label = serializers.SerializerMethodField(
        'fetch_status_label'
    )
    service = serializers.SerializerMethodField(
        'fetch_service'
    )

    def fetch_month_start(self, obj):
        result = None

        month_s = core_models.MonthlyTerms.objects.filter(
            lead_service=obj.id
        ).first()

        if month_s is not None:
            result = month_s.month_start
        return result

    def fetch_month_end(self, obj):
        result = None

        month_e = core_models.MonthlyTerms.objects.filter(
            lead_service=obj.id
        ).first()

        if month_e is not None:
            result = month_e.month_end
        return result

    def fetch_date_start(self, obj):
        result = None

        date_s = core_models.MonthlyTerms.objects.filter(
            lead_service=obj.id
        ).first()

        if date_s is not None:
            result = date_s.date_start
        return result

    def fetch_date_end(self, obj):
        result = None

        date_e = core_models.MonthlyTerms.objects.filter(
            lead_service=obj.id
        ).first()

        if date_e is not None:
            result = date_e.date_end
        return result

    def fetch_status_label(self, obj):
        return obj.lead_info.status_label

    def fetch_service(self, obj):
        return obj.service.name


class ArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.Archive
        fields = [
            'id',
            'lead_id',
            'client_id',
            'date_deleted',
            'deleted_by',
            'name',
            'owner',
            'email',

            'phone_num',
            'job_title',
            'company',
            'address',
            'remarks',
            'status'
        ]

    lead_id = serializers.SerializerMethodField(
        'fetch_lead_id'
    )
    client_id = serializers.SerializerMethodField(
        'fetch_client_id'
    )
    name = serializers.SerializerMethodField(
        'fetch_name'
    )
    owner = serializers.SerializerMethodField(
        'fetch_owner'
    )
    deleted_by = serializers.SerializerMethodField(
        'fetch_deleted_by'
    )
    email = serializers.SerializerMethodField(
        'fetch_email'
    )
    phone_num = serializers.SerializerMethodField(
        'fetch_phone_num'
    )
    job_title = serializers.SerializerMethodField(
        'fetch_job_title'
    )
    company = serializers.SerializerMethodField(
        'fetch_company'
    )
    address = serializers.SerializerMethodField(
        'fetch_address'
    )
    remarks = serializers.SerializerMethodField(
        'fetch_remarks'
    )
    status = serializers.SerializerMethodField(
        'fetch_status'
    )

    def fetch_lead_id(self, obj):
        return obj.lead_info.id

    def fetch_client_id(self, obj):
        return obj.lead_info.client.id

    def fetch_name(self, obj):
        return "%s %s" % (
            obj.lead_info.client.first_name,
            obj.lead_info.client.last_name
        )

    def fetch_owner(self, obj):
        owner = core_models.LeadOwner.objects.filter(
            lead=obj.lead_info
        ).first()
        if owner.account and owner.account.user:
            fname =\
                owner.account.user.first_name\
                if owner.account.user.first_name else ''
            lname =\
                owner.account.user.last_name\
                if owner.account.user.last_name else ''
            return "%s %s" % (fname, lname)
        return ''

    def fetch_deleted_by(self, obj):
        return "%s %s" % (
            obj.deleted_by.user.first_name,
            obj.deleted_by.user.last_name
        )

    def fetch_email(self, obj):
        return obj.lead_info.client.email

    def fetch_phone_num(self, obj):
        return obj.lead_info.client.phone_num

    def fetch_job_title(self, obj):
        return obj.lead_info.client.job_title

    def fetch_company(self, obj):
        return obj.lead_info.client.company.name

    def fetch_address(self, obj):
        return obj.lead_info.client.company.address

    def fetch_remarks(self, obj):
        return obj.lead_info.remarks

    def fetch_status(self, obj):
        return obj.lead_info.status


class DashboardTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.LeadInformation
        fields = [
            "id",
            "client_id",
            "client",
            "industry",
            "source",
            "service",
            "status",
            "otf",
            "msf",
            "annual_revenue",
            "revenue",
            "months",
            "otf_payment"
        ]

    client_id = serializers.SerializerMethodField(
        'fetch_client_id'
    )
    client = serializers.SerializerMethodField(
        'fetch_client'
    )
    industry = serializers.SerializerMethodField(
        'fetch_industry'
    )
    service = serializers.SerializerMethodField(
        'fetch_service'
    )
    otf = serializers.SerializerMethodField(
        'fetch_otf'
    )
    msf = serializers.SerializerMethodField(
        'fetch_msf'
    )
    annual_revenue = serializers.SerializerMethodField(
        'fetch_annual_revenue'
    )
    revenue = serializers.SerializerMethodField(
        'fetch_revenue'
    )
    months = serializers.SerializerMethodField(
        'fetch_months'
    )
    otf_payment = serializers.SerializerMethodField(
        'fetch_otf_payment'
    )

    def fetch_client_id(self, obj):
        return obj.client.id

    def fetch_client(self, obj):
        return "%s %s " % (
            obj.client.first_name,
            obj.client.last_name
        )

    def fetch_industry(self, obj):
        if obj.client.company.industry:
            return f"{obj.client.company.industry.name}"
        else:
            return ""

    def fetch_service(self, obj):
        result = ''
        service = core_models.LeadServices.objects.filter(
            lead_info=obj
        ).first()
        if service:
            if service.service:
                result = service.service.name

        return result

    def fetch_otf(self, obj):
        result = None
        service = core_models.LeadServices.objects.filter(
            lead_info=obj
        ).first()
        if service is None or not service.otf:
            result = ""
        else:
            result = service.otf
        return result

    def fetch_msf(self, obj):
        result = None
        service = core_models.LeadServices.objects.filter(
            lead_info=obj
        ).first()
        if service is None or not service.msf:
            result = ""
        else:
            result = service.msf
        return result

    def fetch_annual_revenue(self, obj):
        current_year = self.context.get('year')
        result = 0

        service = core_models.LeadServices.objects.filter(
            lead_info=obj,
        ).first()

        terms = core_models.TermStatus.objects.filter(
            lead_service=service,
            year=current_year
        )

        if service:
            if service.msf:
                if terms:
                    otf = service.otf or 0
                    msf = service.msf
                    len_terms = len(terms)
                    if service.otf_payment:
                        otf_year = service.otf_payment
                        str_year = otf_year.strftime("%Y")
                        if str_year == current_year:
                            result = (msf * len_terms) + otf
                        else:
                            result = msf * len_terms
                    else:
                        result = msf * len_terms
            else:
                timestamp = current_time_ph.strftime("%Y")
                if timestamp == current_year:
                    result = service.otf

        return result

    def fetch_revenue(self, obj):
        result = None
        service = core_models.LeadServices.objects.filter(
            lead_info=obj
        ).first()
        if service is None or not service.service:
            result = ""
        else:
            result = service.revenue
        return result

    def fetch_months(self, obj):
        current_year = self.context.get('year')
        result = []

        lead = core_models.LeadServices.objects.filter(
            lead_info=obj
        ).first()
        if lead:
            term = core_models.TermStatus.objects.filter(
                lead_service=lead, year=current_year
            )
            if term:
                for payment in term:
                    if payment.months:
                        result.append(
                            {
                                "month": payment.months,
                                "msf": payment.msf
                            }
                        )
        return result

    def fetch_otf_payment(self, obj):
        result = ''
        service = core_models.LeadServices.objects.filter(
            lead_info=obj
        ).first()
        if service:
            if service.otf_payment:
                result = service.otf_payment

        return result


class LeadStatusCountSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = core_models.LeadInformation
        fields = [
            "id",
            "status",
        ]

    def get_status(self, obj):
        lead_info = core_models.LeadInformation.objects.filter(
            condition=1
        ).values('status_label').aggregate(
            count_uncontacted=Count(Case(
                When(status_label=1, then=1),
                output_field=IntegerField(),
            )),
            count_contacted=Count(Case(
                When(status_label=2, then=1),
                output_field=IntegerField(),
            )),
            count_pipeline=Count(Case(
                When(status_label=3, then=1),
                output_field=IntegerField(),
            )),
            count_close_deal=Count(Case(
                When(status_label=4, then=1),
                output_field=IntegerField(),
            )),
            count_cold_leads=Count(Case(
                When(status_label=2, status=4, then=1),
                output_field=IntegerField(),
            ))
        )
        separated_output = [
            {
                "count": lead_info['count_uncontacted'],
                'label': "Uncontacted"
            },
            {
                "count": lead_info['count_contacted'],
                'label': "Contacted"
            },
            {
                "count": lead_info['count_pipeline'],
                'label': "Pipeline"
            },
            {
                "count": lead_info['count_close_deal'],
                'label': "Close Deal"
            },
            {
                "count": lead_info['count_cold_leads'],
                'label': "Cold Leads"
            }
        ]
        sorted_output = sorted(separated_output, key=lambda x: x['count'])
        return sorted_output


class LeadTotalPaymentSerializer(serializers.ModelSerializer):
    months = serializers.SerializerMethodField()
    otf_msf = serializers.SerializerMethodField()
    total_revenue = serializers.SerializerMethodField()

    class Meta:
        model = core_models.TermStatus
        fields = [
            "id",
            "months",
            "otf_msf",
            'total_revenue'
        ]

    def get_otf_msf(self, obj):
        year = self.context.get('year')
        current_year = datetime.now().year
        result = []
        lead = core_models.LeadServices.objects.filter(
            Q(lead_info__status_label=3) |
            Q(lead_info__status_label=4),
            lead_info__condition=1
        )
        for item in lead:
            if item.otf_payment:
                month = item.otf_payment
                month_str = datetime.strptime(str(month), "%Y-%m-%d")
                mont_int = month_str.month
                existing_entry = next(
                    (
                        entry for entry in result if entry['id'] == mont_int
                    ), None
                )
            if item.otf:
                if existing_entry:
                    existing_entry['month'] += item.otf
                else:
                    result.append({
                        'id': mont_int,
                        'month': item.otf
                    })
        if int(current_year) != int(year):
            result = []
        else:
            result
        return result

    def get_months(self, obj):
        current_year = self.context.get('year')

        month_names = [
            'january', 'february', 'march',
            'april', 'may', 'june', 'july',
            'august', 'september', 'october',
            'november', 'december'
        ]

        month_cases = {
            month: Sum(Case(
                When(months=index + 1,
                     lead_service__lead_info__condition=1,
                     then='msf'),
                output_field=FloatField()
            ))
            for index, month in enumerate(month_names)
        }

        month_sums = core_models.TermStatus.objects.filter(
            Q(lead_service__lead_info__status_label=3) |
            Q(lead_service__lead_info__status_label=4),
            year=current_year,
        ).values('months').aggregate(
            **month_cases)

        separated_output = [
            {'id': index + 1, 'month': month_sums[month] or 0}
            for index, month in enumerate(month_names)
        ]
        return separated_output

    def get_total_revenue(self, obj):
        result = 0
        lead_service = core_models.LeadServices.objects.filter(
            lead_info__condition=1,
        ).values('revenue').aggregate(
            sum=Sum('revenue')
        )
        if lead_service:
            result = lead_service
        else:
            result = 0
        return result


class PipelineStatusSerializer(serializers.ModelSerializer):
    presentation = serializers.SerializerMethodField()
    proposal = serializers.SerializerMethodField()
    negotiation = serializers.SerializerMethodField()
    closed_deal = serializers.SerializerMethodField()

    class Meta:
        model = core_models.LeadInformation
        fields = [
            "id",
            "presentation",
            "proposal",
            "negotiation",
            "closed_deal"
        ]

    def get_presentation(self, obj):
        result = None
        lead_service = core_models.LeadServices.objects.filter(
            lead_info__condition=1, lead_info__status=5
        ).values('revenue').aggregate(
            sum=Sum('revenue')
        )
        if lead_service:
            result = lead_service
        else:
            result = ""
        return result

    def get_proposal(self, obj):
        result = None
        lead_service = core_models.LeadServices.objects.filter(
            lead_info__condition=1, lead_info__status=6
        ).values('revenue').aggregate(
            sum=Sum('revenue')
        )
        if lead_service:
            result = lead_service
        else:
            result = ""
        return result

    def get_negotiation(self, obj):
        result = None
        lead_service = core_models.LeadServices.objects.filter(
            lead_info__condition=1, lead_info__status=7
        ).values('revenue').aggregate(
            sum=Sum('revenue')
        )
        if lead_service:
            result = lead_service
        else:
            result = ""
        return result

    def get_closed_deal(self, obj):
        result = None
        lead_service = core_models.LeadServices.objects.filter(
            lead_info__condition=1, lead_info__status=8
        ).values('revenue').aggregate(
            sum=Sum('revenue')
        )
        if lead_service:
            result = lead_service
        else:
            result = ""
        return result


class PerformanceReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = core_models.Account
        fields = [
            'id',
            'name',
            'total',
            'pipeline',
            'projected',
            'actual',
            'total_rev'
        ]

    name = serializers.SerializerMethodField(
        'fetch_name'
    )

    total = serializers.SerializerMethodField(
        'fetch_total'
    )

    pipeline = serializers.SerializerMethodField(
        'fetch_pipeline'
    )

    projected = serializers.SerializerMethodField(
        'fetch_projected'
    )

    actual = serializers.SerializerMethodField(
        'fetch_actual'
    )

    total_rev = serializers.SerializerMethodField(
        'fetch_total_rev'
    )

    def fetch_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def fetch_total(self, obj):
        result = None
        owner = core_models.LeadOwner.objects.filter(
            Q(lead__status_label=2) | Q(lead__status_label=3),
            account=obj,
            lead__condition=1,
        ).aggregate(count=Count('lead'))['count']
        result = owner
        return result

    def fetch_pipeline(self, obj):
        result = None
        owner = core_models.LeadOwner.objects.filter(
            account=obj,
            lead__condition=1,
            lead__status_label=3
        ).aggregate(count=Count('lead'))['count']
        result = owner
        return result

    def fetch_projected(self, obj):
        leads = core_models.LeadOwner.objects.filter(
            Q(lead__status_label=2) | Q(lead__status_label=3),
            account=obj,
            lead__condition=1,
        )

        projected_revenue = 0
        for lead in leads:
            revenue = core_models.LeadServices.objects.filter(
                lead_info=lead.lead
            )
            for rev in revenue:
                projected_revenue += rev.revenue if rev.revenue\
                    is not None else 0

        return projected_revenue

    def fetch_actual(self, obj):
        leads = core_models.LeadOwner.objects.filter(
            lead__status_label=4,
            account=obj,
            lead__condition=1,
        )

        actual_revenue = 0
        for lead in leads:
            revenue = core_models.LeadServices.objects.filter(
                lead_info=lead.lead
            )
            for rev in revenue:
                actual_revenue += rev.revenue if rev.revenue\
                    is not None else 0

        return actual_revenue

    def fetch_total_rev(self, obj):
        leads = core_models.LeadOwner.objects.filter(
            account=obj,
            lead__condition=1,
        )

        total_revenue = 0
        for lead in leads:
            revenue = core_models.LeadServices.objects.filter(
                lead_info=lead.lead
            )
            if revenue:
                for rev in revenue:
                    total_revenue += rev.revenue if rev.revenue\
                        is not None else 0

        return total_revenue


class TotalRevenueSerializer(serializers.ModelSerializer):

    class Meta:
        model = core_models.LeadServices
        fields = [
            'total_revenue',
        ]

    total_revenue = serializers.SerializerMethodField(
        'fetch_total_revenue'
    )

    def fetch_total_revenue(self, obj):
        lead_info = core_models.LeadServices.objects.filter(
            lead_info__condition=1
        ).values('revenue').aggregate(
            pipeline_rev=Sum(
                Case(
                    When(
                        Q(
                            lead_info__status_label=2
                        ) | Q(lead_info__status_label=3),
                        then='revenue'
                    ),
                    output_field=FloatField(),
                )
            ),
            actual_rev=Sum(
                Case(
                    When(
                        lead_info__status_label=4,
                        then='revenue'
                    ),
                    output_field=FloatField()
                )
            ),
            total_rev=Sum(
                Case(
                    When(
                        Q(lead_info__status_label=2) |
                        Q(lead_info__status_label=3) |
                        Q(lead_info__status_label=4),
                        then='revenue'
                    ),
                    output_field=FloatField()
                )
            )
        )
        return lead_info


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.Attachment
        fields = [
            "id",
            "lead_info",
            "status",
            "label",
            "date_inserted",
            "file",
            "uploaded_by"
        ]

    lead_info = serializers.SerializerMethodField(
            'fetch_lead_info'
    )

    def fetch_lead_info(self, obj):
        return "%s %s" % (
            obj.lead_info.client.first_name,
            obj.lead_info.client.last_name
        )


class MsfBreakdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.LeadServices
        fields = [
            'id',
            'otf',
            'msf',
            'revenue',
            'payment',
            'lead_name',
            'service',
            'term',
        ]

    payment = serializers.SerializerMethodField(
        'fetch_payment'
    )
    lead_name = serializers.SerializerMethodField(
        'fetch_lead_name'
    )
    service = serializers.SerializerMethodField(
        'fetch_service'
    )
    term = serializers.SerializerMethodField(
        'fetch_term'
    )

    def fetch_lead_name(self, obj):
        return "%s %s" % (
            obj.lead_info.client.first_name,
            obj.lead_info.client.last_name
        )

    def fetch_service(self, obj):
        return obj.service.name

    def fetch_term(self, obj):
        result = 0
        term_query = core_models.TermStatus.objects.filter(
            lead_service=obj
        ).count()

        result = term_query
        return result

    def fetch_payment(self, obj):
        result = []
        lead_service = core_models.TermStatus.objects.filter(
            lead_service=obj
        ).values_list('year', flat=True).distinct()

        for distint_year in lead_service:
            data = []
            monthly_terms = core_models.TermStatus.objects.filter(
                lead_service=obj, year=distint_year
            )
            for msf in monthly_terms:
                month_name = dict(
                    core_models.TermStatus.MONTHS
                ).get(msf.months, '')
                data.append(
                    {
                        "months": msf.months,
                        "months_name": month_name,
                        "msf": msf.msf,
                        "term_id": msf.id
                    }
                )
            result.append(
                {
                    "year": distint_year,
                    "breakdown": data
                }
            )
        return result


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.Notification
        fields = [
            'id',
            'sender',
            'subject',
            'status',
            'receiver',
            'message',
            'is_seen',
            'date_deliver',
            'date_seen'
        ]

    sender = serializers.SerializerMethodField(
        'fetch_sender'
    )

    def fetch_sender(self, obj):
        return "%s %s" % (
            obj.sender.user.first_name,
            obj.sender.user.last_name
        )


class CustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.LeadOwner
        fields = [
            'id',
            'full_name',
            'email',
            'phone_num',
            'tel_num',
            'company',
            'owner',
            'lead_status',
            'service',
            'rev',

            'industry',
            'remarks',
            'address',
            'source',
            'department',
            'job_title'
        ]

    full_name = serializers.SerializerMethodField(
        'fetch_full_name'
    )
    email = serializers.SerializerMethodField(
        'fetch_email'
    )

    phone_num = serializers.SerializerMethodField(
        'fetch_phone_num'
    )

    tel_num = serializers.SerializerMethodField(
        'fetch_tel_num'
    )

    company = serializers.SerializerMethodField(
        'fetch_company'
    )
    owner = serializers.SerializerMethodField(
        'fetch_owner'
    )
    lead_status = serializers.SerializerMethodField(
        'fetch_lead_status'
    )
    service = serializers.SerializerMethodField(
        'fetch_service'
    )
    rev = serializers.SerializerMethodField(
        'fetch_rev'
    )
    industry = serializers.SerializerMethodField(
        'fetch_industry'
    )
    remarks = serializers.SerializerMethodField(
        'fetch_remarks'
    )
    address = serializers.SerializerMethodField(
        'fetch_address'
    )
    source = serializers.SerializerMethodField(
        'fetch_source'
    )
    department = serializers.SerializerMethodField(
        'fetch_department'
    )
    job_title = serializers.SerializerMethodField(
        'fetch_job_title'
    )

    def fetch_job_title(self, obj):
        result = ''
        if obj.lead.client.job_title:
            result = (
                obj.lead.client.job_title
            )
        return result

    def fetch_department(self, obj):
        result = ''
        if obj.lead.client.department:
            result = (
                obj.lead.client.department
            )
        return result

    def fetch_source(self, obj):
        result = ''
        if obj.lead.source:
            result = (
                obj.lead.source
            )
        return result

    def fetch_industry(self, obj):
        result = ''
        if obj.lead.client.company.industry:
            result = (
                obj.lead.client.company.industry.name
            )
        return result

    def fetch_remarks(self, obj):
        result = ''
        if obj.lead.remarks:
            result = (
                obj.lead.remarks
            )
        return result

    def fetch_address(self, obj):
        result = ''
        if obj.lead.client.company.address:
            result = (
                obj.lead.client.company.address
            )
        return result

    def fetch_full_name(self, obj):
        return "%s %s" % (
            obj.lead.client.first_name,
            obj.lead.client.last_name
        )

    def fetch_email(self, obj):
        return obj.lead.client.email

    def fetch_phone_num(self, obj):
        result = ''
        if obj.lead.client.phone_num:
            result = obj.lead.client.phone_num
        return result

    def fetch_tel_num(self, obj):
        result = ''
        if obj.lead.client.tel_num:
            result = obj.lead.client.tel_num
        return result

    def fetch_company(self, obj):
        result = ''
        if obj.lead.client.company.name:
            result = obj.lead.client.company.name
        return result

    def fetch_lead_status(self, obj):
        # return obj.lead.status
        result = ''
        status_list = core_models.LeadInformation.STATUS
        for status in status_list:
            if status[0] == obj.lead.status:
                result = status[1]
        return result

    def fetch_owner(self, obj):
        if obj.account and obj.account.user:
            fname =\
                obj.account.user.first_name\
                if obj.account.user.first_name else ''
            lname =\
                obj.account.user.last_name\
                if obj.account.user.last_name else ''
            return "%s %s" % (fname, lname)
        return ''

    def fetch_service(self, obj):
        result = ''
        lead_service = core_models.LeadServices.objects.filter(
            lead_info=obj.lead
        ).first()
        if lead_service:
            if lead_service.service:
                result = lead_service.service.name

        return result

    def fetch_rev(self, obj):
        result = 0
        lead_service = core_models.LeadServices.objects.filter(
            lead_info=obj.lead
        )

        for ls in lead_service:
            if ls.revenue is not None:
                result += ls.revenue
        return result or 0
