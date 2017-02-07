# This code can be put in any Python module, it does not require IPython
# itself to be running already.  It only creates the magics subclass but
# doesn't instantiate it yet.
# from __future__ import print_function
import json
from IPython.core.magic import (Magics, magics_class, line_magic,
                                cell_magic, line_cell_magic)
from IPython.display import HTML, display


# The class MUST call this class decorator at creation time
@magics_class
class WebpplMagics(Magics):

    def __init__(self, **kwargs):
            super(WebpplMagics, self).__init__(**kwargs)

    @line_magic
    def lmagic(self, line):
        "my line magic"
        print("Full access to the main IPython object:", self.shell)
        print("Variables in the user namespace:", list(self.shell.user_ns.keys()))
        return line

    @cell_magic
    def webppl(self, line, cell):
        "my cell magic"
        code = json.dumps(cell)
        store = json.dumps(self.shell.user_ns['store'])

        h = """
            <script>
            requirejs.config({
                paths: {
                    webppl: "//cdn.webppl.org/webppl-v0.9.1"
                }
            });
            require(['webppl'], function(webppl) {
                window.webppl = webppl;
            });
            </script>

            <script>
            const code = JSON.parse('""" + code + """');
            const initialStore = JSON.parse('""" + store + """');
            var result;
            webppl.run(code, function(s,x) {result = x},
                {initialStore: initialStore});
            let return = JSON.stringify(result)
            IPython.kernel.Notebook.execute("result='"+return+"'")
            result
            </script>
            """
        display(HTML(h))

    @line_cell_magic
    def lcmagic(self, line, cell=None):
        "Magic that works both as %lcmagic and as %%lcmagic"
        if cell is None:
            print("Called as line magic")
            return line
        else:
            print("Called as cell magic")
            return line, cell


def load_ipython_extension(ipython):
    ip = ipython
    # ip = get_ipython()
    ip.register_magics(WebpplMagics)

if __name__ == "__main__":
    load_ipython_extension(get_ipython())
