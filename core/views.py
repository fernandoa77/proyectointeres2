from django.shortcuts import render
from django.http import HttpResponse
from .models import Loan
from .forms import AmortizationForm, SinkingFundForm
import pandas as pd
from datetime import datetime, timedelta
from decimal import Decimal
import calendar

def amortization_view(request):
    form = AmortizationForm()
    schedule = None  # Inicializamos schedule como None
    
    if request.method == 'POST':
        form = AmortizationForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            interest_rate = Decimal(str(form.cleaned_data['interest_rate']))
            term = form.cleaned_data['term']
            start_date = form.cleaned_data['start_date']

            loan = Loan(
                amount=amount,
                interest_rate=interest_rate,
                term=term,
                start_date=start_date
            )

            schedule = loan.generate_amortization_schedule()

            if 'download' in request.POST:
                df = pd.DataFrame(schedule)
                df.columns = [
                    'Mes',
                    'Fecha de Pago',
                    'Pago Mensual',
                    'Interés',
                    'Principal',
                    'Saldo Restante'
                ]
                response = HttpResponse(content_type='application/vnd.ms-excel')
                response['Content-Disposition'] = 'attachment; filename="tabla_amortizacion.xlsx"'
                df.to_excel(response, index=False)
                return response

    return render(request, 'amortization.html', {
        'form': form,
        'schedule': schedule
    })

def sinking_fund_view(request):
    form = SinkingFundForm()
    schedule = None
    
    if request.method == 'POST':
        form = SinkingFundForm(request.POST)
        if form.is_valid():
            target_amount = form.cleaned_data['target_amount']
            interest_rate = Decimal(str(form.cleaned_data['interest_rate']))
            term = form.cleaned_data['term']
            start_date = form.cleaned_data['start_date']

            schedule = generate_sinking_fund_schedule(
                target_amount, 
                interest_rate, 
                term,
                start_date
            )

            if 'download' in request.POST:
                df = pd.DataFrame(schedule)
                df.columns = [
                    'Período',
                    'Fecha de Depósito',
                    'Depósito',
                    'Interés',
                    'Saldo Acumulado'
                ]
                response = HttpResponse(content_type='application/vnd.ms-excel')
                response['Content-Disposition'] = 'attachment; filename="fondo_amortizacion.xlsx"'
                df.to_excel(response, index=False)
                return response

    return render(request, 'sinking_fund.html', {
        'form': form,
        'schedule': schedule
    })

def generate_sinking_fund_schedule(target_amount, interest_rate, term, start_date):
    # Convertir todos los valores a Decimal
    target_amount = Decimal(str(target_amount))
    interest_rate = Decimal(str(interest_rate))
    term = Decimal(str(term))
    
    # Cálculo del depósito periódico
    rate_per_period = interest_rate / Decimal('12') / Decimal('100')
    n_periods = term * Decimal('12')
    
    # Cálculo del denominador
    denominator = ((Decimal('1') + rate_per_period) ** n_periods - Decimal('1')) / rate_per_period
    deposit = target_amount / denominator

    schedule = []
    balance = Decimal('0')
    current_date = start_date

    for period in range(1, int(n_periods) + 1):
        interest = balance * rate_per_period
        balance += interest + deposit
        
        schedule.append({
            'period': period,
            'payment_date': current_date,
            'deposit': deposit,
            'interest': interest,
            'balance': balance,
        })
        
        # Incrementar la fecha al siguiente mes
        month_days = calendar.monthrange(current_date.year, current_date.month)[1]
        current_date += timedelta(days=month_days)

    return schedule