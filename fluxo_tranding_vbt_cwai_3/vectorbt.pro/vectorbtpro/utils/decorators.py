# Copyright (c) 2021-2024 Oleg Polakow. All rights reserved.

"""Class and function decorators."""

from functools import wraps

from vectorbtpro import _typing as tp
from vectorbtpro.utils.base import Base

__all__ = [
    "class_property",
    "hybrid_property",
    "hybrid_method",
    "cacheable_property",
    "cached_property",
    "cacheable",
    "cached",
    "cacheable_method",
    "cached_method",
]

__pdoc__ = {}


# ############# Generic ############# #


class class_property(Base):
    """Property that can be called on a class."""

    def __init__(self, func: tp.Callable) -> None:
        self._func = func
        self.__doc__ = getattr(func, "__doc__")

    @property
    def func(self) -> tp.Callable:
        """Wrapped function."""
        return self._func

    def __get__(self, instance: object, owner: tp.Optional[tp.Type] = None) -> tp.Any:
        return self.func(owner)

    def __set__(self, instance: object, value: tp.Any) -> None:
        raise AttributeError("can't set attribute")


class hybrid_property(Base):
    """Property that binds `self` to a class if the function is called as class method,
    otherwise to an instance."""

    def __init__(self, func: tp.Callable) -> None:
        self._func = func
        self.__doc__ = getattr(func, "__doc__")

    @property
    def func(self) -> tp.Callable:
        """Wrapped function."""
        return self._func

    def __get__(self, instance: object, owner: tp.Optional[tp.Type] = None) -> tp.Any:
        if instance is None:
            return self.func(owner)
        return self.func(instance)

    def __set__(self, instance: object, value: tp.Any) -> None:
        raise AttributeError("can't set attribute")


class hybrid_method(classmethod, Base):
    """Function decorator that binds `self` to a class if the function is called as class method,
    otherwise to an instance."""

    def __get__(self, instance: object, owner: tp.Optional[tp.Type] = None) -> tp.Any:
        descr_get = super().__get__ if instance is None else self.__func__.__get__
        return descr_get(instance, owner)


# ############# Custom properties ############# #

custom_propertyT = tp.TypeVar("custom_propertyT", bound="custom_property")


class custom_property(property, Base):
    """Custom extensible property that stores function and options as attributes.

    !!! note
        `custom_property` instances belong to classes, not class instances. Thus changing the property
        will do the same for each instance of the class where the property has been defined initially."""

    def __new__(cls: tp.Type[custom_propertyT], *args, **options) -> tp.Union[tp.Callable, custom_propertyT]:
        if len(args) == 0:
            return lambda func: cls(func, **options)
        elif len(args) == 1:
            return super().__new__(cls)
        raise ValueError("Either function or keyword arguments must be passed")

    def __init__(self, func: tp.Callable, **options) -> None:
        property.__init__(self)

        self._func = func
        self._name = func.__name__
        self._options = options
        self.__doc__ = getattr(func, "__doc__")

    @property
    def func(self) -> tp.Callable:
        """Wrapped function."""
        return self._func

    @property
    def name(self) -> str:
        """Wrapped function name."""
        return self._name

    @property
    def options(self) -> tp.Kwargs:
        """Options."""
        return self._options

    def __set_name__(self, owner: tp.Type, name: str) -> None:
        self._name = name

    def __get__(self, instance: object, owner: tp.Optional[tp.Type] = None) -> tp.Any:
        if instance is None:
            return self
        return self.func(instance)

    def __set__(self, instance: object, value: tp.Any) -> None:
        raise AttributeError("Can't set attribute")

    def __call__(self, *args, **kwargs) -> tp.Any:
        pass


