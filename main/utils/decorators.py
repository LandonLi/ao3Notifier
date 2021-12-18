import inspect
import logging
from functools import wraps

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

logger = logging.getLogger(__name__)


def required_arguments(text):
    def decorator(func):
        argspec = inspect.getfullargspec(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            if not isinstance(text, str):
                raise ValueError('decorator required_arguments only accept str')
            arguments = text.split(',')
            for argument in arguments:
                try:
                    argument_index = argspec.args.index(argument)
                except ValueError:
                    logger.error(f"'{argument}' is not in <Func: {func.__name__}>'s arguments")
                    return
                try:
                    argument_value = args[argument_index]
                except IndexError:
                    argument_value = kwargs.get(text)
                if argument_value is None:
                    logger.error(f'<Func: {func.__name__}>: {argument} is None!')
                    return

            return func(*args, **kwargs)

        return wrapper

    return decorator
