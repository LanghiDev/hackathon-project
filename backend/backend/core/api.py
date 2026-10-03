"""DRF router registration for the backend.core API.

A single ``DefaultRouter`` registers all 13 resource viewsets at the route
paths defined in the design's per-resource table. The router is included under
the ``api/`` prefix in ``backend/urls.py`` and also serves the browsable API
root listing every route. (Requirements 2.2, 3.1)
"""

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'branches', views.BranchViewSet)
router.register(r'customers', views.CustomerViewSet)
router.register(r'agents', views.ServiceAgentViewSet)
router.register(r'campaigns', views.MarketingCampaignViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'transactions', views.TransactionViewSet)
router.register(r'interactions', views.CallCenterInteractionViewSet)
router.register(r'transcripts', views.CallTranscriptViewSet)
router.register(r'surveys', views.SatisfactionSurveyViewSet)
router.register(r'digital-events', views.DigitalEventViewSet)
router.register(r'complaints', views.ComplaintViewSet)
router.register(r'campaign-sends', views.CampaignSendViewSet)
router.register(r'exchange-rates', views.DailyExchangeRateViewSet)
