from coalib.output.printers.NullPrinter import NullPrinter
from coalib.misc.Constants import Constants
from coalib.misc.i18n import _


def get_exitcode(exception, log_printer=None):
    log_printer = log_printer or NullPrinter()
    exitcode = 0
    if isinstance(exception, KeyboardInterrupt):  # Ctrl+C
        print(_("Program terminated by user."))
        exitcode = 130
    elif isinstance(exception, EOFError):  # Ctrl+D
        print(_("Found EOF. Exiting gracefully."))
    elif isinstance(exception, SystemExit):
        exitcode = exception.code
    elif isinstance(exception, Exception):
        log_printer.log_exception(Constants.CRASH_MESSAGE, exception)
        exitcode = 255

    return exitcode

