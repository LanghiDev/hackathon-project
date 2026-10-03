from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from . import models, serializers
from .filters import build_filterset_fields


class BaseModelViewSet(viewsets.ModelViewSet):
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
    - ``ModelViewSet`` provides list/retrieve/create/update/partial_update/
      destroy. (Requirements 3.2-3.7)
    """

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'


class BranchViewSet(BaseModelViewSet):
    """CRUD + filter/search/order for Branch. (Requirements 3.1, 7.1, 7.3)"""

    queryset = models.Branch.objects.all()
    serializer_class = serializers.BranchSerializer
    filterset_fields = build_filterset_fields(models.Branch)
    search_fields = ['branch_id', 'branch_code', 'branch_name', 'city', 'state']


class CustomerViewSet(BaseModelViewSet):
    """CRUD + filter/search/order for Customer. (Requirements 3.1, 7.1, 7.3)"""

    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerSerializer
    filterset_fields = build_filterset_fields(models.Customer)
    search_fields = ['customer_id', 'document_number', 'first_name', 'last_name', 'email']


class ServiceAgentViewSet(BaseModelViewSet):
    """CRUD + filter/search/order for ServiceAgent. (Requirements 3.1, 7.1, 7.3)"""

    queryset = models.ServiceAgent.objects.all()
    serializer_class = serializers.ServiceAgentSerializer
    filterset_fields = build_filterset_fields(models.ServiceAgent)
    search_fields = ['agent_id', 'employee_code', 'first_name', 'last_name', 'email']


class ProductViewSet(BaseModelViewSet):
    """CRUD + filter/search/order for Product. (Requirements 3.1, 7.1, 7.3)"""

    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    filterset_fields = build_filterset_fields(models.Product)
    search_fields = ['product_id', 'product_number']


class MarketingCampaignViewSet(BaseModelViewSet):
    """CRUD + filter/search/order for MarketingCampaign. (Requirements 3.1, 7.1, 7.3)"""

    queryset = models.MarketingCampaign.objects.all()
    serializer_class = serializers.MarketingCampaignSerializer
    filterset_fields = build_filterset_fields(models.MarketingCampaign)
    search_fields = ['campaign_id', 'campaign_name', 'promoted_product']


class TransactionViewSet(BaseModelViewSet):
    """CRUD + filter/search/order for Transaction. (Requirements 3.1, 7.1, 7.3)"""

    queryset = models.Transaction.objects.all()
    serializer_class = serializers.TransactionSerializer
    filterset_fields = build_filterset_fields(models.Transaction)
    search_fields = ['transaction_id', 'merchant_name', 'merchant_category']


class CallCenterInteractionViewSet(BaseModelViewSet):
    """CRUD + filter/search/order for CallCenterInteraction. (Requirements 3.1, 7.1, 7.3)"""

    queryset = models.CallCenterInteraction.objects.all()
    serializer_class = serializers.CallCenterInteractionSerializer
    filterset_fields = build_filterset_fields(models.CallCenterInteraction)
    search_fields = ['interaction_id', 'contact_reason', 'mentioned_products']


class CallTranscriptViewSet(BaseModelViewSet):
    """CRUD + filter/search/order for CallTranscript. (Requirements 3.1, 7.1, 7.3)"""

    queryset = models.CallTranscript.objects.all()
    serializer_class = serializers.CallTranscriptSerializer
    filterset_fields = build_filterset_fields(models.CallTranscript)
    search_fields = ['transcript_id', 'detected_keywords', 'main_topics']


class SatisfactionSurveyViewSet(BaseModelViewSet):
    """CRUD + filter/search/order for SatisfactionSurvey. (Requirements 3.1, 7.1, 7.3)"""

    queryset = models.SatisfactionSurvey.objects.all()
    serializer_class = serializers.SatisfactionSurveySerializer
    filterset_fields = build_filterset_fields(models.SatisfactionSurvey)
    search_fields = ['survey_id']


class DigitalEventViewSet(BaseModelViewSet):
    """CRUD + filter/search/order for DigitalEvent. (Requirements 3.1, 7.1, 7.3)"""

    queryset = models.DigitalEvent.objects.all()
    serializer_class = serializers.DigitalEventSerializer
    filterset_fields = build_filterset_fields(models.DigitalEvent)
    search_fields = ['event_id', 'session_id', 'page_title', 'action']


class ComplaintViewSet(BaseModelViewSet):
    """CRUD + filter/search/order for Complaint. (Requirements 3.1, 7.1, 7.3)"""

    queryset = models.Complaint.objects.all()
    serializer_class = serializers.ComplaintSerializer
    filterset_fields = build_filterset_fields(models.Complaint)
    search_fields = ['complaint_id', 'category', 'subcategory']


class CampaignSendViewSet(BaseModelViewSet):
    """CRUD + filter/search/order for CampaignSend. (Requirements 3.1, 7.1, 7.3)"""

    queryset = models.CampaignSend.objects.all()
    serializer_class = serializers.CampaignSendSerializer
    filterset_fields = build_filterset_fields(models.CampaignSend)
    search_fields = ['send_id', 'subject', 'template_used']


class DailyExchangeRateViewSet(BaseModelViewSet):
    """CRUD + filter/search/order for DailyExchangeRate. (Requirements 3.1, 7.1, 7.3)"""

    queryset = models.DailyExchangeRate.objects.all()
    serializer_class = serializers.DailyExchangeRateSerializer
    filterset_fields = build_filterset_fields(models.DailyExchangeRate)
    search_fields = ['source', 'source_currency', 'target_currency']
