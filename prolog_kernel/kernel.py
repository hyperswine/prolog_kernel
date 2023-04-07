from ipykernel.kernelbase import Kernel
from pyswip import Prolog, Functor, Variable, Query, call

# prolog = Prolog()

usage = """\
Rules:
    child(stephanie).
    child(thad).
    mother_child(trude, sally).
 
    father_child(tom, sally).
    father_child(tom, erica).
    father_child(mike, tom).
 
    sibling(X, Y): parent_child(Z, X), parent_child(Z, Y).
 
    parent_child(X, Y): father_child(X, Y).
    parent_child(X, Y): mother_child(X, Y).

    weather(sunny): NOT weather(rainy).

    weather(sunny): NOT weather(rainy), NOT weather(cloudy).

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
    # search = None
    # or text/x-prolog
    # 'codemirror_mode': {'name': 'prolog'},
    # 'pygments_lexer': 'prolog',
    # not sure about file extensions
    language_info = {
        'mimetype': 'text/plain',
        'name': 'prolog',
        # 'file_extension': '.pl'
        'file_extension': '.txt'
    }

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)

        self.assertz = Functor("assertz", 1)
        self.X = Variable()

    def print(self, msg):
        return {'message': msg}

    def error(self, msg):
        return {'error': msg}

    def get_usage(self):
        return usage

    def process_prolog(self, code):
        # check if is a fact, rule or query

        res2 = ""

        father = Functor("father", 2)
        call(self.assertz(father("michael", "john")))
        X = Variable()
        q = Query(father("michael", X))
        while q.nextSolution():
            res2 += X.value + " "
        q.closeQuery()

        return res2

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        if not silent:
            code2 = self.process_prolog(code)

            stream_content = {'name': 'stdout', 'text': code2}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {
            'status': 'ok',
            'execution_count': self.execution_count,
            'payload': [],
            'user_expressions': {},
        }
