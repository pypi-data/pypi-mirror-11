import re
from django import forms
from django.utils.translation import ugettext_lazy as _

PURSE_RE = re.compile(r'^(?P<type>[BCDEGKRUXYZ])(?P<number>\d{12})$')
WMID_RE = re.compile(r'^\d{12}$')


class PaymentRequestForm(forms.Form):
    LMI_PAYMENT_AMOUNT = forms.DecimalField(max_digits=7, decimal_places=2, widget=forms.HiddenInput())
    LMI_PAYMENT_DESC_BASE64 = forms.CharField(widget=forms.HiddenInput())
    LMI_PAYMENT_NO = forms.IntegerField(widget=forms.HiddenInput())
    LMI_PAYEE_PURSE = forms.RegexField(regex=PURSE_RE, widget=forms.HiddenInput())
    LMI_SIM_MODE = forms.IntegerField(initial="0", widget=forms.HiddenInput())


class BasePaymentForm(forms.Form):
    LMI_PAYMENT_NO = forms.IntegerField(label=_('Payment Number'))


class ExtraPaymentForm(BasePaymentForm):
    # Paymer
    LMI_PAYMER_NUMBER = forms.CharField(required=False)
    LMI_PAYMER_EMAIL = forms.EmailField(required=False)

    # Telepat
    LMI_TELEPAT_PHONENUMBER = forms.CharField(required=False)
    LMI_TELEPAT_ORDERID = forms.CharField(required=False)

    # Credit
    LMI_PAYMENT_CREDITDAYS = forms.IntegerField(min_value=0, required=False)


class PrerequestForm(ExtraPaymentForm):
    LMI_PREREQUEST = forms.BooleanField(label=_('Prerequest flag'), required=False)
    LMI_PAYEE_PURSE = forms.RegexField(regex=PURSE_RE)

    LMI_PAYMENT_AMOUNT = forms.DecimalField(max_digits=7, decimal_places=2, label=_('Amount'))
    LMI_MODE = forms.IntegerField(label=_('Test mode'), min_value=0, max_value=1)

    LMI_PAYER_WM = forms.RegexField(regex=WMID_RE)
    LMI_PAYER_PURSE = forms.RegexField(regex=PURSE_RE)


class PayedPaymentForm(BasePaymentForm):
    LMI_SYS_INVS_NO = forms.IntegerField()
    LMI_SYS_TRANS_NO = forms.IntegerField()
    LMI_SYS_TRANS_DATE = forms.DateTimeField(input_formats=['%Y%m%d %H:%M:%S'])


class PaymentNotificationForm(PrerequestForm, PayedPaymentForm):
    LMI_HASH = forms.CharField()


class SettledPaymentForm(PayedPaymentForm, ExtraPaymentForm):
    pass


class UnSettledPaymentForm(PayedPaymentForm, ExtraPaymentForm):
    pass
