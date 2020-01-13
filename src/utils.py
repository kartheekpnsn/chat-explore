"""
    Copyright: https://github.com/luka1199/geo-heatmap/blob/master/utils.py
"""

import webbrowser

TEXT_BASED_BROWSERS = [webbrowser.GenericBrowser, webbrowser.Elinks]


def isTextBasedBrowser(browser):
    """Returns if browser is a text-based browser.
    Arguments:
        browser {webbrowser.BaseBrowser} -- A browser.
    Returns:
        bool -- True if browser is text-based, False if browser is not
            text-based.
    """
    for tb_browser in TEXT_BASED_BROWSERS:
        if type(browser) is tb_browser:
            return True
    return False
