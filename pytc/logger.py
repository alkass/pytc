from sys import stdout

class ColorfulText:
    class Colors:
        BLACK = "\033[0;30m"
        BLUE = "\033[0;34m"
        GREEN = "\033[0;32m"
        CYAN = "\033[0;36m"
        LIGHT_CYAN = "\033[1;36m"
        RED = "\033[0;31m"
        LIGHT_RED = "\033[1;31m"
        PURPLE = "\033[0;35m"
        LIGHT_PURPLE = "\033[1;35m"
        BROWN = "\033[0;33m"
        GRAY = "\033[0;37m"
        DARK_GRAY = "\033[1;30m"
        LIGHT_GRAY = "\033[1;34m"
        LIGHT_GREEN = "\033[1;32m"
        YELLOW = "\033[1;33m"
        WHITE = "\033[1;37m"
        END = "\033[0;00m"

    class TextStyle:
        BOLD = "\033[1m"
        END = "\033[0m"
    def success(self, message):
        return "%s%sPASS%s: %s%s" % (self.Colors.GREEN, self.TextStyle.BOLD, self.TextStyle.END, message, self.Colors.END)
    def info(self, message):
        return "%s%sINFO%s: %s%s" % (self.Colors.BLUE, self.TextStyle.BOLD, self.TextStyle.END, message, self.Colors.END)
    def warning(self, message):
        return "%s%sWARN%s: %s%s" % (self.Colors.YELLOW, self.TextStyle.BOLD, self.TextStyle.END, message, self.Colors.END)
    def fail(self, message):
        return "%s%sFAIL%s: %s%s" % (self.Colors.RED, self.TextStyle.BOLD, self.TextStyle.END, message, self.Colors.END)


class ColorfulOutputLogger:
    c_text = ColorfulText()
    output_redirector = stdout
    debug_level = 0
    padding_str, trailing_str = "", ""
    num_successes, num_infos, num_warnings, num_fails = 0, 0, 0, 0
    def __init__(self, output=stdout, debug_level=0):
        self.output_redirector = output
        self.debug_level = debug_level
    def header(self):
        from getpass import getuser as username
        from time import gmtime, strftime
        tt = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        return "%s%s %s %s%s%s" % (ColorfulText.Colors.LIGHT_RED, tt, ColorfulText.Colors.END, ColorfulText.Colors.PURPLE, username(), ColorfulText.Colors.END)
    def log(self, message, debug_level, func):
        if debug_level <= self.debug_level:
            out_str = "%s%s  %s%s\n" % (self.padding_str, self.header(), func(message), self.trailing_str)
            self.output_redirector.write(out_str)
    def success(self, message, debug_level):
        self.num_successes += 1
        self.log(message, debug_level, self.c_text.success)
    def info(self, message, debug_level):
        self.num_infos += 1
        self.log(message, debug_level, self.c_text.info)
    def warning(self, message, debug_level):
        self.num_warnings += 1
        self.log(message, debug_level, self.c_text.warning)
    def fail(self, message, debug_level):
        self.num_fails += 1
        self.log(message, debug_level, self.c_text.fail)
    def __del__(self):
        self.output_redirector.write("\nPASS(%d)  FAIL(%d)  WARN(%d)  INFO(%d)" % (self.num_successes, self.num_fails, self.num_warnings, self.num_infos))
        self.output_redirector.write("\n")
