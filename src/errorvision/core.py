import sys
import threading
import traceback
import os
import difflib
import urllib.parse
import re
import ast
import tokenize
import io

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.syntax import Syntax
    from rich.text import Text
    from rich import box
    from rich.style import Style
    from rich.padding import Padding
except ImportError:
    print("❌ Error Vision requires 'rich'. Please run: pip install rich")
    sys.exit(1)


class BeginnerErrorVision:
    
    SIMPLE_ERRORS = {
        "NameError": "Variable Not Found",
        "TypeError": "Wrong Data Type",
        "SyntaxError": "Writing Mistake",
        "IndentationError": "Spacing Problem",
        "IndexError": "List Index Error",
        "KeyError": "Dictionary Key Missing",
        "FileNotFoundError": "File Not Found",
        "ZeroDivisionError": "Cannot Divide by Zero",
        "ModuleNotFoundError": "Package Not Installed",
        "AttributeError": "Attribute Missing",
        "ValueError": "Wrong Value",
    }

    def __init__(self):
        self.console = Console(stderr=True, force_terminal=True)

    def _detect_syntax_issue(self, line_text, exc_value):
        if not line_text:
            return None
            
        line = line_text.strip()
        error_msg = str(exc_value).lower()
        
        colon_keywords = ["if ", "elif ", "else:", "else ", "for ", "while ", "def ", "class ", "try:", "except", "finally", "with "]
        for keyword in colon_keywords:
            if keyword in line:
                if not line.rstrip().endswith(":") and ":" not in line[-15:]:
                    return "Add a colon : at the end of this line"
        
        if any(kw in line for kw in ["if ", "elif ", "while "]):
            if "==" not in line and re.search(r'[^=<>!]=(?!=)', line):
                return "Use == to compare (not =)"
        
        if line.count("(") > line.count(")"):
            return "Add a closing parenthesis )"
        if line.count("[") > line.count("]"):
            return "Add a closing bracket ]"
        if line.count("{") > line.count("}"):
            return "Add a closing brace }"
        
        single_quotes = len(re.findall(r"(?<!\\)'", line))
        double_quotes = len(re.findall(r'(?<!\\)"', line))
        
        if single_quotes % 2 != 0:
            return "Add a closing single quote '"
        if double_quotes % 2 != 0:
            return 'Add a closing double quote "'
        
        if "invalid syntax" in error_msg or "invalid character" in error_msg:
            if "print " in line and not re.search(r'print\s*\(', line):
                return "In Python 3, use print() as a function with parentheses"
        
        if "expected" in error_msg:
            if "expected ':'" in error_msg:
                return "Add a colon : at the end of this line"
            if "expected ')'" in error_msg:
                return "Add a closing parenthesis )"
        
        return None

    def _get_simple_fix(self, exc_type, exc_value, frame, line_text):
        line = line_text.strip() if line_text else ""
        error_msg = str(exc_value)

        if issubclass(exc_type, NameError):
            try:
                wrong_name = error_msg.split("'")[1]
                if frame:
                    all_vars = list(frame.f_locals.keys()) + list(frame.f_globals.keys())
                    all_vars = [v for v in all_vars if not v.startswith("__")]
                    similar = difflib.get_close_matches(wrong_name, all_vars, n=1, cutoff=0.6)
                    
                    if similar:
                        return f"Change '{wrong_name}' to '{similar[0]}'"
            except:
                pass
            return "Make sure you wrote the variable name correctly"

        if issubclass(exc_type, SyntaxError):
            detected = self._detect_syntax_issue(line, exc_value)
            if detected:
                return detected
            return "Check for missing : or () or quotes"

        if issubclass(exc_type, IndentationError):
            if "expected an indented block" in error_msg:
                return "Press TAB or add 4 spaces before this line"
            if "unindent does not match" in error_msg:
                return "Fix the spacing - this line doesn't match the indentation above"
            return "Fix the spacing - make sure lines are aligned properly"

        if issubclass(exc_type, TypeError):
            if "can only concatenate str" in error_msg:
                return "Convert number to text using str() before adding"
            if "unsupported operand type" in error_msg:
                return "These data types can't be used together in this operation"
            return "Make sure you're using the right data types together"

        if issubclass(exc_type, IndexError):
            return "This position doesn't exist in your list"

        if issubclass(exc_type, KeyError):
            try:
                key = error_msg.split("'")[1]
                return f"Key '{key}' doesn't exist in your dictionary"
            except:
                return "This key doesn't exist in your dictionary"

        if issubclass(exc_type, ZeroDivisionError):
            return "Cannot divide by zero - check your math"

        if issubclass(exc_type, ModuleNotFoundError):
            try:
                module = error_msg.split("'")[1]
                return f"Install it by typing: pip install {module}"
            except:
                return "Install the missing package using pip install"

        if issubclass(exc_type, ValueError):
            if "invalid literal" in error_msg:
                return "The value can't be converted - check the data format"
            return "The value is not valid for this operation"

        if issubclass(exc_type, AttributeError):
            return "This object doesn't have that attribute or method"

        return "Read the error message and check your code"

    def handler(self, exc_type, exc_value, tb):
        error_name = exc_type.__name__
        simple_name = self.SIMPLE_ERRORS.get(error_name, error_name)
        
        filename = "your file"
        lineno = 0
        line_code = ""
        full_path = ""
        
        if issubclass(exc_type, SyntaxError):
            full_path = exc_value.filename
            filename = os.path.basename(full_path) if full_path else "your file"
            lineno = exc_value.lineno or 0
            line_code = exc_value.text.strip() if exc_value.text else ""
        else:
            stack = traceback.extract_tb(tb)
            if stack:
                loc = stack[-1]
                full_path = loc.filename
                filename = os.path.basename(full_path)
                lineno = loc.lineno
                line_code = loc.line or ""

        curr_tb = tb
        while curr_tb and curr_tb.tb_next:
            curr_tb = curr_tb.tb_next
        frame = curr_tb.tb_frame if curr_tb else None
        
        fix = self._get_simple_fix(exc_type, exc_value, frame, line_code)

        self.console.print("\n")
        
        title = Text()
        title.append(f"  ⚠️  {simple_name}  ", style="bold white on red")
        self.console.print(title)
        
        location = Text()
        location.append(f"\n📍 In file: ", style="bold cyan")
        location.append(f"{filename}", style="yellow")
        location.append(f"  →  Line {lineno}\n", style="bold yellow")
        self.console.print(location)

        if full_path and os.path.exists(full_path):
            try:
                self.console.print("─" * 60, style="dim")
                
                error_style = Style(bold=True, bgcolor="rgb(80,20,20)")
                
                code_view = Syntax.from_path(
                    full_path,
                    line_numbers=True,
                    start_line=max(1, lineno - 1),
                    line_range=(max(1, lineno - 1), lineno + 1),
                    highlight_lines={lineno},
                    theme="monokai",
                    background_color="default"
                )
                
                code_view.highlight_lines_style = error_style
                self.console.print(code_view)
                self.console.print("─" * 60, style="dim")
            except:
                pass

        self.console.print(f"\n💬 Error message: ", style="bold white", end="")
        self.console.print(f"{str(exc_value)}", style="yellow")

        self.console.print()
        fix_box = Panel(
            Text(f"✅  {fix}", style="bold white", justify="left"),
            title="[bold green]HOW TO FIX[/bold green]",
            title_align="left",
            border_style="bold green",
            box=box.HEAVY,
            padding=(1, 2)
        )
        self.console.print(fix_box)

        search_url = urllib.parse.quote(f"python {error_name} beginner")
        self.console.print(
            f"\n💡 Need more help? [link=https://www.google.com/search?q={search_url}]"
            f"[cyan underline]Click here to search for solutions[/cyan underline][/link]\n",
            style="dim"
        )


_vision = BeginnerErrorVision()


def enable():
    sys.excepthook = _vision.handler
    
    def thread_handler(args):
        _vision.handler(args.exc_type, args.exc_value, args.exc_traceback)
    
    threading.excepthook = thread_handler


enable()