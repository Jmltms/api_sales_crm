from django.core.management.base import BaseCommand
from core import models as core_models
from django.db import transaction
import json


class Command(BaseCommand):
    help = "Upload industry data"

    def handle(self, *args, **options):
        file = open(
            'core/management/json/industry.json'
        ).read()
        json_data = json.loads(file)

        for data in json_data:
            with transaction.atomic():
                industry_name = data.get("name")
                exist_industry = core_models.Industry.objects.filter(
                    name=data.get("name")
                ).first()
                if not exist_industry:
                    industry = core_models.Industry(
                        name=industry_name,
                        field=data.get("field")
                    )
                    industry.save()
                    print(f"{industry_name} successfully uploaded.")
                else:
                    print(f"{industry_name} already exist.")
        print("Industry list successfully uploaded.")
