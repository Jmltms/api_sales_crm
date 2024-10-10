from core import models as core_models
import random
import string


class Core():

    @classmethod
    def create_activity(cls, **kwargs):

        activity = core_models.Activity(
            **kwargs
        )
        activity.save()

        return 'activity'

    @classmethod
    def generate_int_str(cls, length):
        return ''.join(random.choice(
            string.ascii_letters + string.digits
        ) for _ in range(length))

    @classmethod
    def send_notification(cls, sender, receiver,
                          message, date_delivered):

        s = core_models.Account.objects.filter(
            employee_id=sender
        ).first()
        r = core_models.Account.objects.filter(
            employee_id=receiver
        ).first()

        notification = core_models.Notification(
            sender=s,
            receiver=r,
            message=message,
            date_deliver=date_delivered
        )
        notification.save()

        return 'notification'
