import functools


def debug(func):
    """Print the function signature and return value"""

    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        try:
            is_callable = func.__call__
        except AttributeError:
            is_callable = None

        if is_callable:
            print(f"Calling {func.__name__}({signature})")  # noqa: T201
            value = func(*args, **kwargs)
            print(f"{func.__name__}() returned {value!r}")  # noqa: T201
            return value

        print(f"Debugged object {func!r} cannot be called")  # noqa: T201
        return func

    return wrapper_debug
