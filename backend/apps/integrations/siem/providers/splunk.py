import os
import logging
import requests
from typing import Dict, Any
from apps.monitoring.models.events import Event
from .base import BaseSIEMProvider

logger = logging.getLogger("kavan.integrations")

class SplunkHECProvider(BaseSIEMProvider):
    """
    Splunk HTTP Event Collector (HEC) Provider.
    Maps events to Splunk Common Information Model (CIM) and MITRE ATT&CK.
    """
    
    def __init__(self, endpoint_url: str):
        self.endpoint_url = endpoint_url
        self.hec_token = os.environ.get("SPLUNK_HEC_TOKEN", "")
        if not self.hec_token:
            logger.warning("SPLUNK_HEC_TOKEN environment variable not set.")

    def forward(self, payload: Dict[str, Any]) -> bool:
        if not self.endpoint_url or not self.hec_token:
            return False

        headers = {
            "Authorization": f"Splunk {self.hec_token}",
            "Content-Type": "application/json"
        }
        
        try:
            # Splunk HEC requires the payload wrapped in an 'event' envelope
            hec_payload = {
                "event": payload,
                "sourcetype": "_json",
                "index": f"tenant_{payload.get('tenant_id', 'system')}" if payload.get('tenant_id') else "kavan_system"
            }
            
            # Using timeout to prevent blocking the worker
            response = requests.post(
                self.endpoint_url,
                headers=headers,
                json=hec_payload,
                timeout=5
            )
            response.raise_for_status()
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to forward to Splunk HEC: {str(e)}")
            raise e

    def normalize_event(self, event: Event) -> Dict[str, Any]:
        """
        Normalizes a KAVAN event to Splunk CIM.
        """
        payload = {
            "event_id": str(event.id),
            "tenant_id": str(event.tenant_id) if event.tenant_id else None,
            "user_id": str(event.user_id) if event.user_id else None,
            "app": "kavan_enterprise",
            "module": event.module,
            "severity": event.severity,
            "action": event.action,
            "status": event.status,
            "src_ip": event.metadata.get("ip_address", ""),
            "timestamp": event.created_at.isoformat(),
        }

        # Example MITRE ATT&CK Mapping
        if event.module == "RBAC" and event.event_type == "PRIVILEGE_ESCALATION":
            payload["mitre_tactic"] = "Privilege Escalation"
            payload["mitre_technique"] = "T1078"
            
        return payload
