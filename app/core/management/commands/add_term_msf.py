from django.core.management.base import BaseCommand
from core import models as core_models


class Command(BaseCommand):
    help = "Add term msf"

    def handle(self, *args, **options):

        lead_service = core_models.LeadServices.objects.all()

        for ls in lead_service:
            core_models.TermStatus.objects.filter(
                lead_service=ls
            ).exclude(msf__isnull=False).update(msf=ls.msf)

            self.stdout.write(self.style.SUCCESS(
                "Msf successfully add to lead service"
            ))
