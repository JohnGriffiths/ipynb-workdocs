import IPython.nbformat.current as nbformat

from IPython.nbconvert.writers.base import WriterBase

class NotebookCopyWriter(WriterBase):

    def write(self, output, resources, notebook_name=None, **kw):
        with open(notebook_name + '.output.ipynb', 'w') as outfile:
            nbformat.write(resources['notebook_copy'], outfile, u'ipynb')