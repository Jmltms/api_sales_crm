from django.core.management.base import BaseCommand
from core import models as core_models
from django.db import transaction
import json


class Command(BaseCommand):
    help = "Upload industry data"

    def handle(self, *args, **options):
        file = open(
            'core/management/json/service_offered.json'
        ).read()
        json_data = json.loads(file)

        for data in json_data:
            with transaction.atomic():
                service_name = data.get("name")
                exist_service = core_models.ServiceOffered.objects.filter(
                    name=data.get("name")
                ).first()
                if not exist_service:
                    service = core_models.ServiceOffered(
                        name=service_name,
                        description=data.get("description")
                    )
                    service.save()
                    print(f"{service_name} successfully uploaded.")
                else:
                    print(f"{service_name} already exist.")
        print("Industry list success full uploaded.")
