"""Sphinx directive for building code from snippets."""

from contextlib import redirect_stdout
from io import StringIO

from docutils import nodes

import ratapi

from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective
from sphinx.util.typing import ExtensionMetadata


class OutputDirective(SphinxDirective):
    """A directive for getting the output of some code."""

    has_content = True
    optional_arguments = 1

    def run(self) -> list[nodes.Node]:
        language = self.arguments[0]
        code = "\n".join(self.content)

        if language == "Python":
            try:
                output_print = write_python_output(code, self.env.snippets_env)
            except Exception as err:
                raise RuntimeError(f"Error running {code}: {err}")
        if language == "Matlab":
            try:
                output_print = write_matlab_output(code, self.env.matlab_engine)
            except Exception as err:
                raise RuntimeError(f"Error running {code}: {err}")

        output = nodes.literal_block(output_print, output_print)
        output["language"] = "text"

        return [output]


def setup(app: Sphinx) -> ExtensionMetadata:
    app.add_directive("output", OutputDirective)

    def setup_envs(*ignore):
        """Initialise Python/MATLAB environments."""
        app.env.snippets_env = {"RAT": ratapi} 
        app.env.matlab_engine = setup_matlab()
        app.env.matlab_engine.eval(
            "cd('API'); addPaths; cd('..'); ratVars = who;", nargout=0
        )

    def clear_envs(*ignore):
        """Clear Python/MATLAB environments from the build environment."""
        app.env.snippets_env = {"RAT": ratapi}
        app.env.matlab_engine.eval(
            r"clearvars('-except', 'ratVars', ratVars{:});", nargout=0
        )

    def del_engine(*ignore):
        """Stop and delete the MATLAB engine when building is finished."""
        del app.env.snippets_env
        app.env.matlab_engine.quit()
        del app.env.matlab_engine

    app.connect("builder-inited", setup_envs)
    app.connect("doctree-read", clear_envs)
    app.connect("env-updated", del_engine)


class FallbackMatlabEngine:
    """A fallback class that intercepts calls to MATLAB engine when the engine is not available."""

    def eval(self, *args, **kwargs):
        pass 

    def quit(self):
        pass


def setup_matlab():
    """Create a MATLAB engine, or a fallback if MATLAB engine is not available."""
    try:
        from matlab.engine import start_matlab
    except ImportError:
        return FallbackMatlabEngine()

    print("Starting up MATLAB Engine for snippets...")
    return start_matlab()


def write_python_output(code: str, env: dict | None) -> str:
    """Run arbitrary Python code and return the output.

    Parameters
    ----------
    code : str
        The code to be run.
    env : dict or None
        The predefined environment.

    Returns
    -------
    str
        The output of running the code.

    """
    if env is None:
        env = {}
    with StringIO() as buf:
        with redirect_stdout(buf):
            exec(code, None, env)

        return buf.getvalue()


def write_matlab_output(code: str, engine) -> str:
    """Run arbitrary MATLAB code and return the output.

    Parameters
    ----------
    code : str
        The code to be run.
    engine : MatlabEngine
        The predefined MATLAB engine.

    Returns
    -------
    str
        The output of running the code.

    """
    with StringIO() as buf:
        engine.eval(code, nargout=0, stdout=buf)

        return buf.getvalue()
