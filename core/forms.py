from django import forms

PAYMENT_FREQUENCY_CHOICES = [
    (24, 'Quincenal'),
    (12, 'Mensual'),
    (2, 'Semestral'),
    (1, 'Anual'),
]

class AmortizationForm(forms.Form):
    amount = forms.DecimalField(label='Monto del préstamo', max_digits=12, decimal_places=2)
    interest_rate = forms.FloatField(label='Tasa de interés anual (%)')
    term = forms.IntegerField(label='Plazo en años')
    payment_frequency = forms.ChoiceField(
        label='Frecuencia de pago',
        choices=PAYMENT_FREQUENCY_CHOICES,
        initial=12
    )
    start_date = forms.DateField(label='Fecha de inicio', widget=forms.DateInput(attrs={'type': 'date'}))

class SinkingFundForm(forms.Form):
    target_amount = forms.DecimalField(label='Monto objetivo', max_digits=12, decimal_places=2)
    interest_rate = forms.FloatField(label='Tasa de interés anual (%)')
    term = forms.IntegerField(label='Plazo en años')
    payment_frequency = forms.ChoiceField(
        label='Frecuencia de depósito',
        choices=PAYMENT_FREQUENCY_CHOICES,
        initial=12
    )
    start_date = forms.DateField(label='Fecha del primer depósito', widget=forms.DateInput(attrs={'type': 'date'})) 