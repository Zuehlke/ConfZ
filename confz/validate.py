from .confz import ConfZ


def _get_sub_classes(cls):
    direct_sub_classes = cls.__subclasses__()

    all_sub_classes = direct_sub_classes.copy()
    for sub_class in direct_sub_classes:
        all_sub_classes.extend(_get_sub_classes(sub_class))

    return all_sub_classes


def validate_all_configs(include_listeners: bool = False):
    """Instantiates all config classes with a singleton mechanism
    (`CONFIG_SOURCES` set). This allows to catch validation errors early instead of
    waiting for the first access.

    :param include_listeners: Whether all listeners (marked with
        :func:`~confz.depends_on`) should be included.
    :raises ConfZException: If any config could not be loaded.
    """
    config_classes = []
    sync_listeners = []
    async_listeners = []
    for config_class in _get_sub_classes(ConfZ):
        if config_class.CONFIG_SOURCES is not None:
            config_classes.append(config_class)
            if include_listeners and config_class.listeners is not None:
                for listener in config_class.listeners:
                    if listener.is_async:
                        async_listeners.append(listener)
                    else:
                        sync_listeners.append(listener)

    def sync_calls():
        for cls in config_classes:
            cls()
        for fn in sync_listeners:
            fn()

    if len(async_listeners) > 0:

        async def inner():
            sync_calls()
            for fn in async_listeners:
                await fn()

    else:
        inner = sync_calls

    return inner()
