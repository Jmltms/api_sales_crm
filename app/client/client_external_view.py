from rest_framework import (
    viewsets,
    status
)
from rest_framework.decorators import action
from rest_framework.response import Response
from core import models as core_model
from django.db import transaction
from django.utils import timezone
from core.core_function import Core


class ExternalView(viewsets.ModelViewSet):

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
        }
        """
        data = request.data
        print(data)
        f_name = data.get('first_name')
        l_name = data.get('last_name')
        message = (
            f"Say hello to our latest lead {f_name} {l_name},"
            f" joining our journey towards greater opportunities and success!"
            f" added by Zoho platform."
        )

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

            if exist_email:
                return Response(
                    {
                        "success": False,
                        "message": "Provided email has already used"
                    }, status=status.HTTP_200_OK)
            else:
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
                for fields in ['first_name', 'last_name', 'phone_num',
                               'tel_num', 'email', 'job_title',
                               'department', 'remarks']:

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

                lead_owner = core_model.LeadOwner(
                    lead=lead_info,
                    date_handle=timezone.now(),
                    account=account_id
                )

                lead_owner.save()

                Core.create_activity(
                    lead_info=lead_info,
                    message=message,
                    type=core_model.Activity.NEWLEADS,
                    status=core_model.Activity.ACTIVE,
                    date_generated=timezone.now(),
                    owner="Zoho platform"
                )

                return Response(
                    {
                        "success": True,
                        "message": "New leads successfully uploaded"
                    }, status=status.HTTP_200_OK)
