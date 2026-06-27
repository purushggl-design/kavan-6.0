"""
KAVAN v6.0 — Service Provider
============================================================
Resolves concrete services and handles dependency injection of repositories.
"""

import inspect
from typing import Type, Any
from django.db import models
from common.container.container import container
from common.interfaces.service import IService
from common.providers.repository_provider import RepositoryProvider

class ServiceProvider:
    """
    Coordinates service resolution, injecting repositories or other components.
    """

    @staticmethod
    def get_service(service_class: Type[Any]) -> Any:
        """
        Resolves the service instance from the container. If not registered,
        it auto-analyzes the constructor and performs injection.
        """
        try:
            return container.resolve(service_class)
        except ValueError:
            # Dynamic factory mapping using signature analysis
            sig = inspect.signature(service_class.__init__)
            
            def factory(c):
                kwargs = {}
                for param_name, param in sig.parameters.items():
                    if param_name in ("self", "args", "kwargs"):
                        continue
                        
                    annotation = param.annotation
                    
                    # 1. Check if the type annotation is a Django model class
                    if isinstance(annotation, type) and issubclass(annotation, models.Model):
                        kwargs[param_name] = RepositoryProvider.get_repository(annotation)
                    # 2. Check if parameter name hints at a model/repo
                    elif param_name.endswith("_repository") or param_name.endswith("_repo"):
                        # Attempt to guess model by name prefix (e.g. user_repo -> User)
                        model_name = param_name.replace("_repository", "").replace("_repo", "").capitalize()
                        # Search models in django apps registry
                        from django.apps import apps
                        try:
                            # Try to find a matching model name in registered apps
                            found_model = None
                            for config in apps.get_app_configs():
                                if model_name in config.models:
                                    found_model = config.models[model_name]
                                    break
                            if found_model:
                                kwargs[param_name] = RepositoryProvider.get_repository(found_model)
                        except Exception:
                            pass
                return service_class(**kwargs)

            # Register as transient factory
            container.register(service_class, factory, is_singleton=False)
            return container.resolve(service_class)
