from django.db import models
from django.utils.timezone import now
from datetime import timedelta, date
import calendar
from decimal import Decimal

# Loan model
class Loan(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)  # Monto del préstamo
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)  # Tasa de interés anual (en porcentaje)
    term = models.IntegerField()  # Plazo en meses
    start_date = models.DateField(default=now)  # Fecha de inicio del préstamo
    
    def monthly_payment(self):
        """
        Calcula el pago mensual usando la fórmula de amortización.
        """
        # Convertir la tasa de interés a decimal mensual
        monthly_rate = Decimal(str(self.interest_rate)) / Decimal('100') / Decimal('12')
        
        # Calcular el pago mensual
        n_payments = Decimal(str(self.term))
        numerator = monthly_rate * (Decimal('1') + monthly_rate) ** n_payments
        denominator = (Decimal('1') + monthly_rate) ** n_payments - Decimal('1')
        return self.amount * (numerator / denominator)

    def generate_amortization_schedule(self):
        """
        Genera la tabla de amortización.
        """
        schedule = []
        remaining_balance = self.amount
        monthly_payment = self.monthly_payment()
        monthly_rate = Decimal(str(self.interest_rate)) / Decimal('100') / Decimal('12')
        payment_date = self.start_date

        for month in range(1, self.term + 1):
            interest = remaining_balance * monthly_rate
            principal = monthly_payment - interest
            remaining_balance -= principal

            schedule.append({
                "month": month,
                "payment_date": payment_date,
                "monthly_payment": monthly_payment,
                "interest": interest,
                "principal": principal,
                "remaining_balance": remaining_balance,
            })

            # Incrementar la fecha al siguiente mes
            month_days = calendar.monthrange(payment_date.year, payment_date.month)[1]
            payment_date += timedelta(days=month_days)

        return schedule


# Payment model
class Payment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateField()  # Fecha en que se realizó el pago
    amount = models.DecimalField(max_digits=12, decimal_places=2)  # Monto del pago
    
    def apply_payment(self):
        """
        Apply this payment to the corresponding loan.
        Updates the remaining balance and recalculates future payments if necessary.
        """
        amortization_schedule = self.loan.generate_amortization_schedule()
        remaining_amount = self.amount

        for entry in amortization_schedule:
            if remaining_amount <= 0:
                break
            
            # Apply to interest first, then principal
            interest_to_cover = entry['interest']
            if remaining_amount >= interest_to_cover:
                remaining_amount -= interest_to_cover
                entry['interest'] = 0
            else:
                entry['interest'] -= remaining_amount
                remaining_amount = 0
                continue

            principal_to_cover = entry['principal']
            if remaining_amount >= principal_to_cover:
                remaining_amount -= principal_to_cover
                entry['principal'] = 0
            else:
                entry['principal'] -= remaining_amount
                remaining_amount = 0

            entry['remaining_balance'] = max(0, entry['remaining_balance'] - self.amount)

# Optional model for persisted amortization schedule (if needed)
class AmortizationSchedule(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name="amortization_schedules")
    month_number = models.PositiveIntegerField()
    payment_date = models.DateField()
    beginning_balance = models.DecimalField(max_digits=12, decimal_places=2)
    interest = models.DecimalField(max_digits=10, decimal_places=2)
    principal = models.DecimalField(max_digits=10, decimal_places=2)
    ending_balance = models.DecimalField(max_digits=12, decimal_places=2)
    is_paid = models.BooleanField(default=False)
