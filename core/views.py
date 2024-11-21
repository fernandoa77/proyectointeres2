from django.shortcuts import render
from django.http import HttpResponse
from .forms import AmortizationForm, SinkingFundForm
import pandas as pd
from datetime import datetime, timedelta
from decimal import Decimal
import calendar

def generate_amortization_schedule(amount, interest_rate, term, payment_frequency, start_date):
    schedule = []
    rate_per_period = float(interest_rate) / (100 * payment_frequency)
    n_periods = term * payment_frequency
    
    # Cálculo del pago periódico
    payment = float(amount) * (rate_per_period * (1 + rate_per_period)**n_periods) / ((1 + rate_per_period)**n_periods - 1)
    
    remaining_balance = float(amount)
    current_date = start_date

    for period in range(1, int(n_periods) + 1):
        interest_payment = remaining_balance * rate_per_period
        principal_payment = payment - interest_payment
        remaining_balance -= principal_payment
        
        schedule.append({
            'month': period,
            'payment_date': current_date,
            'monthly_payment': payment,
            'interest': interest_payment,
            'principal': principal_payment,
            'remaining_balance': remaining_balance if remaining_balance > 0 else 0
        })
        
        # Actualizar la fecha según la frecuencia de pago
        if payment_frequency == 24:  # Quincenal
            current_date += timedelta(days=15)
        elif payment_frequency == 12:  # Mensual
            month_days = calendar.monthrange(current_date.year, current_date.month)[1]
            current_date += timedelta(days=month_days)
        elif payment_frequency == 2:  # Semestral
            for _ in range(6):
                month_days = calendar.monthrange(current_date.year, current_date.month)[1]
                current_date += timedelta(days=month_days)
        else:  # Anual
            for _ in range(12):
                month_days = calendar.monthrange(current_date.year, current_date.month)[1]
                current_date += timedelta(days=month_days)
    
    return schedule

def amortization_view(request):
    form = AmortizationForm()
    schedule = None
    
    if request.method == 'POST':
        form = AmortizationForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            interest_rate = Decimal(str(form.cleaned_data['interest_rate']))
            term = form.cleaned_data['term']
            payment_frequency = int(form.cleaned_data['payment_frequency'])
            start_date = form.cleaned_data['start_date']

            schedule = generate_amortization_schedule(
                amount, 
                interest_rate, 
                term,
                payment_frequency,
                start_date
            )

            if 'download' in request.POST:
                df = pd.DataFrame(schedule)
                df.columns = [
                    'Período',
                    'Fecha de Pago',
                    f'Pago {"Quincenal" if payment_frequency == 24 else "Mensual" if payment_frequency == 12 else "Semestral" if payment_frequency == 2 else "Anual"}',
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
            payment_frequency = int(form.cleaned_data['payment_frequency'])
            start_date = form.cleaned_data['start_date']

            schedule = generate_sinking_fund_schedule(
                target_amount, 
                interest_rate, 
                term,
                payment_frequency,
                start_date
            )

            if 'download' in request.POST:
                df = pd.DataFrame(schedule)
                df.columns = [
                    'Período',
                    'Fecha de Depósito',
                    f'Depósito {"Quincenal" if payment_frequency == 24 else "Mensual" if payment_frequency == 12 else "Semestral" if payment_frequency == 2 else "Anual"}',
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

def generate_sinking_fund_schedule(target_amount, interest_rate, term, payment_frequency, start_date):
    # Convertir todos los valores a Decimal
    target_amount = Decimal(str(target_amount))
    interest_rate = Decimal(str(interest_rate))
    term = Decimal(str(term))
    
    # Cálculo del depósito periódico
    rate_per_period = interest_rate / Decimal(str(payment_frequency)) / Decimal('100')
    n_periods = term * Decimal(str(payment_frequency))
    
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
        
        # Incrementar la fecha según la frecuencia
        if payment_frequency == 24:  # Quincenal
            current_date += timedelta(days=15)
        elif payment_frequency == 12:  # Mensual
            month_days = calendar.monthrange(current_date.year, current_date.month)[1]
            current_date += timedelta(days=month_days)
        elif payment_frequency == 2:  # Semestral
            for _ in range(6):
                month_days = calendar.monthrange(current_date.year, current_date.month)[1]
                current_date += timedelta(days=month_days)
        else:  # Anual
            for _ in range(12):
                month_days = calendar.monthrange(current_date.year, current_date.month)[1]
                current_date += timedelta(days=month_days)

    return schedule