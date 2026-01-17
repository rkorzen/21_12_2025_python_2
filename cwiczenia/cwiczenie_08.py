"""

Napisz dekorator, ktory bedzie logowac uzycie funkcji, jej nazwe, argumenty, wynik i czas wykonania

"""
import logging
import sys
import time
from functools import wraps

sys.set_int_max_str_digits(100000)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    filename="log.txt"
)
logger = logging.getLogger(__name__)


def logowanie(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        t1 = time.time()
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            logger.error(
                f"Error in function `{func.__name__}` with args: pozycyjne: {args}, nazwane: {kwargs}. Error: {e}",
                exc_info=True, stack_info=True)
            raise
        log = f"Wywołano funkcję: `{func.__name__}` z parametrami: pozycyjne: {args}, nazwane: {kwargs} wynik: {str(result)[:10]}, czas: {time.time() - t1:.2f}s"
        logger.info(log)
        return result

    return wrapper


@logowanie
def add(a, b):
    return a + b


@logowanie
def bar(n=10):
    return sum(x ** n for x in range(n))


@logowanie
def bad_function():
    1 / 0


add(10, 20)

bar(1000)

bad_function()
