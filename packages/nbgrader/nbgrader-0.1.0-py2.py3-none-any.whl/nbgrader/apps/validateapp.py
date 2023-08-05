from IPython.utils.traitlets import Unicode, List, Bool
from IPython.nbconvert.nbconvertapp import NbConvertApp, DottedOrNone
from nbgrader.preprocessors import DisplayAutoGrades, Execute, ClearOutput
from nbgrader.apps.baseapp import BaseApp, base_flags, base_aliases

aliases = {}
aliases.update(base_aliases)
aliases.update({
})

flags = {}
flags.update(base_flags)
flags.update({
    'invert': (
        {'DisplayAutoGrades': {'invert': True}},
        "Complain when cells pass, rather than vice versa."
    )
})

class ValidateApp(BaseApp, NbConvertApp):

    name = u'nbgrader-validate'
    description = u'Validate a notebook by running it'

    aliases = aliases
    flags = flags

    examples = """
        You can run `nbgrader validate` on just a single file, e.g.:
            nbgrader validate "Problem 1.ipynb"

        Or, you can run it on multiple files using shell globs:
            nbgrader validate "Problem Set 1/*.ipynb"

        If you want to test instead that none of the tests pass (rather than that
        all of the tests pass, which is the default), you can use --invert:
            nbgrader validate --invert "Problem 1.ipynb"
        """

    preprocessors = List([
        ClearOutput,
        Execute,
        DisplayAutoGrades
    ])

    export_format = Unicode('notebook')
    use_output_suffix = Bool(False)
    postprocessor_class = DottedOrNone('')
    notebooks = List([])
    writer_class = DottedOrNone('FilesWriter')
    output_base = Unicode('')

    def _log_level_default(self):
        return 'ERROR'

    def _classes_default(self):
        classes = super(ValidateApp, self)._classes_default()
        for pp in self.preprocessors:
            if len(pp.class_traits(config=True)) > 0:
                classes.append(pp)
        return classes

    def build_extra_config(self):
        extra_config = super(ValidateApp, self).build_extra_config()
        extra_config.Exporter.default_preprocessors = self.preprocessors
        return extra_config

    def init_single_notebook_resources(self, notebook_filename):
        resources = super(ValidateApp, self).init_single_notebook_resources(notebook_filename)
        resources['nbgrader'] = {}
        return resources

    def write_single_notebook(self, output, resources):
        return
