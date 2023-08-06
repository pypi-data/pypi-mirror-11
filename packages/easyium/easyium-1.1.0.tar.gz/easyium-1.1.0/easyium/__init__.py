try:
    import appium
    appium_installed = True
except ImportError:
    appium_installed = False

from .webdriver import WebDriver, WebDriverType
from .staticelement import StaticElement
from .identifier import Identifier
from .waiter import Waiter

__author__ = 'karl.gong'
