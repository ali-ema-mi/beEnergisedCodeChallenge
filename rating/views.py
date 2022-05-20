from rest_framework import viewsets
from rest_framework.response import Response
from .models import Invoice
from .serializers import InvoiceSerializerInput, InvoiceSerializerOutput


class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializerInput
    queryset = Invoice.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        invoice = Invoice.objects.create(
            meterStart=validated_data['cdr']['meterStart'],
            meterStop=validated_data['cdr']['meterStop'],
            timestampStart=validated_data['cdr']['timestampStart'],
            timestampStop=validated_data['cdr']['timestampStop'],
            energy=validated_data['rate']['energy'],
            time=validated_data['rate']['time'],
            transaction=validated_data['rate']['transaction'],
        )
        return Response(InvoiceSerializerOutput(invoice).data)
