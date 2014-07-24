from copy import deepcopy
from IPython.nbconvert.preprocessors import Preprocessor
from IPython.utils.traitlets import Unicode

class CherryPickingPreprocessor(Preprocessor):

    expression = Unicode('True', config=True, help="Cell tag expression.")

    def preprocess(self, nb, resources):

        # Loop through each cell, remove cells that dont match the query.
        for worksheet in nb.worksheets:
            remove_indices = []
            for index, cell in enumerate(worksheet.cells):
                if not self.validate_cell_tags(cell):
                    remove_indices.append(index)

            for index in remove_indices[::-1]:
                del worksheet.cells[index]

        resources['notebook_copy'] = deepcopy(nb)
        return nb, resources


    def validate_cell_tags(self, cell):
        if 'cell_tags' in cell['metadata']:
            return self.eval_tag_expression(cell['metadata']['cell_tags'], self.expression)
        else: 
            return True

    def eval_tag_expression(self, tags, expression):
        
        # Create the tags as True booleans.  This allows us to use python 
        # expressions.
        for tag in tags:
            tagtag = tags[tag]
            exec tag + " = tagtag"

        # Attempt to evaluate expression.  If a variable is undefined, define
        # the variable as false.
        try:
          res = eval(expression)
        except NameError as Error:
          exec str(Error).split("'")[1] + " = False"
          res = eval(expression)
        return res




