from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Invoice(models.Model):
    """
    model for keeping Charge detail record and rate data
    """
    meterStart = models.PositiveIntegerField(verbose_name=_('Meter start'), default=0)
    timestampStart = models.DateTimeField(verbose_name=_('Time stamp start'))
    meterStop = models.PositiveIntegerField(verbose_name=_('Meter stop'), default=0)
    timestampStop = models.DateTimeField(verbose_name=_('Time stamp stop'))
    energy = models.FloatField(verbose_name=_('Energy fee'), help_text=_('Energy fee in € per kWh'), default=0)
    time = models.FloatField(verbose_name=_('Time fee'), help_text=_('Time fee in € per hour'), default=0)
    transaction = models.FloatField(verbose_name=_('Transaction fee'), help_text=_('Transaction fee in € per service'),
                                    default=0)

    class Meta:
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')
        ordering = ['-timestampStart', '-timestampStop']

    def clean(self):
        if self.meterStop < self.meterStart:
            raise ValidationError(_('Meter start should be lower than meter stop'))

        if self.timestampStop and self.timestampStart and self.timestampStop < self.timestampStart:
            raise ValidationError(_('Start time should be lower than stop time'))

        for field in ['energy', 'time', 'transaction']:
            if getattr(self, field) < 0:
                raise ValidationError(_(f'{field} fee should be a positive number'))

    @property
    def energy_price(self):
        try:
            # calculate energy in kW
            energy_amount = (self.meterStop - self.meterStart) / 1000
            # calculate energy price component in a precision of 3 digits
            return round(energy_amount * self.energy, 3)
        except Exception:
            return 0

    @property
    def time_price(self):
        try:
            # calculate time in hour
            time_amount = (self.timestampStop - self.timestampStart).total_seconds() / 3600
            # calculate time price component in 3 digits precision
            return round(time_amount * self.time, 3)
        except Exception:
            return 0

    @property
    def transaction_price(self):
        try:
            transaction_amount = 1
            # calculate transaction price component in a precision of 3 digits
            return round(transaction_amount * self.transaction, 3)
        except Exception:
            return 0

    def price(self):
        # calculate total price in a precision of 2 digits
        return round(self.energy_price + self.time_price + self.transaction_price, 2)

    price.short_description = _('Price in €')
