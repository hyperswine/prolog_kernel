from functools import reduce
from ipykernel.kernelbase import Kernel
from pyswip import Prolog, Variable

usage = """\
Rules:
    child(stephanie).
    child(thad).
    ...

Queries:
    child(NAME)?
    sibling(sally, erica)?
    father_child(Father, Child)?
"""


class PrologKernel(Kernel):
    implementation = 'Prolog'
    implementation_version = '1.0'
    language = 'prolog'
    language_version = '0.1'
    banner = "Prolog kernel - it just works"
    language_info = {
        'mimetype': 'text/x-prolog',
        'name': 'prolog',
        'file_extension': '.pl',
        'pygments_lexer': 'prolog',
    }

    def __init__(self, **kwargs):
        self.prolog = Prolog()
        Kernel.__init__(self, **kwargs)

    def print(self, msg):
        pass

    def error(self, msg):
        pass

    def get_usage(self):
        return usage

    def process_prolog(self, code: str):
        match code:
            case code if code.endswith("?"): return self.handle_query(code)
            case _: return self.handle_assertion(code)

    def handle_query(self, code):
        query_str = code[:-1]  # Remove the '?' at the end
        solutions = []

        try:
            for sol in self.prolog.query(query_str):
                solutions.append(sol)
        except Exception as e:
            return f"Error: {str(e)}"

        return str(solutions)

    def handle_assertion(self, code):
        try:
            self.prolog.assertz(code)
            return "Assertion added."
        except Exception as e:
            return f"Error: {str(e)}"

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        if not silent:
            stream_content = {'name': 'stdout',
                              'text': self.process_prolog(code)}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {
            'status': 'ok',
            'execution_count': self.execution_count,
            'payload': [],
            'user_expressions': {},
        }
