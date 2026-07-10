import logging
from apps.monitoring.models.events import Event
from .detection import DetectionEngine
from .correlation import CorrelationEngine

logger = logging.getLogger("kavan.apps.siem")

class SIEMEngine:
    """
    Master entry point for SIEM processing.
    Receives events from the Event Bus and routes them.
    """
    
    @classmethod
    def analyze(cls, event: Event):
        """
        Main analysis pipeline.
        1. Run Detection Rules
        2. Run Correlation Rules
        """
        logger.debug(f"SIEM Engine analyzing event {event.id} ({event.event_type})")
        
        # 1. Single Event Detection
        DetectionEngine.evaluate(event)
        
        # 2. Multi-Event Correlation
        CorrelationEngine.evaluate(event)
        
        # 3. External SIEM Forwarding
        try:
            from apps.integrations.siem.connector import SIEMConnector
            SIEMConnector.forward_event(event)
        except Exception as e:
            logger.error(f"Failed to forward event to external SIEMs: {str(e)}")
