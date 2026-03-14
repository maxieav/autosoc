from __future__ import annotations
import logging
import smtplib
from email.mime.text import MIMEText
from src.infrastructure.connectors.base import BaseCommunicationChannel

logger = logging.getLogger(__name__)


class EmailChannel(BaseCommunicationChannel):
    def __init__(self, config: dict[str, str]) -> None:
        self._config = config

    async def send_notification(
        self,
        recipient: str,
        subject: str,
        body: str,
        thread_id: str | None = None,
    ) -> str:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = self._config.get("from_address", "autosoc@localhost")
        msg["To"] = recipient
        if thread_id:
            msg["In-Reply-To"] = thread_id
            msg["References"] = thread_id

        smtp_host = self._config.get("smtp_host", "localhost")
        smtp_port = int(self._config.get("smtp_port", "25"))
        try:
            with smtplib.SMTP(smtp_host, smtp_port) as smtp:
                smtp.sendmail(msg["From"], [recipient], msg.as_string())
        except Exception:
            logger.exception("Failed to send email to %s via %s:%s", recipient, smtp_host, smtp_port)
        return msg["Message-ID"] or ""
