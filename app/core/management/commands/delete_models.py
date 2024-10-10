from django.core.management.base import BaseCommand
from core import models as core_models


class Command(BaseCommand):
    help = "Delete Models"

    def delete_activity(self):
        activity, _ = core_models.Activity.objects.all(
        ).delete()

        self.stdout.write(self.style.SUCCESS(
            f"Successfully deleted {activity}"
        ))

    def delete_lead_services(self):
        lead_service, _ = core_models.LeadServices.objects.all(
        ).delete()

        self.stdout.write(self.style.SUCCESS(
            f"Successfully deleted {lead_service}"
        ))

    def delete_lead_owner(self):
        lead_owner, _ = core_models.LeadOwner.objects.all(
        ).delete()

        self.stdout.write(self.style.SUCCESS(
            f"Successfully deleted {lead_owner}"
        ))

    def delete_lead_information(self):
        lead_owner, _ = core_models.LeadInformation.objects.all(
        ).delete()

        self.stdout.write(self.style.SUCCESS(
            f"Successfully deleted {lead_owner}"
        ))

    def delete_client(self):
        client, _ = core_models.Client.objects.all(
        ).delete()

        self.stdout.write(self.style.SUCCESS(
            f"Successfully deleted {client}"
        ))

    def delete_company_information(self):
        company, _ = core_models.CompanyInformation.objects.all(
        ).delete()

        self.stdout.write(self.style.SUCCESS(
            f"Successfully deleted {company}"
        ))

    def handle(self, *args, **options):
        self.delete_activity()
        self.delete_lead_services()
        self.delete_lead_owner()
        self.delete_lead_information()
        self.delete_client()
        self.delete_company_information()
