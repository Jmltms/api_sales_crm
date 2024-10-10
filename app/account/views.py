from rest_framework import (
    viewsets,
    status
)
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from account import serializers as account_serializer
from core import models as core_model
# from django.db import transaction
from django.db.models import Q


class AccountView(viewsets.ModelViewSet):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(methods=['GET'], detail=True)
    def fetch_detailed_account(self, request, pk=None):
        """
        <GET> url:/api/account/<user_id>/fetch_detailed_account
        """
        account = core_model.Account.objects.filter(
            user__id=pk
        ).first()

        if not account:
            return Response(
                {'message': 'Account not found!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {
                "success": True,
                "data": account_serializer.AccountSerializer(
                    instance=account,
                    many=False
                ).data
            }, status=status.HTTP_200_OK
        )

    @action(methods=["GET"], detail=False)
    def fetch_staff_account(self, request, pk=None):
        """
        <GET> url: api/account/fetch_staff_account/
            ?page=1&page_size=5
        """
        queryset = core_model.Account.objects.filter(
            # user__is_staff=True,
            type__in=[2, 3]
            )
        search_str = self.request.query_params.get("search_str")
        if search_str:
            queryset = queryset.filter(
                Q(employee_id__icontains=search_str) |
                Q(user__first_name__icontains=search_str) |
                Q(user__last_name__icontains=search_str)
            )

        page_size = 5
        paginator = PageNumberPagination()
        paginator.page_size = page_size

        return paginator.get_paginated_response(
            account_serializer.AccountSerializer(
                instance=paginator.paginate_queryset(
                    queryset, request
                ),
                many=True
            ).data
        )

    @action(methods=["GET"], detail=False)
    def fetch_all_staff(self, request, pk=None):
        """
        <GET> url: api/account/fetch_all_staff/
        """

        all_staff = core_model.Account.objects.filter(
            type__in=[2, 3]
        )
        serializer = account_serializer.AccountSerializerNonPaginated(
            all_staff,
            many=True)

        return Response(
            {
                "success": True,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
