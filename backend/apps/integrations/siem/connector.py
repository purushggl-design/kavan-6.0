import logging
from django.utils import timezone
from datetime import timedelta
from apps.monitoring.models.events import Event
from apps.integrations.models.siem import SIEMIntegrationConfig, SIEMRetryQueue
from .providers.splunk import SplunkHECProvider

logger = logging.getLogger("kavan.integrations")

class SIEMConnector:
    """
    Master Dispatcher for external SIEM platforms.
    Guarantees reliable delivery with a Retry Queue.
    """
    
    @classmethod
    def get_active_providers(cls):
        providers = []
        configs = SIEMIntegrationConfig.objects.filter(is_active=True)
        for config in configs:
            if config.provider == 'SPLUNK_HEC':
                providers.append((config, SplunkHECProvider(config.endpoint_url)))
            # Add other providers here (Sentinel, Wazuh)
        return providers

    @classmethod
    def forward_event(cls, event: Event, risk_score: int = None):
        """
        Normalizes and forwards a KAVAN Event to all active external SIEMs.
        """
        active_providers = cls.get_active_providers()
        if not active_providers:
            return
            
        for config, provider in active_providers:
            # We can filter by severity here before parsing
            # (assuming simple string comparison is insufficient, we'd map INFO<LOW<MEDIUM<HIGH<CRITICAL)
            
            try:
                # 1. Normalize Event (CIM mapping, MITRE injection)
                payload = provider.normalize_event(event)
                
                # Optional: Inject Correlation Risk Score
                if risk_score is not None:
                    payload['risk_score'] = risk_score
                
                # 2. Forward Event
                provider.forward(payload)
                
            except Exception as e:
                logger.error(f"External SIEM Delivery failed for {config.provider}: {str(e)}")
                # 3. Add to Retry Queue for reliable delivery
                fallback_payload = provider.normalize_event(event)
                SIEMRetryQueue.objects.create(
                    provider=config.provider,
                    payload=fallback_payload,
                    last_error=str(e),
                    next_retry_at=timezone.now() + timedelta(minutes=1)
                )

    @classmethod
    def process_retry_queue(cls):
        """
        Executed by Celery Beat to flush the retry queue.
        """
        now = timezone.now()
        items = SIEMRetryQueue.objects.filter(next_retry_at__lte=now)
        
        for item in items:
            # Instantiating the provider dynamically based on the queue entry
            # In a full system, we would query SIEMIntegrationConfig for the URL
            config = SIEMIntegrationConfig.objects.filter(provider=item.provider, is_active=True).first()
            if not config:
                continue
                
            if item.provider == 'SPLUNK_HEC':
                provider = SplunkHECProvider(config.endpoint_url)
            else:
                continue
                
            try:
                provider.forward(item.payload)
                item.delete() # Success, remove from queue
                logger.info(f"Successfully retried event for {item.provider}")
            except Exception as e:
                item.retry_count += 1
                item.last_error = str(e)
                # Exponential backoff
                item.next_retry_at = now + timedelta(minutes=(2 ** item.retry_count))
                item.save(update_fields=['retry_count', 'last_error', 'next_retry_at'])
                logger.error(f"Retry failed for {item.provider}. Attempt {item.retry_count}")
