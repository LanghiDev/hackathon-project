from rest_framework import permissions, serializers as drf_serializers, status, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from . import models, serializers
from .auth import issue_customer_token
from .filters import build_filterset_fields


class BaseModelViewSet(viewsets.ReadOnlyModelViewSet):
    """Shared base viewset wiring the three filter backends once.

    Concrete per-model viewsets inherit from this class and provide their own
    ``queryset``, ``serializer_class``, ``filterset_fields`` (via
    ``build_filterset_fields``), and ``search_fields``.

    - ``filter_backends`` enables field filtering (DjangoFilterBackend),
      free-text search (SearchFilter), and client-controlled ordering
      (OrderingFilter). (Requirements 6.1, 6.2, 7.4, 7.5)
    - ``ordering_fields = '__all__'`` allows ordering by any field; invalid
      ordering values are ignored and the model's ``Meta.ordering`` applies.
      (Requirements 7.4, 7.5, 7.6)
    - ``ReadOnlyModelViewSet`` provides list/retrieve only; the API is
      read-only for customers and the agent.
    - ``customer_field``: when set, a customer token only sees rows where this
      field equals its own ``customer_id``. Staff (Django session) see all rows.
    """

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    customer_field = None

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if self.customer_field and not user.is_staff:
            customer_id = getattr(user, 'customer_id', None)
            if customer_id is None:
                return queryset.none()
            queryset = queryset.filter(**{self.customer_field: customer_id})
        return queryset


class CustomerScopedViewSet(BaseModelViewSet):
    """Rows owned by a customer: scoped to the authenticated customer."""

    customer_field = 'customer_id'


class StaffOnlyViewSet(BaseModelViewSet):
    """Internal bank data that customers must not see."""

    permission_classes = [permissions.IsAdminUser]


class BranchViewSet(BaseModelViewSet):
    """Read + filter/search/order for Branch. (Requirements 3.1, 7.1, 7.3)"""

    queryset = models.Branch.objects.all()
    serializer_class = serializers.BranchSerializer
    filterset_fields = build_filterset_fields(models.Branch)
    search_fields = ['branch_id', 'branch_code', 'branch_name', 'city', 'state']


class CustomerViewSet(CustomerScopedViewSet):
    """Read + filter/search/order for Customer. (Requirements 3.1, 7.1, 7.3)"""

    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerSerializer
    filterset_fields = build_filterset_fields(models.Customer)
    search_fields = ['customer_id', 'document_number', 'first_name', 'last_name', 'email']


class ServiceAgentViewSet(StaffOnlyViewSet):
    """Read + filter/search/order for ServiceAgent. (Requirements 3.1, 7.1, 7.3)"""

    queryset = models.ServiceAgent.objects.all()
    serializer_class = serializers.ServiceAgentSerializer
    filterset_fields = build_filterset_fields(models.ServiceAgent)
    search_fields = ['agent_id', 'employee_code', 'first_name', 'last_name', 'email']


class ProductViewSet(CustomerScopedViewSet):
    """Read + filter/search/order for Product. (Requirements 3.1, 7.1, 7.3)"""

    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    filterset_fields = build_filterset_fields(models.Product)
    search_fields = ['product_id', 'product_number']


class MarketingCampaignViewSet(StaffOnlyViewSet):
    """Read + filter/search/order for MarketingCampaign. (Requirements 3.1, 7.1, 7.3)"""

    queryset = models.MarketingCampaign.objects.all()
    serializer_class = serializers.MarketingCampaignSerializer
    filterset_fields = build_filterset_fields(models.MarketingCampaign)
    search_fields = ['campaign_id', 'campaign_name', 'promoted_product']


class TransactionViewSet(CustomerScopedViewSet):
    """Read + filter/search/order for Transaction. (Requirements 3.1, 7.1, 7.3)"""

    queryset = models.Transaction.objects.all()
    serializer_class = serializers.TransactionSerializer
    filterset_fields = build_filterset_fields(models.Transaction)
    search_fields = ['transaction_id', 'merchant_name', 'merchant_category']


class CallCenterInteractionViewSet(CustomerScopedViewSet):
    """Read + filter/search/order for CallCenterInteraction. (Requirements 3.1, 7.1, 7.3)"""

    queryset = models.CallCenterInteraction.objects.all()
    serializer_class = serializers.CallCenterInteractionSerializer
    filterset_fields = build_filterset_fields(models.CallCenterInteraction)
    search_fields = ['interaction_id', 'contact_reason', 'mentioned_products']


class CallTranscriptViewSet(CustomerScopedViewSet):
    """Read + filter/search/order for CallTranscript. (Requirements 3.1, 7.1, 7.3)"""

    queryset = models.CallTranscript.objects.all()
    serializer_class = serializers.CallTranscriptSerializer
    filterset_fields = build_filterset_fields(models.CallTranscript)
    search_fields = ['transcript_id', 'detected_keywords', 'main_topics']


class SatisfactionSurveyViewSet(CustomerScopedViewSet):
    """Read + filter/search/order for SatisfactionSurvey. (Requirements 3.1, 7.1, 7.3)"""

    queryset = models.SatisfactionSurvey.objects.all()
    serializer_class = serializers.SatisfactionSurveySerializer
    filterset_fields = build_filterset_fields(models.SatisfactionSurvey)
    search_fields = ['survey_id']


class DigitalEventViewSet(CustomerScopedViewSet):
    """Read + filter/search/order for DigitalEvent. (Requirements 3.1, 7.1, 7.3)"""

    queryset = models.DigitalEvent.objects.all()
    serializer_class = serializers.DigitalEventSerializer
    filterset_fields = build_filterset_fields(models.DigitalEvent)
    search_fields = ['event_id', 'session_id', 'page_title', 'action']


class ComplaintViewSet(CustomerScopedViewSet):
    """Read + filter/search/order for Complaint. (Requirements 3.1, 7.1, 7.3)"""

    queryset = models.Complaint.objects.all()
    serializer_class = serializers.ComplaintSerializer
    filterset_fields = build_filterset_fields(models.Complaint)
    search_fields = ['complaint_id', 'category', 'subcategory']


class CampaignSendViewSet(CustomerScopedViewSet):
    """Read + filter/search/order for CampaignSend. (Requirements 3.1, 7.1, 7.3)"""

    queryset = models.CampaignSend.objects.all()
    serializer_class = serializers.CampaignSendSerializer
    filterset_fields = build_filterset_fields(models.CampaignSend)
    search_fields = ['send_id', 'subject', 'template_used']


class DailyExchangeRateViewSet(BaseModelViewSet):
    """Read + filter/search/order for DailyExchangeRate. (Requirements 3.1, 7.1, 7.3)"""

    queryset = models.DailyExchangeRate.objects.all()
    serializer_class = serializers.DailyExchangeRateSerializer
    filterset_fields = build_filterset_fields(models.DailyExchangeRate)
    search_fields = ['source', 'source_currency', 'target_currency']


class LoginSerializer(drf_serializers.Serializer):
    document_number = drf_serializers.CharField(max_length=20)
    date_of_birth = drf_serializers.DateField()


class CustomerLoginView(APIView):
    """POST {document_number, date_of_birth} -> {access, customer_id, first_name}."""

    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'login'

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = models.Customer.objects.filter(**serializer.validated_data).first()
        if customer is None:
            # Same message for unknown document and wrong birth date.
            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({
            'access': issue_customer_token(customer),
            'customer_id': customer.customer_id,
            'first_name': customer.first_name,
        })
