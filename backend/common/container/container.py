"""
KAVAN v6.0 — Service Container
============================================================
Lightweight Inversion of Control (IoC) Container for dependency injection.
"""

from typing import Dict, Any, Callable, Type, TypeVar, Union

T = TypeVar("T")

class ServiceContainer:
    """
    IoC Container managing registration and lifecycle (singleton vs factory)
    of repositories, services, and utilities.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ServiceContainer, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._registry: Dict[Any, Callable[..., Any]] = {}
        self._singletons: Dict[Any, Any] = {}
        self._is_singleton_map: Dict[Any, bool] = {}

    def register(
        self,
        key: Any,
        factory: Callable[..., Any],
        is_singleton: bool = False,
    ) -> None:
        """
        Registers a dependency factory in the container.
        """
        self._registry[key] = factory
        self._is_singleton_map[key] = is_singleton
        if key in self._singletons:
            del self._singletons[key]

    def register_singleton(self, key: Any, instance: Any) -> None:
        """
        Registers a pre-instantiated singleton object.
        """
        self._singletons[key] = instance
        self._is_singleton_map[key] = True

    def resolve(self, key: Type[T]) -> T:
        """
        Resolves and returns a registered dependency.
        """
        # If it has already been instantiated as a singleton, return it
        if key in self._singletons:
            return self._singletons[key]

        if key not in self._registry:
            # Fallback: if key is a class, try to instantiate it directly
            if isinstance(key, type):
                try:
                    return key()
                except TypeError:
                    raise ValueError(f"Dependency '{key}' is not registered and cannot be instantiated automatically.")
            raise ValueError(f"Dependency '{key}' is not registered in the container.")

        factory = self._registry[key]
        
        # Instantiate the dependency
        try:
            # Try passing container context to factory
            instance = factory(self)
        except TypeError:
            # Fall back to zero-argument call
            instance = factory()

        # Cache if marked as singleton
        if self._is_singleton_map.get(key, False):
            self._singletons[key] = instance

        return instance

    def clear(self) -> None:
        """
        Wipes container state. Used mainly during test isolation.
        """
        self._registry.clear()
        self._singletons.clear()
        self._is_singleton_map.clear()

# Global IoC container instance
container = ServiceContainer()
