import logging
from abc import ABC, abstractmethod
from typing import Dict, Any

logger = logging.getLogger("kavan.apps.monitoring")

class BaseNotificationProvider(ABC):
    """
    Interface for notification channels (Email, Slack, MS Teams, etc.)
    """
    @abstractmethod
    def send(self, subject: str, message: str, severity: str, context: Dict[str, Any] = None) -> bool:
        pass


class EmailProvider(BaseNotificationProvider):
    def send(self, subject: str, message: str, severity: str, context: Dict[str, Any] = None) -> bool:
        # Placeholder for actual email sending logic via Django core mail
        logger.info(f"[Email Notification] [{severity}] {subject} - {message}")
        return True


class WebhookProvider(BaseNotificationProvider):
    def send(self, subject: str, message: str, severity: str, context: Dict[str, Any] = None) -> bool:
        # Placeholder for webhook HTTP post
        logger.info(f"[Webhook Notification] [{severity}] {subject} - {message}")
        return True


class NotificationEngine:
    """
    Manages and dispatches notifications across configured providers.
    """
    def __init__(self):
        # In a real setup, these could be loaded dynamically or configured per-tenant
        self.providers = [
            EmailProvider(),
            WebhookProvider(),
        ]

    def notify(self, subject: str, message: str, severity: str, context: Dict[str, Any] = None):
        """
        Dispatches notification to all registered providers.
        """
        for provider in self.providers:
            try:
                provider.send(subject, message, severity, context or {})
            except Exception as e:
                logger.error(f"Notification Provider {provider.__class__.__name__} failed: {str(e)}")
