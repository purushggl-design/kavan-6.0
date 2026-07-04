from abc import ABC, abstractmethod

class ProvisionProvider(ABC):
    @abstractmethod
    def provision_infrastructure(self, deployment):
        pass

    @abstractmethod
    def rollback_infrastructure(self, deployment):
        pass

    @abstractmethod
    def restart_infrastructure(self, deployment):
        pass

    @abstractmethod
    def health_check(self, deployment):
        pass
