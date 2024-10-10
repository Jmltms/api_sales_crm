from django.core.management.base import BaseCommand
from core import models as core_models
from django.db import transaction
import json


class Command(BaseCommand):
    help = "Upload outlet data"

    def handle(self, *args, **options):
        file = open('core/management/json/user.json').read()
        json_data = json.loads(file)

        with transaction.atomic():
            for data in json_data:
                u_password = data.get("password")
                email = data.get("email")
                user = core_models.User.objects.filter(
                    email=email
                ).first()

                if not user:
                    print(
                        "Username: " + data.get("email")
                        + " ====== " + "Password: " + u_password)
                    user = core_models.User(
                        first_name=data.get("first_name"),
                        last_name=data.get("last_name"),
                        middle_name=data.get("middle_name"),
                        username=data.get("username"),
                        email=data.get("email"),
                        is_active=data.get("active"),
                        is_staff=data.get("staff")
                    )

                    user.set_password(u_password)
                    user.save()

                    account = core_models.Account(
                        user=user,
                        employee_id=data.get("employee_id"),
                        gender=data.get("gender"),
                        date_hired=data.get("hired"),
                        address=data.get("address"),
                        job_title=data.get('job_title'),
                        phone_num=data.get("phone_num"),
                        status=data.get("status"),
                        type=data.get('type')
                    )
                    account.save()
                else:
                    print(
                        "Username: " + data.get("email")
                        + " ====== " + " Password: "
                        + u_password + " already exist"
                    )

        print("Successfully uploading User data ")
