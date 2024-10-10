from rest_framework import (
    viewsets,
    status
)
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from client import serializers as client_serializer
from core import models as core_model
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from core.core_function import Core


ph_timezone = timezone.get_fixed_timezone(480)
current_time_ph = timezone.localtime(
    timezone.now(), ph_timezone
)


class ClientView(viewsets.ModelViewSet):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(methods=['GET'], detail=False)
    def industry_list(self, request, pk=None):
        """
        <GET> url: /api/client/industry_list/
        """

        queryset = core_model.Industry.objects.all()
        industry_serializer = client_serializer.IndustrySerializer(
            instance=queryset,
            many=True
        ).data

        return Response(
            {
                "success": True,
                "data": industry_serializer
            }, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def add_new_leads(self, request, pk=None):
        """
        <POST> url: /api/client/add_new_leads/
        request = {
            "first_name": "John",
            "last_name": "Doe",
            "phone_num": 09182475698,
            "tel_num": 908-098-09,
            "email": johndoe@gmail.com,
            "job_title": "Programmer",
            "company_name": "One Outsource Direct Company",
            "address": "makati",
            "remarks: "new found lead",
            "company_size": 10,
            "lead_owner": 867,
            "department": CI,
            "source": facebook,
            "industry":
            "Telecommunications"
            "session": jimuel tomas,
            "service": 2
        }
        """
        data = request.data
        print(data)
        f_name = data.get('first_name')
        l_name = data.get('last_name')

        account_id = core_model.Account.objects.filter(
            employee_id=data.get("lead_owner")
        ).first()

        if not account_id:
            return Response(
                {
                    "success": False,
                    "message": "employee doest not exist",
                }, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            exist_email = core_model.Client.objects.filter(
                email=data.get('email')
            ).first()
            so = core_model.ServiceOffered.objects.filter(
                id=data.get("service")
            ).first()

            if exist_email:
                message = (
                    f"Say hello again to {f_name} {l_name}, "
                    f"added by {data.get('session')}."
                )

                lead_info = core_model.LeadInformation()
                for fields in ['status_label', 'source', 'remarks']:
                    if data.get(fields):
                        setattr(lead_info, fields, data.get(fields))
                if exist_email.company != "":
                    lead_info.type = 1
                else:
                    lead_info.type = 2
                lead_info.save()

                if data.get('lead_status'):
                    lead_info.status = int(data.get('lead_status'))

                lead_info.client = exist_email
                lead_info.save()

                lead_service = None
                if data.get('service'):
                    lead_service = core_model.LeadServices(
                        lead_info=lead_info,
                        service=so
                    )
                    lead_service.save()

                lead_owner = core_model.LeadOwner(
                    lead=lead_info,
                    date_handle=current_time_ph,
                    account=account_id
                )

                lead_owner.save()

                Core.create_activity(
                    lead_info=lead_info,
                    message=message,
                    type=core_model.Activity.NEWLEADS,
                    status=core_model.Activity.ACTIVE,
                    date_generated=current_time_ph,
                    owner=data.get("session")
                )
                return Response(
                    {
                        "success": True,
                        "message": (
                            "Added leads has already exist, "
                            "kindly double check it."
                        )
                    }, status=status.HTTP_200_OK)

            else:
                message = (
                    f"Say hello to our latest lead {f_name} {l_name}, "
                    f"joining our journey towards greater "
                    f"opportunities and success!"
                    f" added by {data.get('session')}."
                )
                if data.get("industry"):
                    industry = core_model.Industry.objects.filter(
                        name=data.get("industry")
                    ).first()

                    if not industry:
                        return Response(
                            {
                                "success": False,
                                "message": "industry doest not exist",
                            }, status=status.HTTP_400_BAD_REQUEST)

                company = core_model.CompanyInformation()
                for fields in ['address', 'company_size']:

                    if data.get(fields):
                        setattr(company, fields, data.get(fields))

                if data.get("company_name"):
                    company.name = data.get("company_name")

                if data.get("industry"):
                    company.industry = industry

                company.save()

                client = core_model.Client()
                if data.get("first_name"):
                    client.first_name = data.get("first_name").title()

                if data.get("last_name"):
                    client.last_name = data.get("last_name").title()

                for fields in ['phone_num', 'tel_num', 'email',
                               'job_title', 'department', 'remarks']:

                    if data.get(fields):
                        setattr(client, fields, data.get(fields))

                client.company = company

                client.save()

                lead_info = core_model.LeadInformation()
                for fields in ['status_label', 'source', 'remarks']:
                    if data.get(fields):
                        setattr(lead_info, fields, data.get(fields))
                if data.get('company_name'):
                    lead_info.type = 1
                else:
                    lead_info.type = 2
                lead_info.save()

                if data.get('lead_status'):
                    lead_info.status = int(data.get('lead_status'))

                lead_info.client = client
                lead_info.save()

                lead_service = None
                if data.get('service'):
                    lead_service = core_model.LeadServices(
                        lead_info=lead_info,
                        service=so
                    )
                    lead_service.save()

                lead_owner = core_model.LeadOwner(
                    lead=lead_info,
                    date_handle=current_time_ph,
                    account=account_id
                )

                lead_owner.save()

                Core.create_activity(
                    lead_info=lead_info,
                    message=message,
                    type=core_model.Activity.NEWLEADS,
                    status=core_model.Activity.ACTIVE,
                    date_generated=current_time_ph,
                    owner=data.get("session")
                )

                return Response(
                    {
                        "success": True,
                        "message": "New leads successfully uploaded"
                    }, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False)
    def fetch_all_leads(self, request, pk=None):
        """
        <GET> url: api/client/fetch_all_leads/
        ?page=1&page_size=10&search_str="&status=1
        """

        queryset = core_model.LeadOwner.objects.filter(
            lead__condition=1
        ).order_by('-id')
        status = self.request.query_params.get("status") or 0
        search_owner = self.request.query_params.get("search_owner") or 0
        search_str = self.request.query_params.get("search_str") or ""
        filter_service = self.request.query_params.get("filter_service") or 0

        if int(status) != 0:
            queryset = core_model.LeadOwner.objects.filter(
                lead__status=status, lead__condition=1
            )

        if int(search_owner) != 0:
            queryset = core_model.LeadOwner.objects.filter(
                account__employee_id=search_owner, lead__condition=1
            )

        if int(filter_service) != 0:
            filter_services = core_model.LeadServices.objects.filter(
                service=filter_service
            ).values_list('lead_info__id', flat=True)

            queryset = core_model.LeadOwner.objects.filter(
                lead__id__in=filter_services, lead__condition=1
            )

        if search_str:
            queryset = queryset.filter(
               Q(lead__client__first_name__icontains=search_str) |
               Q(lead__client__last_name__icontains=search_str) |
               Q(lead__client__company__name__icontains=search_str) |
               Q(account__user__first_name__icontains=search_str)
            )

        page_size = request.query_params.get('page_size') or 10
        paginator = PageNumberPagination()
        paginator.page_size = page_size

        return paginator.get_paginated_response(
            client_serializer.AllLeadSerializer(
                instance=paginator.paginate_queryset(
                    queryset, request
                ),
                many=True
            ).data
        )

    @action(methods=["GET"], detail=False)
    def fetch_uncontacted_leads(self, request, pk=None):
        """
        <GET> url: api/client/fetch_uncontacted_leads/
        ?page=1&page_size=10&search_str="&status=1&session=867&
        """

        session = self.request.query_params.get("session")
        queryset = core_model.LeadOwner.objects.filter(
            account__employee_id=session, lead__condition=1
        ).order_by('-id')
        status = self.request.query_params.get("status")
        search_str = self.request.query_params.get("search_str") or ""

        if int(status) != 0:
            queryset = core_model.LeadOwner.objects.filter(
                lead__status=status, account__employee_id=session,
                lead__condition=1
            ).order_by('-id')
        # else:
        #     queryset = core_model.LeadOwner.objects.all().order_by('-id')
        if search_str:
            queryset = queryset.filter(
               Q(lead__client__first_name__icontains=search_str) |
               Q(lead__client__last_name__icontains=search_str) |
               Q(lead__client__email__icontains=search_str)
            )
        page_size = request.query_params.get('page_size') or 10
        paginator = PageNumberPagination()
        paginator.page_size = page_size

        return paginator.get_paginated_response(
            client_serializer.AllLeadSerializer(
                instance=paginator.paginate_queryset(
                    queryset, request
                ),
                many=True
            ).data
        )

    @action(methods=["GET"], detail=False)
    def fetch_closed_leads(self, request, pk=None):
        """
        <GET> url: api/client/fetch_closed_leads/
        ?page=1&page_size=10&search_str="&status=1&session=867&
        """

        session = self.request.query_params.get("session")
        queryset = core_model.LeadOwner.objects.filter(
            account__employee_id=session, lead__condition=1,
            lead__status=8
        ).order_by('-id')
        search_str = self.request.query_params.get("search_str") or ""
        filter_service = self.request.query_params.get("filter_service")

        if search_str:
            queryset = queryset.filter(
               Q(lead__client__first_name__icontains=search_str) |
               Q(lead__client__last_name__icontains=search_str) |
               Q(lead__client__email__icontains=search_str)
            )

        if int(filter_service) != 0:
            filter_services = core_model.LeadServices.objects.filter(
                service=filter_service
            ).values_list('lead_info__id', flat=True)

            queryset = core_model.LeadOwner.objects.filter(
                lead__id__in=filter_services, lead__condition=1
            )

        page_size = request.query_params.get('page_size') or 10
        paginator = PageNumberPagination()
        paginator.page_size = page_size

        return paginator.get_paginated_response(
            client_serializer.AllLeadSerializer(
                instance=paginator.paginate_queryset(
                    queryset, request
                ),
                many=True
            ).data
        )

    @action(methods=["GET"], detail=False)
    def fetch_leads(self, request, pk=None):
        """
        <GET> url: api/client/fetch_leads/
        ?page=1&page_size=10&searc_str="&status_label=1&session=867
        """

        session = self.request.query_params.get("session")
        queryset = core_model.LeadOwner.objects.filter(
            account__employee_id=session, lead__condition=1
        )
        statuss = self.request.query_params.get("status_label")
        search_str = self.request.query_params.get("search_str") or ""

        if int(statuss) != 0:
            queryset = core_model.LeadOwner.objects.filter(
                lead__status_label=statuss, account__employee_id=session,
                lead__condition=1
            )
        # else:
        #     queryset = core_model.LeadOwner.objects.all().order_by('-id')
        if search_str:
            queryset = queryset.filter(
               Q(lead__client__first_name__icontains=search_str) |
               Q(lead__client__last_name__icontains=search_str) |
               Q(lead__client__email__icontains=search_str)
            )

        page_size = request.query_params.get('page_size') or 10
        paginator = PageNumberPagination()
        paginator.page_size = page_size

        return paginator.get_paginated_response(
            client_serializer.AllLeadSerializer(
                instance=paginator.paginate_queryset(
                    queryset, request
                ),
                many=True
            ).data
        )

    @action(methods=['GET'], detail=True)
    def fetch_detail_leads(self, request, pk=None):
        """
        <GET> url: api/client/<id>/fetch_detail_leads/
        """

        lead_owner = core_model.LeadOwner.objects.filter(
            id=pk,
        ).first()
        print(lead_owner)

        if not lead_owner:
            return Response(
                {
                    "success": False,
                    "message": "Lead not found"
                }, status=status.HTTP_400_NOT_FOUND
            )

        return Response({
            "success": True,
            "data": client_serializer.LeadStatusSerializer(
                instance=lead_owner,
                many=False
            ).data,
        }, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def update_lead_status(self, request, pk=None):
        """
        <POST> url: api/client/update_lead_status/
            request = {
            id: 1,
            lead_status: 2
            }
        """

        data = request.data
        print(data)
        session = data.get('session')

        lead_info = core_model.LeadInformation.objects.filter(
            id=int(data.get("id"))
        ).first()

        if not lead_info:
            return Response({
                "success": False,
                "message": "lead id does not exist"
            }, status=status.HTTP_400_NOT_FOUND)

        client = core_model.Client.objects.filter(
            id=lead_info.client.id
        ).first()
        print(client)

        if not client:
            return Response({
                "success": False,
                "message": "client id does not exist"
            }, status=status.HTTP_400_NOT_FOUND)

        company = core_model.CompanyInformation.objects.filter(
            id=client.company.id
        ).first()

        if not company:
            return Response({
                "success": False,
                "message": "company id does not exist"
            }, status=status.HTTP_400_NOT_FOUND)

        with transaction.atomic():
            if data.get("industry_name"):
                industry = core_model.Industry.objects.filter(
                    name=data.get("industry_name")
                ).first()
                company.industry = industry
                company.save()

                Core.create_activity(
                    lead_info=lead_info,
                    message=(
                        f"{session} has been updated the industry"
                        f" into {industry}."
                    ),
                    type=core_model.Activity.UPDATEINFO,
                    status=core_model.Activity.ACTIVE,
                    date_generated=current_time_ph,
                    owner=data.get("session")
                )

            if data.get("company"):
                company_n = data.get("company")
                company.name = data.get("company")
                company.save()

                Core.create_activity(
                    lead_info=lead_info,
                    message=(
                        f"{session} has been updated the"
                        f" company name into {company_n}."
                    ),
                    type=core_model.Activity.UPDATEINFO,
                    status=core_model.Activity.ACTIVE,
                    date_generated=current_time_ph,
                    owner=data.get("session")
                )

            if data.get("address"):
                address = data.get("address")
                company.address = data.get("address")
                company.save()

                Core.create_activity(
                    lead_info=lead_info,
                    message=(
                        f"{session} has been updated the"
                        f" address into {address}."
                    ),
                    type=core_model.Activity.UPDATEINFO,
                    status=core_model.Activity.ACTIVE,
                    date_generated=current_time_ph,
                    owner=data.get("session")
                )
            if data.get("first_name"):
                client.first_name = data.get("first_name")
                Core.create_activity(
                    lead_info=lead_info,
                    message=(
                        f"{session} has been updated the"
                        f" first name into {data.get('first_name')}."
                    ),
                    type=core_model.Activity.UPDATEINFO,
                    status=core_model.Activity.ACTIVE,
                    date_generated=current_time_ph,
                    owner=data.get("session")
                )
            if data.get("last_name"):
                client.last_name = data.get("last_name")
                Core.create_activity(
                    lead_info=lead_info,
                    message=(
                        f"{session} has been updated the"
                        f" last name into {data.get('last_name')}."
                    ),
                    type=core_model.Activity.UPDATEINFO,
                    status=core_model.Activity.ACTIVE,
                    date_generated=current_time_ph,
                    owner=data.get("session")
                )
            if data.get("phone_num"):
                client.phone_num = data.get("phone_num")
                Core.create_activity(
                    lead_info=lead_info,
                    message=(
                        f"{session} has been updated the"
                        f" phone number into {data.get('phone_num')}."
                    ),
                    type=core_model.Activity.UPDATEINFO,
                    status=core_model.Activity.ACTIVE,
                    date_generated=current_time_ph,
                    owner=data.get("session")
                )
            if data.get("tel_num"):
                client.tel_num = data.get("tel_num")
                Core.create_activity(
                    lead_info=lead_info,
                    message=(
                        f"{session} has been updated the"
                        f" telephone number into {data.get('tel_num')}."
                    ),
                    type=core_model.Activity.UPDATEINFO,
                    status=core_model.Activity.ACTIVE,
                    date_generated=current_time_ph,
                    owner=data.get("session")
                )
            if data.get("email"):
                client.email = data.get("email")
                Core.create_activity(
                    lead_info=lead_info,
                    message=(
                        f"{session} has been updated the"
                        f" email into {data.get('email')}."
                    ),
                    type=core_model.Activity.UPDATEINFO,
                    status=core_model.Activity.ACTIVE,
                    date_generated=current_time_ph,
                    owner=data.get("session")
                )
            if data.get("job_title"):
                client.job_title = data.get("job_title")
                Core.create_activity(
                    lead_info=lead_info,
                    message=(
                        f"{session} has been updated the"
                        f" job title into {data.get('job_title')}."
                    ),
                    type=core_model.Activity.UPDATEINFO,
                    status=core_model.Activity.ACTIVE,
                    date_generated=current_time_ph,
                    owner=data.get("session")
                )
            if data.get("deparment"):
                client.deparment = data.get("deparment")
                Core.create_activity(
                    lead_info=lead_info,
                    message=(
                        f"{session} has been updated the"
                        f" department into {data.get('deparment')}."
                    ),
                    type=core_model.Activity.UPDATEINFO,
                    status=core_model.Activity.ACTIVE,
                    date_generated=current_time_ph,
                    owner=data.get("session")
                )
            client.save()

            if data.get("remarks"):
                remarks = data.get('remarks')
                lead_info.remarks = data.get('remarks')

                lead_info.save()

                Core.create_activity(
                    lead_info=lead_info,
                    message=(
                        f"{session} has been updated the"
                        f" remarks into {remarks}."
                    ),
                    type=core_model.Activity.UPDATEINFO,
                    status=core_model.Activity.ACTIVE,
                    date_generated=current_time_ph,
                    owner=data.get("session")
                )

            if data.get("service"):
                lead_service = core_model.LeadServices.objects.filter(
                    lead_info__id=lead_info.id
                ).first()
                service_id = core_model.ServiceOffered.objects.filter(
                    id=int(data.get("service"))
                ).first()

                if not lead_service:
                    lead_service = core_model.LeadServices(
                        lead_info=lead_info,
                        service=service_id
                    )
                    lead_service.save()
                    Core.create_activity(
                        lead_info=lead_info,
                        message=(
                            f"{session} added a service offered"
                            f" as {service_id.name} for this lead."
                        ),
                        type=core_model.Activity.UPDATEINFO,
                        status=core_model.Activity.ACTIVE,
                        date_generated=current_time_ph,
                        owner=data.get("session")
                    )
                else:
                    lead_service.service = service_id
                    lead_service.save()

                    Core.create_activity(
                        lead_info=lead_info,
                        message=(
                            f"{session} updated the service offered"
                            f" into {service_id.name} for this lead."
                        ),
                        type=core_model.Activity.UPDATEINFO,
                        status=core_model.Activity.ACTIVE,
                        date_generated=current_time_ph,
                        owner=data.get("session")
                    )

            if data.get("lead_status"):
                status_value = int(data.get('lead_status'))
                stat = core_model.LeadInformation.STATUS[
                    status_value - 1][1]

                lead_info.status = int(data.get("lead_status"))
                lead_info.date_contacted = current_time_ph

                if int(data.get("lead_status")) == 1:
                    lead_info.status_label = 1

                if int(data.get("lead_status")) in [2, 3, 4]:
                    lead_info.status_label = 2

                if int(data.get("lead_status")) in [5, 6, 7]:
                    lead_info.status_label = 3

                if int(data.get("lead_status")) == 8:
                    lead_info.status_label = 4

                if int(data.get("lead_status")) in [9, 10, 11]:
                    lead_info.status_label = 5

                lead_info.save()

                Core.create_activity(
                    lead_info=lead_info,
                    message=(
                        f"{session} has been updated the lead status"
                        f" into {stat.upper()}."
                    ),
                    type=core_model.Activity.UPDATESTATUS,
                    status=core_model.Activity.ACTIVE,
                    date_generated=current_time_ph,
                    owner=data.get("session")
                )

        return Response(
            {
                "success": True,
                "message": "Lead status successfully updated"
            }, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False)
    def import_csv_leads(self, request, pk=None):
        """
        <POST> url: api/client/import_csv_leads/
            request = [
                {
                    "first_name": "John",
                    "last_name": "Doe",
                    "phone_num": 09182475698,
                    "tel_num": 908-098-09,
                    "email": johndoe@gmail.com,
                    "job_title": "Programmer",
                    "company_name":
                    "One Outsource Direct Company",
                    "address": "makati",
                    "remarks: "new found lead",
                    "company_size": 10,
                    "lead_owner": ""
                    "department": ""
                    "type": 1,
                    "source": facebook,
                    "industry":
                    "Telecommunications"
                }
            ]
        """

        data = request.data
        print(data)

        with transaction.atomic():
            session = data.get('session')
            for lead in data.get('bulk_lead'):

                company = core_model.CompanyInformation()
                # account_id = core_model.Account.objects.filter(
                #     employee_id=lead.get("lead_owner")
                # ).first()

                industry_name = lead.get('industry')
                industry = core_model.Industry.objects.filter(
                    name=industry_name
                ).first()

                if lead.get("company"):
                    company.name = lead.get("company_name")
                if lead.get('address'):
                    company.address = lead.get("address")
                if lead.get('company_size'):
                    company.company_size = lead.get('company_size')
                if lead.get('industry'):
                    company.industry = industry

                company.save()

                client = core_model.Client(
                    company=company,
                )
                if lead.get('first_name'):
                    client.first_name = lead.get(
                        "first_name").title()
                if lead.get('last_name'):
                    client.last_name = lead.get(
                        "last_name").title()
                if lead.get('phone_num'):
                    client.phone_num = lead.get("phone_num")
                if lead.get('tel_num'):
                    client.tel_num = lead.get("tel_num")
                if lead.get('email'):
                    client.email = lead.get("email")
                if lead.get('job_title'):
                    client.job_title = lead.get("job_title")
                if lead.get('department'):
                    client.department = lead.get("department")

                client.save()

                lead_info = core_model.LeadInformation(
                    client=client
                )
                if lead.get("company"):
                    lead_info.type = 1
                else:
                    lead_info.type = 2

                if lead.get('source'):
                    lead_info.source = lead.get('source')

                if lead.get('remarks'):
                    client.remarks = lead.get('remarks')

                lead_info.save()

                lead_owner = core_model.LeadOwner(
                    lead=lead_info,
                )
                lead_owner.save()
                # if lead.get('lead_owner'):
                #     lead_info.account = account_id if account_id else "None"
                #     lead_info.date_handle = current_time_ph
                # lead_owner.save()

                f_name = lead.get('first_name')
                l_name = lead.get('last_name')
                message = (
                    f"Say hello to our latest lead {f_name} {l_name},"
                    f" joining our journey towards greater"
                    f" opportunities and success!"
                    f" added by {session}."
                )

                Core.create_activity(
                    lead_info=lead_info,
                    message=message,
                    type=core_model.Activity.NEWLEADS,
                    status=core_model.Activity.ACTIVE,
                    date_generated=current_time_ph,
                    owner=lead.get("lead_owner")
                )

        return Response(
            {
                "success": True,
                "message": "Imported leads uploaded successfully"
            }, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def change_lead_owner(self, request, pk=None):
        """
        <POST> url: api/client/change_lead_owner/
        request = {
            new_owner: 813,
            lead_id: [1,2,3],
            session: "jimueltomas"
            sender: 8233
        }
        """
        data = request.data
        print(data)
        session = data.get("session")
        account = core_model.Account.objects.filter(
            employee_id=int(data.get("new_owner"))
        ).first()
        sender = core_model.Account.objects.filter(
            employee_id=int(data.get("sender"))
        ).first()

        if not account:
            return Response(
                {
                    "success": False,
                    "message": "Employee id not found"
                }, status=status.HTTP_400_NOT_FOUND)

        with transaction.atomic():
            for lead_id in data.get("lead_id"):
                print(lead_id)
                lead_owner = core_model.LeadOwner.objects.filter(
                    id=int(lead_id)
                )

                for lo in lead_owner:
                    sndr = "%s %s" % (
                        sender.user.first_name,
                        sender.user.last_name
                    )
                    lead = "%s %s" % (
                        lo.lead.client.first_name,
                        lo.lead.client.last_name
                    )
                    messages = (
                        f"Mr./ Ms. {sndr} assigned new leads to you. "
                        f"Lead Name: {lead} please reach out to the "
                        f"lead at your earliest convenience."
                    )

                    old_owner_name = ""
                    if lo.account is not None:
                        old_owner = core_model.Account.objects.filter(
                            employee_id=lo.account.employee_id
                        )

                        for ow in old_owner:
                            date_handle = lo.date_handle\
                                          if lo.date_handle is not None\
                                          else current_time_ph
                            owner_history = core_model.OwnerHistory(
                                lead_owner=lo,
                                date_transfer=current_time_ph,
                                date_handle=date_handle,
                                last_owner=ow
                            )
                            owner_history.save()

                            old_owner_name = "%s %s" % (
                                ow.user.first_name,
                                ow.user.last_name)
                    lo.account = account
                    lo.save()
                    if old_owner_name != "":
                        message = (
                                f"{session} has been transfer the lead from"
                                f" {old_owner_name} to"
                                f" {lo.account.user.first_name}."
                            )
                    else:
                        message = (
                               f"{session} has assign new leads to "
                               f"{lo.account.user.first_name}."
                           )

                    Core.create_activity(
                        lead_info=lo.lead,
                        message=message,
                        type=core_model.Activity.UPDATEINFO,
                        status=core_model.Activity.ACTIVE,
                        date_generated=current_time_ph,
                        owner=data.get("session")
                    )
                    Core.send_notification(
                        sender=int(data.get('sender')),
                        receiver=int(data.get('new_owner')),
                        message=messages,
                        date_delivered=current_time_ph
                    )

        return Response(
            {
                "success": True,
                "message": "Lead successfully transfered"
            }, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def add_lead_note(self, request, pk=None):
        """
        <POST> url: api/client/add_lead_note/
        request: {
        lead_id: 1,
        message: "this lead is initially contacted"
        }
        """
        data = request.data

        lead_id = core_model.LeadInformation.objects.filter(
            id=int(data.get("lead_id"))
        ).first()

        if not lead_id:
            return Response(
                {
                    "success": False,
                    "message": "lead id not found"
                }, status=status.HTTP_400_NOT_FOUND
            )
        with transaction.atomic():
            notes = core_model.Notes(
                lead_info=lead_id,
                message=data.get("message"),
                date_noted=current_time_ph
            )
            notes.save()

        return Response(
            {
                "success": True,
                "message": "Successfully done"
            }, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False)
    def fetch_lead_note(self, request, pk=None):
        """
        <GET> url: api/client/fetch_lead_note/
        ?page=1&page_size=3
        """
        lead_id = request.query_params.get("lead_id")
        notes = core_model.Notes.objects.filter(
            lead_info=lead_id, status=1
        ).order_by('id')

        page_size = request.query_params.get('page_size') or 3
        paginator = PageNumberPagination()
        paginator.page_size = page_size

        return paginator.get_paginated_response(
            client_serializer.NoteSerializer(
                instance=paginator.paginate_queryset(
                    notes, request
                ),
                many=True
            ).data
        )

    @action(methods=["GET"], detail=False)
    def fetch_lead_activity(self, request, pk=None):
        """
        <GET> url: api/client/fetch_lead_activity/
        ?page=1&page_size=3
        """
        lead_id = request.query_params.get("lead_id")
        notes = core_model.Activity.objects.filter(
            lead_info=lead_id
        ).order_by('-id')

        page_size = request.query_params.get('page_size') or 5
        paginator = PageNumberPagination()
        paginator.page_size = page_size

        return paginator.get_paginated_response(
            client_serializer.ActivitySerializer(
                instance=paginator.paginate_queryset(
                    notes, request
                ),
                many=True
            ).data
        )

    @action(methods=["POST"], detail=False)
    def uncontacted_csv_leads(self, request, pk=None):
        """
        <POST> url: api/client/uncontacted_csv_leads/
            request = [
                {
                    "first_name": "John",
                    "last_name": "Doe",
                    "phone_num": 09182475698,
                    "tel_num": 908-098-09,
                    "email": johndoe@gmail.com,
                    "job_title": "Programmer",
                    "company_name":
                    "One Outsource Direct Company",
                    "address": "makati",
                    "remarks: "new found lead",
                    "company_size": 10,
                    "lead_owner": ""
                    "department": ""
                    "type": 1,
                    "source": facebook,
                    "industry":
                    "Telecommunications"
                }
            ]
        """

        data = request.data
        print(data)

        with transaction.atomic():
            session = data.get("session")
            account_id = core_model.Account.objects.filter(
                    employee_id=data.get("lead_owner")
            ).first()

            for lead in data.get('bulk_lead'):

                company = core_model.CompanyInformation()

                industry_name = lead.get('industry')
                industry = core_model.Industry.objects.filter(
                    name=industry_name
                ).first()

                if lead.get("company"):
                    company.name = lead.get("company")
                if lead.get('address'):
                    company.address = lead.get("address")
                if lead.get('company_size'):
                    company.company_size = lead.get('company_size')
                if lead.get('industry'):
                    company.industry = industry

                company.save()

                client = core_model.Client(
                    company=company,
                    first_name=lead.get("first_name"),
                    last_name=lead.get("last_name")
                )

                if lead.get('phone_num'):
                    client.phone_num = lead.get("phone_num")
                if lead.get('tel_num'):
                    client.tel_num = lead.get("tel_num")
                if lead.get('email'):
                    client.email = lead.get("email")
                if lead.get('job_title'):
                    client.job_title = lead.get("job_title")
                if lead.get('department'):
                    client.department = lead.get("department")

                client.save()

                lead_info = core_model.LeadInformation(
                    client=client
                )
                if lead.get("company"):
                    lead_info.type = 1
                else:
                    lead_info.type = 2

                if lead.get('source'):
                    lead_info.source = lead.get('source')

                if lead.get('remarks'):
                    lead_info.remarks = lead.get('remarks')

                lead_info.save()

                lead_owner = core_model.LeadOwner(
                    lead=lead_info,
                    account=account_id,
                    date_handle=current_time_ph
                )
                lead_owner.save()

                f_name = lead.get('first_name').title()
                l_name = lead.get('last_name').title()
                message = (
                    f"Say hello to our latest lead {f_name} {l_name},"
                    f" joining our journey towards greater"
                    f" opportunities and success!"
                    f" added by {session}."
                )

                Core.create_activity(
                    lead_info=lead_info,
                    message=message,
                    type=core_model.Activity.NEWLEADS,
                    status=core_model.Activity.ACTIVE,
                    date_generated=current_time_ph,
                    owner=lead.get("lead_owner")
                )

        return Response(
            {
                "success": True,
                "message": "Imported leads uploaded successfully"
            }, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def fetch_services(self, request, pk=None):
        """
        <GET> url: api/client/fetch_services/?page=1&page_size=10
        """

        service_offered = core_model.ServiceOffered.objects.filter(
            status=1
        )

        if not service_offered:
            return Response(
                {
                    "success": False,
                    "message": "Request can not be performed"
                }, status=status.HTTP_400_BAD_REQUEST)

        page_size = request.query_params.get('page_size') or 10
        paginator = PageNumberPagination()
        paginator.page_size = page_size

        return paginator.get_paginated_response(
            client_serializer.ServiceOfferedSerializer(
                instance=paginator.paginate_queryset(
                    service_offered, request
                ),
                many=True
            ).data
        )

    @action(methods=["GET"], detail=False)
    def fetch_lead_service(self, request, pk=None):
        """
        <GET> url: api/client/fetch_lead_service/?lead_id=2
        """
        lead_id = request.query_params.get("lead_id")

        queryset = core_model.LeadServices.objects.filter(
            lead_info=lead_id, status=1
        )

        # if not queryset:
        #     return Response(
        #         {
        #             "success": False,
        #             "message": "Lead Id was not found"
        #         }, status=status.HTTP_400_NOT_FOUND)

        return Response(
            {
                "success": True,
                "data": client_serializer.LeadServiceSerializer(
                    instance=queryset,
                    many=True
                ).data
            }, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False)
    def add_revenue(self, request, pk=None):
        """
        <POST> url: api/client/add_revenue/
        request = {
            id: 1,
            otf: 2000,
            msf: 100,
            prevenue: 5000,
            month_start: 1,
            month_end: 4,
            months = [1,2,3,4]
        }
        """
        data = request.data
        print(data)
        session = data.get('session')

        lead_service = core_model.LeadServices.objects.filter(
            id=int(data.get('id'))
        ).first()

        if not lead_service:
            return Response(
                {
                    "success": False,
                    "message": "lead id was not found"
                }, status=status.HTTP_400_NOT_FOUND)

        with transaction.atomic():
            if data.get("otf"):
                lead_service.otf = float(data.get("otf"))
                lead_service.otf_payment = data.get(
                    "date_start") or current_time_ph
            if data.get("msf"):
                lead_service.msf = float(data.get("msf"))
            if data.get("prevenue"):
                lead_service.revenue = float(data.get("prevenue"))
            lead_service.save()

            monthy_t = core_model.MonthlyTerms.objects.filter(
                lead_service=lead_service
            ).first()

            if monthy_t:
                monthy_t.month_start = int(data.get('month_start'))
                monthy_t.month_end = int(data.get('month_end'))
                monthy_t.date_start = data.get("date_start")
                monthy_t.date_end = data.get("date_end")

                monthy_t.save()
            else:
                monthly_terms = core_model.MonthlyTerms(
                    month_start=int(data.get('month_start')),
                    month_end=int(data.get('month_end')),
                    lead_service=lead_service,
                    date_start=data.get("date_start"),
                    date_end=data.get("date_end")
                )

                monthly_terms.save()

            term_query = core_model.TermStatus.objects.filter(
                lead_service=lead_service
            )

            if data.get("months"):
                if term_query:
                    term_query.delete()
                    for month in data.get("months"):
                        term_status = core_model.TermStatus(
                            lead_service=lead_service,
                            months=int(month.get('month')),
                            year=int(month.get('year')),
                            msf=float(data.get("msf")) or None,
                            status=1
                        )
                        term_status.save()
                else:
                    for month in data.get("months"):
                        term_status = core_model.TermStatus(
                            lead_service=lead_service,
                            months=int(month.get('month')),
                            year=int(month.get('year')),
                            msf=float(data.get("msf")) or None,
                            status=1
                        )
                        term_status.save()

            Core.create_activity(
                lead_info=lead_service.lead_info,
                message=(
                    f"{session} updated the contract"
                    f" and other info for this lead"
                ),
                type=core_model.Activity.UPDATEINFO,
                status=core_model.Activity.ACTIVE,
                date_generated=current_time_ph,
                owner=data.get("session")
            )

        return Response(
            {
                "success": True,
                "message": "Revenue created successfully."
            }, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False)
    def fetch_detail_revenue(self, request, pk=None):
        """
        <GET> url: api/client/fetch_detail_revenue/?id=1
        """

        id = request.query_params.get('id')
        lead_services = core_model.LeadServices.objects.filter(
            id=id
        ).first()

        if not lead_services:
            return Response(
                {
                    "success": False,
                    "message": "lead service not found!"
                }, status=status.HTTP_400_NOT_FOUND)

        return Response(
            {
                "success": True,
                "data": client_serializer.leadServiceDataSerializer(
                    instance=lead_services,
                    many=False
                ).data
            }, status=status.HTTP_200_OK)

    @action(methods=['PUT'], detail=False)
    def remove_leads(self, request, pk=None):
        """
        <PUT> url: api/client/remove_leads/
        """

        data = request.data
        print(data)

        lead_info = core_model.LeadInformation.objects.filter(
            id=int(data.get('leadId'))
        ).first()

        session = core_model.Account.objects.filter(
            employee_id=int(data.get("session"))
        ).first()

        if not lead_info:
            return Response(
                {
                    "success": False,
                    "message": "Lead not found"
                }, status=status.HTTP_400_NOT_FOUND
            )

        lead_info.condition = 2
        lead_info.save()

        archive = core_model.Archive(
            lead_info=lead_info,
            date_deleted=current_time_ph,
            deleted_by=session
        )
        archive.save()

        return Response(
            {
                "success": True,
                "message": "Lead successfully deleted"
            }, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False)
    def fetch_deleted_leads(self, request, pk=None):
        """
        <GET> url: api/client/fetch_deleted_leads/
        ?page=1&page_size=10&search_str=""
        """

        queryset = core_model.Archive.objects.all().order_by('-id')
        search_str = self.request.query_params.get("search_str") or ""

        if search_str:
            queryset = queryset.filter(
               Q(lead_info__client__first_name__icontains=search_str) |
               Q(lead_info__client__last_name__icontains=search_str) |
               Q(lead_info__client__email__icontains=search_str) |
               Q(lead_info__client__company__name__icontains=search_str) |
               Q(deleted_by__user__first_name__icontains=search_str) |
               Q(deleted_by__user__last_name__icontains=search_str)
            )

        page_size = request.query_params.get('page_size') or 10
        paginator = PageNumberPagination()
        paginator.page_size = page_size

        return paginator.get_paginated_response(
            client_serializer.ArchiveSerializer(
                instance=paginator.paginate_queryset(
                    queryset, request
                ),
                many=True
            ).data
        )

    @action(methods=["GET"], detail=False)
    def fetch_client_list(self, request, pk=None):
        """
        <GET> url: api/client/fetch_client_list/
        ?page=1&page_size=10&search_str=""
        """

        lead_info = core_model.LeadInformation.objects.filter(
            condition=1
        ).values_list('client', flat=True)
        queryset = core_model.Client.objects.filter(
            id__in=lead_info
        ).order_by('-id')
        search_str = self.request.query_params.get("search_str") or ""

        if search_str:
            queryset = queryset.filter(
               Q(first_name__icontains=search_str) |
               Q(last_name__icontains=search_str) |
               Q(email__icontains=search_str) |
               Q(company__name__icontains=search_str)
            )

        page_size = request.query_params.get('page_size') or 10
        paginator = PageNumberPagination()
        paginator.page_size = page_size

        return paginator.get_paginated_response(
            client_serializer.ClientSerializer(
                instance=paginator.paginate_queryset(
                    queryset, request
                ),
                many=True
            ).data
        )

    @action(methods=['POST'], detail=False)
    def add_existing_leads(self, request, pk=None):
        """
        <POST> url: api/client/add_existing_leads/
        """

        data = request.data

        client = core_model.Client.objects.filter(
            id=int(data.get('client'))
        ).first()

        account_id = core_model.Account.objects.filter(
            employee_id=data.get("lead_owner")
        ).first()

        if not client:
            return Response(
                {
                    "success": False,
                    "message": "client id not found"
                }, status=status.HTTP_400_NOT_FOUND)

        with transaction.atomic():
            li = core_model.LeadInformation.objects.filter(
                client=client
            ).first()

            if li:
                f_name = "%s %s" % (
                    client.first_name,
                    client.last_name
                )
                so = core_model.ServiceOffered.objects.filter(
                    id=data.get("service")
                ).first()

                message = (
                    f"Say hello again to {f_name} "
                    f"added by {data.get('session')} "
                    f"avail service of {so}"
                )

                lead_info = core_model.LeadInformation(
                    client=client,
                    source=li.source,
                    status_label=3,
                    status=5
                )
                if client.company.name:
                    lead_info.type = 1
                else:
                    lead_info.type = 2

                lead_info.save()

                lead_service = core_model.LeadServices(
                    lead_info=lead_info,
                    service=so
                )
                lead_service.save()

                lead_owner = core_model.LeadOwner(
                    lead=lead_info,
                    date_handle=current_time_ph,
                    account=account_id
                )

                lead_owner.save()

                Core.create_activity(
                    lead_info=lead_info,
                    message=message,
                    type=core_model.Activity.NEWLEADS,
                    status=core_model.Activity.ACTIVE,
                    date_generated=current_time_ph,
                    owner=data.get("session")
                )
        return Response(
            {
                "success": True,
                "message": (
                    "Exisiting leads add another "
                    "service successfully."
                )
            }, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False)
    def contacted_csv_leads(self, request, pk=None):
        """
        <POST> url: api/client/contacted_csv_leads/
            request = [
                {
                    "first_name": "John",
                    "last_name": "Doe",
                    "phone_num": 09182475698,
                    "tel_num": 908-098-09,
                    "email": johndoe@gmail.com,
                    "job_title": "Programmer",
                    "company_name":
                    "One Outsource Direct Company",
                    "address": "makati",
                    "remarks: "new found lead",
                    "company_size": 10,
                    "lead_owner": ""
                    "department": ""
                    "type": 1,
                    "source": facebook,
                    "industry":
                    "Telecommunications"
                }
            ]
        """

        data = request.data
        print(data)

        with transaction.atomic():
            session = data.get("session")
            account_id = core_model.Account.objects.filter(
                    employee_id=data.get("lead_owner")
            ).first()

            for lead in data.get('bulk_lead'):

                company = core_model.CompanyInformation()

                industry_name = lead.get('industry')
                industry = core_model.Industry.objects.filter(
                    name=industry_name
                ).first()

                if lead.get("company"):
                    company.name = lead.get("company")
                if lead.get('address'):
                    company.address = lead.get("address")
                if lead.get('company_size'):
                    company.company_size = lead.get('company_size')
                if lead.get('industry'):
                    company.industry = industry

                company.save()

                client = core_model.Client(
                    company=company,
                    first_name=lead.get("first_name"),
                    last_name=lead.get("last_name")
                )

                if lead.get('phone_num'):
                    client.phone_num = lead.get("phone_num")
                if lead.get('tel_num'):
                    client.tel_num = lead.get("tel_num")
                if lead.get('email'):
                    client.email = lead.get("email")
                if lead.get('job_title'):
                    client.job_title = lead.get("job_title")
                if lead.get('department'):
                    client.department = lead.get("department")

                client.save()

                lead_info = core_model.LeadInformation(
                    client=client
                )
                if lead.get("company"):
                    lead_info.type = 1
                else:
                    lead_info.type = 2

                if lead.get('source'):
                    lead_info.source = lead.get('source')

                if lead.get('remarks'):
                    lead_info.remarks = lead.get('remarks')

                lead_info.status = 2
                lead_info.status_label = 2
                lead_info.save()

                lead_owner = core_model.LeadOwner(
                    lead=lead_info,
                    account=account_id,
                    date_handle=current_time_ph
                )
                lead_owner.save()

                f_name = lead.get("first_name")
                l_name = lead.get("last_name")
                message = (
                    f"Say hello to our latest lead {f_name} {l_name},"
                    f" joining our journey towards greater"
                    f" opportunities and success!"
                    f" added by {session}."
                )

                Core.create_activity(
                    lead_info=lead_info,
                    message=message,
                    type=core_model.Activity.NEWLEADS,
                    status=core_model.Activity.ACTIVE,
                    date_generated=current_time_ph,
                    owner=lead.get("lead_owner")
                )

        return Response(
            {
                "success": True,
                "message": "Imported leads uploaded successfully"
            }, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False)
    def pipeline_csv_leads(self, request, pk=None):
        """
        <POST> url: api/client/contacted_csv_leads/
            request = [
                {
                    "first_name": "John",
                    "last_name": "Doe",
                    "phone_num": 09182475698,
                    "tel_num": 908-098-09,
                    "email": johndoe@gmail.com,
                    "job_title": "Programmer",
                    "company_name":
                    "One Outsource Direct Company",
                    "address": "makati",
                    "remarks: "new found lead",
                    "company_size": 10,
                    "lead_owner": ""
                    "department": ""
                    "type": 1,
                    "source": facebook,
                    "industry":
                    "Telecommunications"
                }
            ]
        """

        data = request.data
        print(data)

        with transaction.atomic():
            session = data.get("session")
            account_id = core_model.Account.objects.filter(
                    employee_id=data.get("lead_owner")
            ).first()

            for lead in data.get('bulk_lead'):

                company = core_model.CompanyInformation()

                industry_name = lead.get('industry')
                industry = core_model.Industry.objects.filter(
                    name=industry_name
                ).first()

                if lead.get("company"):
                    company.name = lead.get("company")
                if lead.get('address'):
                    company.address = lead.get("address")
                if lead.get('company_size'):
                    company.company_size = lead.get('company_size')
                if lead.get('industry'):
                    company.industry = industry

                company.save()

                client = core_model.Client(
                    company=company,
                    first_name=lead.get("first_name"),
                    last_name=lead.get("last_name")
                )

                if lead.get('phone_num'):
                    client.phone_num = lead.get("phone_num")
                if lead.get('tel_num'):
                    client.tel_num = lead.get("tel_num")
                if lead.get('email'):
                    client.email = lead.get("email")
                if lead.get('job_title'):
                    client.job_title = lead.get("job_title")
                if lead.get('department'):
                    client.department = lead.get("department")

                client.save()

                lead_info = core_model.LeadInformation(
                    client=client
                )
                if lead.get("company"):
                    lead_info.type = 1
                else:
                    lead_info.type = 2

                if lead.get('source'):
                    lead_info.source = lead.get('source')

                if lead.get('remarks'):
                    lead_info.remarks = lead.get('remarks')

                lead_info.status = 5
                lead_info.status_label = 3
                lead_info.save()

                lead_owner = core_model.LeadOwner(
                    lead=lead_info,
                    account=account_id,
                    date_handle=current_time_ph
                )
                lead_owner.save()

                f_name = lead.get('first_name').title()
                l_name = lead.get('last_name').title()
                message = (
                    f"Say hello to our latest lead {f_name} {l_name},"
                    f" joining our journey towards greater"
                    f" opportunities and success!"
                    f" added by {session}."
                )

                Core.create_activity(
                    lead_info=lead_info,
                    message=message,
                    type=core_model.Activity.NEWLEADS,
                    status=core_model.Activity.ACTIVE,
                    date_generated=current_time_ph,
                    owner=lead.get("lead_owner")
                )

        return Response(
            {
                "success": True,
                "message": "Imported leads uploaded successfully"
            }, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def fetch_dashboard_table(self, request, pk=None):
        """
        <GET> url: api/client/fetch_dashboard_table/
        ?page=1%page_size=10&search_str="
        """
        queryset = core_model.LeadInformation.objects.filter(
            Q(status_label=3) | Q(status_label=4), condition=1
        ).order_by('-id')
        search_str = self.request.query_params.get("search_str") or ""
        year = self.request.query_params.get("year")

        if search_str:
            queryset = queryset.filter(
               Q(client__first_name__icontains=search_str) |
               Q(client__last_name__icontains=search_str) |
               Q(client__email__icontains=search_str) |
               Q(client__company__name__icontains=search_str)
            )

        page_size = request.query_params.get('page_size') or 100
        paginator = PageNumberPagination()
        paginator.page_size = page_size

        return paginator.get_paginated_response(
            client_serializer.DashboardTableSerializer(
                instance=paginator.paginate_queryset(
                    queryset, request,
                ), many=True, context={'year': year}
            ).data
        )

    @action(methods=['GET'], detail=False)
    def fetch_status_count(self, request, pk=None):
        """
        <GET> url: api/client/fetch_status_count/
        """

        leaad_info = core_model.LeadInformation.objects.all()

        if not leaad_info:
            return Response(
                {
                    "success": False,
                    "message": "Request failed"
                }, status=status.HTTP_400_NOT_FOUND)

        return Response(
            {
                "success": True,
                "data": client_serializer.LeadStatusCountSerializer(
                    instance=leaad_info,
                    many=False
                ).data
            }, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def fetch_monthly_total(self, request, pk=None):
        """
        <GET> url: api/client/fetch_monthly_total/
        """

        monthly_term = core_model.TermStatus.objects.all()
        year = self.request.query_params.get("year")

        return Response(
            {
                "success": True,
                "data": client_serializer.LeadTotalPaymentSerializer(
                    instance=monthly_term,
                    many=False, context={'year': year}
                ).data
            }, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def fetch_pipeline_total(self, request, pk=None):
        """
        <GET> url: api/client/fetch_pipeline_total/
        """

        lead_service = core_model.LeadServices.objects.filter(
            lead_info__condition=1
        ).first()

        return Response(
            {
                "success": True,
                "data": client_serializer.PipelineStatusSerializer(
                    instance=lead_service,
                    many=False
                ).data
            }, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def fetch_agent_leads(self, request, pk=None):
        """
        <GET> url: api/client/fetch_agent_leads/
        ?page=1%page_size=10&search_str="
        """
        queryset = core_model.Account.objects.filter(
            Q(type=2) | Q(type=3)
        ).order_by('-id')
        search_str = self.request.query_params.get("search_str") or ""

        if search_str:
            queryset = queryset.filter(
               Q(user__first_name__icontains=search_str) |
               Q(user__last_name__icontains=search_str)
            )

        page_size = request.query_params.get('page_size') or 10
        paginator = PageNumberPagination()
        paginator.page_size = page_size

        return paginator.get_paginated_response(
            client_serializer.PerformanceReportSerializer(
                instance=paginator.paginate_queryset(
                    queryset, request
                ), many=True
            ).data
        )

    @action(methods=['GET'], detail=False)
    def fetch_revenue_total(self, request, pk=None):
        """
        <GET> url: api/client/fetch_revenue_total/
        """

        lead_service = core_model.LeadServices.objects.filter(
            lead_info__condition=1
        ).first()

        return Response(
            {
                "success": True,
                "data": client_serializer.TotalRevenueSerializer(
                    instance=lead_service,
                    many=False
                ).data
            }, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def add_attachment(self, request, pk=None):
        """
        <POST> url: api/client/add_attachement/
        request = {
            "lead_service": 1,
            "file": [file],
            "label": "label"
        }
        """

        data = request.data
        print(data)
        message = (
            f"{data.get('session')} add new attachment"
        )

        lead_info = core_model.LeadInformation.objects.filter(
                id=int(data.get('lead_info'))
            ).first()

        if not lead_info:
            return Response(
                {
                    "success": False,
                    "message": "Lead service id not found"
                }, status=status.HTTP_200_OK)

        account = core_model.Account.objects.filter(
            employee_id=int(data.get('emp_id'))
        ).first()

        if not account:
            return Response(
                {
                    "success": False,
                    "message": "Account id not found"
                }, status=status.HTTP_200_OK)

        with transaction.atomic():

            for file in request.FILES.getlist('file'):
                attachment = core_model.Attachment(
                    lead_info=lead_info,
                    uploaded_by=account,
                    date_inserted=current_time_ph,
                    file=file
                )

                attachment.label = data.get('label') or ""
                attachment.save()

            Core.create_activity(
                lead_info=lead_info,
                message=message,
                type=core_model.Activity.NEWLEADS,
                status=core_model.Activity.ACTIVE,
                date_generated=current_time_ph,
                owner=data.get("session")
            )
        return Response(
            {
                "success": True,
                "message": "Attachment successfully uploaded"
            }, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def fetch_lead_attachment(self, request, pk=None):
        """
        <GET> url: api/clients/fetch_lead_attachment/id=1
        """

        id = request.query_params.get('id')

        lead_info = core_model.LeadInformation.objects.filter(
            id=id
        ).first()

        attachments = core_model.Attachment.objects.filter(
            lead_info=lead_info, status=1
        ).order_by('-id')

        page_size = request.query_params.get('page_size') or 5
        paginator = PageNumberPagination()
        paginator.page_size = page_size

        return paginator.get_paginated_response(
            client_serializer.AttachmentSerializer(
                instance=paginator.paginate_queryset(
                    attachments, request
                ),
                many=True
            ).data
        )

    @action(methods=['PUT'], detail=False)
    def fetch_delete_attachment(self, request, pk=None):
        """
        <GET> url: api/clients/fetch_delete_attachment/id=1
        """

        data = request.data
        print(data)

        attachment = core_model.Attachment.objects.filter(
            id=data.get('id')
        ).first()

        attachment.status = 2
        attachment.save()

        message = (
            f"{data.get('session')} deleted an attachment"
        )

        Core.create_activity(
                lead_info=attachment.lead_info,
                message=message,
                type=core_model.Activity.NEWLEADS,
                status=core_model.Activity.ACTIVE,
                date_generated=current_time_ph,
                owner=data.get("session")
            )

        return Response(
            {
                "success": True,
                "message": "Successfully deleted"
            },
            status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=True)
    def fetch_term_status(self, request, pk=None):
        """
        <GET> url: api/client/<id>/fetch_term_status/
        """

        service_query = core_model.LeadServices.objects.filter(
            id=pk
        ).first()

        if not service_query:
            return Response(
                {
                    "success": False,
                    "message": "Id not found"
                }, status=status.HTTP_200_OK
            )
        return Response(
            {
                "success": True,
                "data": client_serializer.MsfBreakdownSerializer(
                    instance=service_query,
                    many=False
                ).data
            }, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def edit_msf_breakdown(self, request, pk=None):
        """
        <POST> url: api/client/edit_msf_breakdown/
        """

        data = request.data

        lead_service_query = core_model.LeadServices.objects.filter(
            id=int(data.get('leadId'))
        ).first()

        message = (
            f"{data.get('session')} updated the monthly "
            f"service fee breakdown."
        )

        if not lead_service_query:
            return Response(
                {
                    "success": False,
                    "message": "lead service id not found."
                }, status=status.HTTP_400_NOT_FOUND)

        with transaction.atomic():
            lead_service_query.revenue = data.get('revenue')
            lead_service_query.save()

            for term_input in data.get('newInput'):
                term_query = core_model.TermStatus.objects.filter(
                    id=term_input.get('id')
                ).first()

                if term_query:
                    term_query.msf = term_input.get('newMsf')
                    term_query.save()

            Core.create_activity(
                lead_info=lead_service_query.lead_info,
                message=message,
                type=core_model.Activity.NEWLEADS,
                status=core_model.Activity.ACTIVE,
                date_generated=current_time_ph,
                owner=data.get("session")
            )

        return Response(
            {
                "success": True,
                "message": "Monthly service fee updated"
            }, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def fetch_notification(self, request, pk=None):
        """
        <GET> url: api/client/fetch_notification/
        ?page=1&page_size=10&employee_id=23
        """

        employee_id = request.query_params.get('employee_id')
        notification = core_model.Notification.objects.filter(
            receiver__employee_id=employee_id, status=1
        ).order_by('-id')

        page_size = request.query_params.get('page_size') or 5
        paginator = PageNumberPagination()
        paginator.page_size = page_size

        return paginator.get_paginated_response(
            client_serializer.NotificationSerializer(
                instance=paginator.paginate_queryset(
                    notification, request
                ),
                many=True
            ).data
        )

    @action(methods=['PUT'], detail=True)
    def seen_notification(self, request, pk=None):
        """
        <PUT> url: api/client/id/seen_notification/
        """

        core_model.Notification.objects.filter(
            id=pk
        ).update(is_seen=True, date_seen=current_time_ph)

        return Response(
            {
                "success": True,
                "message": "Message is already seen"
            }, status=status.HTTP_200_OK)

    @action(methods=['PUT'], detail=True)
    def delete_notification(slef, request, pk=None):
        """
        <GET> url: api/client/id/delete_notification
        """

        notification = core_model.Notification.objects.filter(
            id=pk
        ).first()

        if notification:
            notification.status = 2
            if not notification.is_seen:
                notification.is_seen = True

            notification.save()

        return Response(
            {
                "success": True,
                "message": "Notification deleted successfully"
            }, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def count_notification(self, request, pk=None):
        """
        <GET>  url: api/client/count_notification
        """

        employee_id = request.query_params.get('employee_id')
        notification = core_model.Notification.objects.filter(
            status=1, is_seen=False, receiver__employee_id=employee_id
        ).count()

        return Response(
            {
                "success": True,
                "data": notification
            }, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False)
    def custom_fetch(self, request, pk=None):
        """
        <GET> url: api/client/custom_leads/
        """

        queryset = core_model.LeadOwner.objects.filter(
            lead__condition=1
        ).order_by('-id')

        return Response(
            {
                "success": True,
                "data": client_serializer.CustomSerializer(
                    instance=queryset, many=True
                ).data
            }, status=status.HTTP_200_OK)
