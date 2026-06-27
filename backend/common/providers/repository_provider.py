"""
KAVAN v6.0 — Repository Provider
============================================================
Dynamically resolves or creates concrete repositories for Django models.
"""

from typing import Type
from django.db import models
from common.container.container import container
from common.repositories.base_repository import BaseRepository
from common.interfaces.repository import IRepository

class RepositoryProvider:
    """
    Provides repository resolution and caching using the IoC container.
    """

    @staticmethod
    def get_repository(model_class: Type[models.Model]) -> IRepository:
        """
        Resolves the repository instance for a given Django model class.
        If no custom repository exists in the container, it dynamically instantiates one.
        """
        container_key = f"repository_{model_class.__name__.lower()}"
        
        try:
            # Attempt to resolve from IoC container
            return container.resolve(container_key)
        except ValueError:
            # Dynamically build a repository class
            dynamic_repo_class = type(
                f"Dynamic{model_class.__name__}Repository",
                (BaseRepository,),
                {"model": model_class}
            )
            
            # Register in container as a singleton factory
            container.register(
                key=container_key,
                factory=lambda c: dynamic_repo_class(),
                is_singleton=True
            )
            
            return container.resolve(container_key)
