import logging
from common.services.base_service import BaseService
from apps.deployments.repositories import (
    DeploymentRepository, DeploymentJobRepository, DeploymentHistoryRepository,
    DeploymentLogRepository
)
from apps.deployments.models import DeploymentState

logger = logging.getLogger(__name__)

class StateMachineService(BaseService):
    VALID_TRANSITIONS = {
        DeploymentState.REQUESTED: [DeploymentState.QUEUED, DeploymentState.FAILED],
        DeploymentState.QUEUED: [DeploymentState.VALIDATING, DeploymentState.FAILED],
        DeploymentState.VALIDATING: [DeploymentState.PROVISIONING, DeploymentState.FAILED],
        DeploymentState.PROVISIONING: [DeploymentState.INSTALLING, DeploymentState.FAILED],
        DeploymentState.INSTALLING: [DeploymentState.CONFIGURING, DeploymentState.FAILED],
        DeploymentState.CONFIGURING: [DeploymentState.STARTING, DeploymentState.FAILED],
        DeploymentState.STARTING: [DeploymentState.HEALTH_CHECK, DeploymentState.FAILED],
        DeploymentState.HEALTH_CHECK: [DeploymentState.RUNNING, DeploymentState.FAILED],
        DeploymentState.RUNNING: [DeploymentState.FAILED, DeploymentState.ROLLBACK],
        DeploymentState.FAILED: [DeploymentState.ROLLBACK],
        DeploymentState.ROLLBACK: [DeploymentState.ROLLED_BACK, DeploymentState.FAILED],
        DeploymentState.ROLLED_BACK: [],
    }

    def transition(self, deployment, new_status, job=None):
        old_status = deployment.status
        if old_status == new_status:
            return
            
        if new_status not in self.VALID_TRANSITIONS.get(old_status, []):
            raise ValueError(f"Invalid transition from {old_status} to {new_status}")
            
        DeploymentRepository.update_status(deployment.id, new_status)
        DeploymentHistoryRepository.create(deployment_id=deployment.id, old_status=old_status, new_status=new_status)
        
        deployment.status = new_status
        
        if job:
            DeploymentJobRepository.update_status(job.id, new_status)
            DeploymentLogRepository.append_log(job.id, f"Transitioned from {old_status} to {new_status}")
            job.status = new_status
            
        self._log_operation("transition", deployment_id=str(deployment.id), old_status=old_status, new_status=new_status)
        
        from apps.monitoring.services.event_bus import EventBusService
        from apps.monitoring.models.events import EventType, EventSeverity
        
        event_type = EventType.SYSTEM_ALERT
        severity = EventSeverity.INFO
        status_event = "success"
        
        if new_status == DeploymentState.QUEUED:
            event_type = EventType.DEPLOYMENT_STARTED
        elif new_status == DeploymentState.FAILED:
            event_type = EventType.DEPLOYMENT_FAILED
            severity = EventSeverity.HIGH
            status_event = "failed"
        elif new_status == DeploymentState.RUNNING:
            event_type = EventType.DEPLOYMENT_SUCCESS
            severity = EventSeverity.INFO
            
        # Only publish significant state changes
        if event_type != EventType.SYSTEM_ALERT:
            EventBusService.publish(
                module="Deployment",
                event_type=event_type,
                action="transition",
                status=status_event,
                severity=severity,
                tenant_id=deployment.tenant.id if deployment.tenant else None,
                resource=str(deployment.id),
                metadata={"old_status": old_status, "new_status": new_status}
            )

class SchedulerService(BaseService):
    def schedule_deployment(self, deployment):
        job = DeploymentJobRepository.create(deployment_id=deployment.id, status=DeploymentState.QUEUED)
        state_machine = StateMachineService()
        state_machine.transition(deployment, DeploymentState.QUEUED, job)
        return job

class DeploymentService(BaseService):
    def __init__(self):
        super().__init__(repository=DeploymentRepository)

    def request_deployment(self, tenant, product, tenant_product, template):
        deployment = self.repository.create(
            tenant=tenant, product=product, tenant_product=tenant_product, template=template, status=DeploymentState.REQUESTED
        )
        return deployment

    def deploy(self, deployment):
        if deployment.status != DeploymentState.REQUESTED:
            raise ValueError(f"Cannot deploy from state {deployment.status}")
            
        scheduler = SchedulerService()
        job = scheduler.schedule_deployment(deployment)
        
        # Trigger Celery Task
        from apps.deployments.tasks import deploy_product_task
        deploy_product_task.delay(deployment.id, job.id)
        
        return job
