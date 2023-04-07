from functools import reduce
from ipykernel.kernelbase import Kernel
from pyswip import Prolog, Functor, Query, Variable, call, Term

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
    language_info = {
        'mimetype': 'text/x-prolog',
        'name': 'prolog',
        'file_extension': '.pl',
        'pygments_lexer': 'prolog',
    }

    def __init__(self, **kwargs):
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

        try:
            # Parse the query string into a Functor and its arguments.
            functor_name, args_str = query_str.split("(", 1)
            args_str = args_str.rstrip(")")
            args = args_str.split(", ")

            # Convert the arguments to either Variable or a string (if a constant).
            variables = []
            converted_args = []
            for arg in args:
                if arg.isupper():
                    var = Variable(arg)
                    variables.append(var)
                    converted_args.append(var)
                else:
                    converted_args.append(arg)

            # Create the Functor object with the parsed name and arguments.
            functor = Functor(functor_name, len(converted_args))

            # Execute the query.
            query = Query(functor(*converted_args))

            # Collect results.
            results = []
            while query.nextSolution():
                result = {str(var): var.value for var in variables}
                results.append(result)

            # Close the query.
            query.closeQuery()

            res = str(results)
        except Exception as e:
            res = f"Error: {str(e)}"

        return res

    def handle_assertion(self, code):
        try:
            assertz = Functor("assertz", 1)
            terms = code.split("(")
            functor_name = terms[0]
            arguments = terms[1].strip(")").split(", ")
            functor = Functor(functor_name, len(arguments))
            call(assertz(functor(*arguments)))
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