class cacheable_property(custom_property):
    """Extends `custom_property` for cacheable properties.

    !!! note
        Assumes that the instance (provided as `self`) won't change. If calculation depends
        upon object attributes that can be changed, it won't notice the change."""

    def __init__(self, func: tp.Callable, use_cache: bool = False, whitelist: bool = False, **options) -> None:
        from vectorbtpro._settings import settings

        caching_cfg = settings["caching"]

        super().__init__(func, **options)

        self._init_use_cache = use_cache
        self._init_whitelist = whitelist
        if not caching_cfg["register_lazily"]:
            self.get_ca_setup()

    @property
    def init_use_cache(self) -> bool:
        """Initial value for `use_cache`."""
        return self._init_use_cache

    @property
    def init_whitelist(self) -> bool:
        """Initial value for `whitelist`."""
        return self._init_whitelist

    def get_ca_setup(self, instance: tp.Optional[object] = None) -> tp.Optional["CARunSetup"]:
        """Get setup of type `vectorbtpro.registries.ca_registry.CARunSetup` if instance is known,
        or `vectorbtpro.registries.ca_registry.CAUnboundSetup` otherwise.

        See `vectorbtpro.registries.ca_registry` for details on the caching procedure."""
        from vectorbtpro.registries.ca_registry import CAUnboundSetup, CARunSetup

        unbound_setup = CAUnboundSetup.get(self, use_cache=self.init_use_cache, whitelist=self.init_whitelist)
        if instance is None:
            return unbound_setup
        return CARunSetup.get(self, instance=instance)

    def __get__(self, instance: object, owner: tp.Optional[tp.Type] = None) -> tp.Any:
        if instance is None:
            return self
        run_setup = self.get_ca_setup(instance)
        if run_setup is None:
            return self.func(instance)
        return run_setup.run()


class cached_property(cacheable_property):
    """`cacheable_property` with `use_cache` set to True."""

    def __init__(self, func: tp.Callable, **options) -> None:
        cacheable_property.__init__(self, func, use_cache=True, **options)


# ############# Custom functions ############# #


class custom_functionT(tp.Protocol):
    decorator_name: str
    func: tp.Callable
    name: str
    options: tp.Kwargs
    is_method: bool
    is_custom: bool

    def __call__(*args, **kwargs) -> tp.Any:
        pass


__pdoc__["custom_functionT"] = False


def custom_function(
    *args,
    _decorator_name: tp.Optional[str] = None,
    **options,
) -> tp.Union[tp.Callable, custom_functionT]:
    """Custom function decorator."""

    def decorator(func: tp.Callable) -> custom_functionT:
        @wraps(func)
        def wrapper(*args, **kwargs) -> tp.Any:
            return func(*args, **kwargs)

        wrapper.decorator_name = "custom_function" if _decorator_name is None else _decorator_name
        wrapper.func = func
        wrapper.name = func.__name__
        wrapper.options = options
        wrapper.is_method = False
        wrapper.is_custom = True

        return wrapper

    if len(args) == 0:
        return decorator
    elif len(args) == 1:
        return decorator(args[0])
    raise ValueError("Either function or keyword arguments must be passed")


class cacheable_functionT(custom_functionT):
    is_cacheable: bool
    get_ca_setup: tp.Callable[[], tp.Optional["CARunSetup"]]


__pdoc__["cacheable_functionT"] = False


def cacheable(
    *args,
    use_cache: bool = False,
    whitelist: bool = False,
    max_size: tp.Optional[int] = None,
    ignore_args: tp.Optional[tp.Iterable[tp.AnnArgQuery]] = None,
    _decorator_name: tp.Optional[str] = None,
    **options,
) -> tp.Union[tp.Callable, cacheable_functionT]:
    """Cacheable function decorator.

    See notes on `cacheable_property`.

    !!! note
        To decorate an instance method, use `cacheable_method`."""

    def decorator(func: tp.Callable) -> cacheable_functionT:
        from vectorbtpro.registries.ca_registry import CARunSetup
        from vectorbtpro._settings import settings

        caching_cfg = settings["caching"]

        @wraps(func)
        def wrapper(*args, **kwargs) -> tp.Any:
            run_setup = wrapper.get_ca_setup()
            if run_setup is None:
                return func(*args, **kwargs)
            return run_setup.run(*args, **kwargs)

        def get_ca_setup() -> tp.Optional[CARunSetup]:
            """Get setup of type `vectorbtpro.registries.ca_registry.CARunSetup`.

            See `vectorbtpro.registries.ca_registry` for details on the caching procedure."""
            return CARunSetup.get(
                wrapper,
                use_cache=use_cache,
                whitelist=whitelist,
                max_size=max_size,
                ignore_args=ignore_args,
            )

        wrapper.decorator_name = "cacheable" if _decorator_name is None else _decorator_name
        wrapper.func = func
        wrapper.name = func.__name__
        wrapper.options = options
        wrapper.is_method = False
        wrapper.is_custom = True
        wrapper.is_cacheable = True
        wrapper.get_ca_setup = get_ca_setup
        if not caching_cfg["register_lazily"]:
            wrapper.get_ca_setup()

        return wrapper

    if len(args) == 0:
        return decorator
    elif len(args) == 1:
        return decorator(args[0])
    raise ValueError("Either function or keyword arguments must be passed")


