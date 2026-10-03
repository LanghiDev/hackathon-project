from rest_framework import serializers

from . import models


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Branch
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class ServiceAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ServiceAgent
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class MarketingCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MarketingCampaign
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class CallCenterInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CallCenterInteraction
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class CallTranscriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CallTranscript
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class SatisfactionSurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SatisfactionSurvey
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class DigitalEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DigitalEvent
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Complaint
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class CampaignSendSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CampaignSend
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class DailyExchangeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DailyExchangeRate
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
