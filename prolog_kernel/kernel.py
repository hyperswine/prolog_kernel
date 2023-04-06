from ipykernel.kernelbase import Kernel
import prolog
import re

usage = """\
This is the Prolog kernel.

Example Rules:
    child(stephanie).
    child(thad).
    mother_child(trude, sally).
 
    father_child(tom, sally).
    father_child(tom, erica).
    father_child(mike, tom).
 
    sibling(X, Y) : parent_child(Z, X), parent_child(Z, Y).
 
    parent_child(X, Y) : father_child(X, Y).
    parent_child(X, Y) : mother_child(X, Y).

Example Queries:
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
    # search = None
    language_info = {
        'mimetype': 'text/x-prolog',
        'name': 'prolog',
        'codemirror_mode': {'name': 'prolog'},
        'pygments_lexer': 'prolog',
    }

    # todo, I think just return {'message': msg}
    def print(self, msg):
        return {'message': msg}

    # todo, I think just return {'error': msg}
    def error(self, msg):
        return {'error': msg}

    def get_usage(self):
        return usage

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        if not silent:
            stream_content = {'name': 'stdout', 'text': code}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {
            'status': 'ok',
            'execution_count': self.execution_count,
            'payload': [],
            'user_expressions': {},
        }