def cached(*args, **options) -> tp.Union[tp.Callable, cacheable_functionT]:
    """`cacheable` with `use_cache` set to True.

    !!! note
        To decorate an instance method, use `cached_method`."""
    return cacheable(*args, use_cache=True, _decorator_name="cached", **options)


# ############# Custom methods ############# #


class custom_methodT(custom_functionT):
    def __call__(instance: object, *args, **kwargs) -> tp.Any:
        pass


__pdoc__["custom_methodT"] = False


def custom_method(
    *args,
    _decorator_name: tp.Optional[str] = None,
    **options,
) -> tp.Union[tp.Callable, custom_methodT]:
    """Custom method decorator."""

    def decorator(func: tp.Callable) -> custom_methodT:
        @wraps(func)
        def wrapper(instance: object, *args, **kwargs) -> tp.Any:
            return func(instance, *args, **kwargs)

        wrapper.decorator_name = "custom_method" if _decorator_name is None else _decorator_name
        wrapper.func = func
        wrapper.name = func.__name__
        wrapper.options = options
        wrapper.is_method = True
        wrapper.is_custom = True

        return wrapper

    if len(args) == 0:
        return decorator
    elif len(args) == 1:
        return decorator(args[0])
    raise ValueError("Either function or keyword arguments must be passed")


class cacheable_methodT(custom_methodT):
    get_ca_setup: tp.Callable[[tp.Optional[object]], tp.Optional["CARunSetup"]]


__pdoc__["cacheable_methodT"] = False


def cacheable_method(
    *args,
    use_cache: bool = False,
    whitelist: bool = False,
    max_size: tp.Optional[int] = None,
    ignore_args: tp.Optional[tp.Iterable[tp.AnnArgQuery]] = None,
    _decorator_name: tp.Optional[str] = None,
    **options,
) -> tp.Union[tp.Callable, cacheable_methodT]:
    """Cacheable method decorator.

    See notes on `cacheable_property`."""

    def decorator(func: tp.Callable) -> cacheable_methodT:
        from vectorbtpro.registries.ca_registry import CAUnboundSetup, CARunSetup
        from vectorbtpro._settings import settings

        caching_cfg = settings["caching"]

        @wraps(func)
        def wrapper(instance: object, *args, **kwargs) -> tp.Any:
            run_setup = wrapper.get_ca_setup(instance)
            if run_setup is None:
                return func(instance, *args, **kwargs)
            return run_setup.run(*args, **kwargs)

        def get_ca_setup(instance: tp.Optional[object] = None) -> tp.Optional[CARunSetup]:
            """Get setup of type `vectorbtpro.registries.ca_registry.CARunSetup` if instance is known,
            or `vectorbtpro.registries.ca_registry.CAUnboundSetup` otherwise.

            See `vectorbtpro.registries.ca_registry` for details on the caching procedure."""
            unbound_setup = CAUnboundSetup.get(wrapper, use_cache=use_cache, whitelist=whitelist)
            if instance is None:
                return unbound_setup
            return CARunSetup.get(wrapper, instance=instance, max_size=max_size, ignore_args=ignore_args)

        wrapper.decorator_name = "cacheable_method" if _decorator_name is None else _decorator_name
        wrapper.func = func
        wrapper.name = func.__name__
        wrapper.options = options
        wrapper.is_method = True
        wrapper.is_custom = True
        wrapper.is_cacheable = True
        wrapper.get_ca_setup = get_ca_setup
        if not caching_cfg["register_lazily"]:
            wrapper.get_ca_setup()

        return wrapper

    if len(args) == 0:
        return decorator
    elif len(args) == 1:
        return decorator(args[0])
    raise ValueError("Either function or keyword arguments must be passed")


def cached_method(*args, **options) -> tp.Union[tp.Callable, cacheable_methodT]:
    """`cacheable_method` with `use_cache` set to True."""
    return cacheable_method(*args, use_cache=True, _decorator_name="cached_method", **options)


cacheableT = tp.Union[cacheable_property, cacheable_functionT, cacheable_methodT]
