import calendar
from datetime import date

from celery import shared_task
from django.conf import settings
from django.db.models import Sum

from ..debts.models import Debt
from ..incomes.models import Income
from ..users.models import User
from .models import Expense


def send_monthly_report(user: User):
    """Send monthly report to user."""
    expenses = Expense.objects.filter(user=user, created_at__month=date.today().month - 1)

    total_expenses = expenses.total()

    total_by_categories = expenses.total_by_categories()

    report = expenses.report()

    income = Income.objects.filter(user=user, created_at__month=date.today().month - 1).aggregate(total=Sum("amount"))

    unpaid_debts = Debt.objects.filter(
        person=user, is_paid=False, deadline__month=date.today().month - 1, type=Debt.DebtType.LEND.value
    ).count()
    overdue_debts = Debt.objects.filter(
        person=user, is_paid=False, deadline__month=date.today().month - 1, type=Debt.DebtType.BORROW.value
    ).count()

    subject = "Monthly report"

    message = f"""
        <h1>Report for {calendar.month_name[date.today().month - 1]}.</h1>
        <br>
        <h2>Incomes: {income.get("total") or 0} {user.currency}</h2>
        <h2>Spent: {total_expenses.get("amount") or 0} {user.currency}</h2>
        <br>
        <h2>Debts:</h2>
        <h3>Unpaid lent left: {unpaid_debts}</h3>
        <h3>Unpaid borrowed left: {overdue_debts}</h3>
        <br>
        <h2>Expenses by categories:</h2>
        <ul>
        """
    for category in total_by_categories:
        message += f"<li><h3>{category['category']}: {category['total']}  {user.currency}</h3></li>"
    message += "</ul>"
    message += "<br>"
    message += "<h2>Expenses by days:</h2>"
    for day in report:
        message += f"<h3>{day['date'].day} {calendar.month_name[date.today().month - 1]}</h3>"
        message += "<ul>"
        for category in day["total_by_categories"]:
            message += f"<li><h4>{category['category']}: {category['total']}  {user.currency}</h4></li>"
        message += "</ul>"
    message += "</ul>"
    message += "<ul>"
    user.email_user(subject, message, html_message=message, from_email=settings.EMAIL_HOST_USER)


@shared_task(name="monthly_report")
def monthly_report():
    for user in User.objects.filter(is_active=True, email__isnull=False):
        send_monthly_report(user)
