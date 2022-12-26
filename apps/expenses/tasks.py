import calendar
from datetime import date
from smtplib import SMTPException

from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.db.models import Sum
from django.template.loader import get_template

from ..debts.models import Debt
from ..incomes.models import Income
from ..users.models import User
from .models import Expense

logger = get_task_logger(__name__)


def send_monthly_report(user: User):
    """Send monthly report to user."""

    expenses = Expense.objects.filter(user=user, created_at__month=date.today().month - 1)
    total_expenses = expenses.total()
    total_by_categories = expenses.total_by_categories()
    expenses_by_days = expenses.report()

    income = Income.objects.filter(user=user, created_at__month=date.today().month - 1).aggregate(total=Sum("amount"))

    unpaid_lent_debts = Debt.objects.filter(
        person=user, is_paid=False, deadline__month=date.today().month - 1, type=Debt.DebtType.LEND.value
    ).count()
    unpaid_borrowed_debts = Debt.objects.filter(
        person=user, is_paid=False, deadline__month=date.today().month - 1, type=Debt.DebtType.BORROW.value
    ).count()

    context = {
        "month": calendar.month_name[date.today().month - 1],
        "currency": user.currency,
        "income": income.get("total") or 0,
        "spent": total_expenses.get("amount") or 0,
        "unpaid_lent_debts": unpaid_lent_debts,
        "unpaid_borrowed_debts": unpaid_borrowed_debts,
        "total_by_categories": total_by_categories,
        "expenses_by_days": expenses_by_days,
    }
    message = get_template("monthly_report.html").render(context)

    try:
        user.email_user(
            subject="Monthly report", message=message, html_message=message, from_email=settings.EMAIL_HOST_USER
        )
        logger.info("Email sent.")
    except SMTPException as e:
        logger.error(f"Email not sent: {e}")


@shared_task(name="monthly_report")
def monthly_report():
    for user in User.objects.filter(is_active=True, email__isnull=False):
        logger.info(f"User: {user.username}.")
        send_monthly_report(user)

    return True
