import datetime
from datetime import timedelta
from smtplib import SMTPException
from typing import Optional

from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings

from ..users.models import User
from .models import DebtType

logger = get_task_logger(__name__)


@shared_task(name="remind_deadline")
def remind_deadline(days: int) -> Optional[bool]:
    users = User.objects.filter(is_active=True, email__isnull=False)

    for user in users:
        logger.info(f"User: {user.username}.")
        deadline = datetime.date.today() + timedelta(days=days)

        if debts := user.debt_set.filter(deadline=deadline, is_paid=False, type=DebtType.BORROW):
            message = (
                f'Hello, you have {debts.count()} {"debt" if debts.count() == 1 else "debts"} to pay '
                f"where deadline is {deadline}."
            )

            try:
                user.email_user(subject="Deadline reminder.", message=message, from_email=settings.EMAIL_HOST_USER)
                logger.info("Email sent.")
            except SMTPException as e:
                logger.error(f"Email not sent: {e}")
                return False
        else:
            logger.info("No debts for this user.")

    return True
