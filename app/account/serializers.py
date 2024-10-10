from rest_framework import serializers
from core import models as core_models
# from user import serializers as user_serializers


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.Account
        fields = [
            'id',
            'employee_id',
            'full_name',
            'gender',
            'date_hired',
            'job_title',
            'address',
            'phone_num',
            'status',
            'type'
        ]

    full_name = serializers.SerializerMethodField(
        'fetch_full_name'
    )

    def fetch_full_name(self, obj):
        return "%s %s" % (
            obj.user.first_name,
            obj.user.last_name
        )


class AccountSerializerNonPaginated(serializers.ModelSerializer):
    class Meta:
        model = core_models.Account
        fields = [
            'id',
            'employee_id',
            'first_name',
            'last_name',
            'gender',
            'date_hired',
            'job_title',
            'address',
            'phone_num',
            'status',
            'type'
        ]

    first_name = serializers.SerializerMethodField(
        'fetch_first_name'
    )
    last_name = serializers.SerializerMethodField(
        'fetch_last_name'
    )

    def fetch_first_name(self, obj):
        return obj.user.first_name

    def fetch_last_name(self, obj):
        return obj.user.last_name
