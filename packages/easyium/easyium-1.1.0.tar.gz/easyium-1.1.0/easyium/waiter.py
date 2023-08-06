import time

from .exceptions import TimeoutException
from .config import DEFAULT, waiter_default_wait_interval, waiter_default_wait_timeout

__author__ = 'karl.gong'


class Waiter:
    def __init__(self, interval=DEFAULT, timeout=DEFAULT):
        """
            Create a Waiter instance.

        :param interval: the wait interval (in milliseconds), default value is from config.waiter_default_wait_interval
        :param timeout: the wait timeout (in milliseconds), default value is from config.waiter_default_wait_timeout
        """
        self.__interval = waiter_default_wait_interval if interval == DEFAULT else interval
        self.__timeout = waiter_default_wait_timeout if timeout == DEFAULT else timeout

    def wait_for(self, condition_function, *function_args, **function_kwargs):
        """
            Wait for the condition.

        :param condition_function: the condition function
        :param function_args: the args for condition_function
        :param function_kwargs: the kwargs for condition_function
        """
        start_time = time.time() * 1000.0

        if condition_function(*function_args, **function_kwargs):
            return

        while (time.time() * 1000.0 - start_time) <= self.__timeout:
            if condition_function(*function_args, **function_kwargs):
                return
            else:
                time.sleep(self.__interval / 1000.0)

        raise TimeoutException("Timed out waiting for <%s>." % condition_function.__name__)


class ContextWaiter(Waiter):
    def __init__(self, context, interval, timeout):
        Waiter.__init__(self, interval, timeout)
        self.__context = context

    def wait_for(self, condition_function, *function_args, **function_kwargs):
        """
            Wait for the condition.
            The context will be passed to to condition_function as first argument.

        :param condition_function: the condition function which accepts context as first argument
        :param function_args: the args for condition_function (except context)
        :param function_kwargs: the kwargs for condition_function (except context)
        """
        Waiter.wait_for(self, condition_function, self.__context, *function_args, **function_kwargs)


class ElementWaitFor:
    def __init__(self, element, interval, timeout):
        self.__element = element
        self.__desired_occurrence = True
        self.__waiter = Waiter(interval, timeout)

    def __wait_for(self, element_condition):
        def is_element_condition_occurred():
            return element_condition.occurred() == self.__desired_occurrence

        try:
            self.__waiter.wait_for(is_element_condition_occurred)
        except TimeoutException:
            raise TimeoutException(
                "Timed out waiting for <%s> to be <%s>." % (element_condition, self.__desired_occurrence))

    def not_(self):
        self.__desired_occurrence = not self.__desired_occurrence
        return self

    def exists(self):
        self.__wait_for(ElementExistence(self.__element))

    def visible(self):
        self.__wait_for(ElementVisible(self.__element))

    def attribute_contains_one(self, attribute, *values):
        self.__wait_for(ElementAttributeContainsOne(self.__element, attribute, *values))

    def attribute_contains_all(self, attribute, *values):
        self.__wait_for(ElementAttributeContainsAll(self.__element, attribute, *values))


class ElementExistence:
    def __init__(self, element):
        self.__element = element

    def occurred(self):
        return self.__element.exists()

    def __str__(self):
        return "ElementExistence [\n%s\n]" % self.__element


class ElementVisible:
    def __init__(self, element):
        self.__element = element

    def occurred(self):
        return self.__element.is_displayed()

    def __str__(self):
        return "ElementVisible [\n%s\n]" % self.__element


class ElementAttributeContainsOne:
    def __init__(self, element, attribute, *values):
        self.__element = element
        self.__attribute = attribute
        self.__values = values

    def occurred(self):
        attribute_value = self.__element.get_attribute(self.__attribute)
        for value in self.__values:
            if attribute_value.find(value) != -1:
                return True
        return False

    def __str__(self):
        return "ElementAttributeContainsOne [element: \n%s\n][attribute: %s][values: %s]" % (
            self.__element, self.__attribute, self.__values)


class ElementAttributeContainsAll:
    def __init__(self, element, attribute, *values):
        self.__element = element
        self.__attribute = attribute
        self.__values = values

    def occurred(self):
        attribute_value = self.__element.get_attribute(self.__attribute)
        for value in self.__values:
            if attribute_value.find(value) == -1:
                return False
        return True

    def __str__(self):
        return "ElementAttributeContainsAll [element: \n%s\n][attribute: %s][values: %s]" % (
            self.__element, self.__attribute, self.__values)
