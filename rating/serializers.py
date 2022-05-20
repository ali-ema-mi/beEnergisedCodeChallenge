from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from rating.models import Invoice


class BaseSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class RateSerializer(BaseSerializer):
    energy = serializers.FloatField(min_value=0, required=True)
    time = serializers.FloatField(min_value=0, required=True)
    transaction = serializers.FloatField(min_value=0, required=True)


class CDRSerializer(BaseSerializer):
    meterStart = serializers.IntegerField(min_value=0, default=0)
    timestampStart = serializers.DateTimeField(required=True)
    meterStop = serializers.IntegerField(min_value=0, default=0)
    timestampStop = serializers.DateTimeField(required=True)

    def validate(self, attrs):
        if attrs.get('meterStop') < attrs.get('meterStart'):
            raise serializers.ValidationError(_('Meter start should be lower than meter stop'))

        if attrs.get('timestampStop') < attrs.get('timestampStart'):
            raise serializers.ValidationError(_('Start time should be lower than stop time'))

        return attrs


class InvoiceSerializerInput(serializers.ModelSerializer):
    rate = RateSerializer(write_only=True)
    cdr = CDRSerializer(write_only=True)

    class Meta:
        model = Invoice
        fields = '__all__'
        extra_kwargs = {
            'meterStart': {'read_only': True},
            'meterStop': {'read_only': True},
            'timestampStart': {'read_only': True},
            'timestampStop': {'read_only': True},
            'energy': {'read_only': True},
            'time': {'read_only': True},
            'transaction': {'read_only': True},
        }


class InvoiceSerializerOutput(BaseSerializer):
    overall = serializers.SerializerMethodField()
    components = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'

    @staticmethod
    def get_overall(obj):
        return obj.price()

    @staticmethod
    def get_components(obj):
        return {"energy": obj.energy_price, "time": obj.time_price, "transaction": obj.transaction_price}
