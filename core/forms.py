from django import forms

class AmortizationForm(forms.Form):
    amount = forms.DecimalField(label='Monto del préstamo', max_digits=12, decimal_places=2)
    interest_rate = forms.FloatField(label='Tasa de interés anual (%)')
    term = forms.IntegerField(label='Plazo en meses')
    start_date = forms.DateField(label='Fecha de inicio', widget=forms.DateInput(attrs={'type': 'date'}))

class SinkingFundForm(forms.Form):
    target_amount = forms.DecimalField(label='Monto objetivo', max_digits=12, decimal_places=2)
    interest_rate = forms.FloatField(label='Tasa de interés anual (%)')
    term = forms.IntegerField(label='Plazo en años')
    start_date = forms.DateField(label='Fecha del primer depósito', widget=forms.DateInput(attrs={'type': 'date'})) 