
from copy import deepcopy
from IPython.nbconvert.preprocessors import Preprocessor
from IPython.utils.traitlets import Unicode

from IPython.config import Config
from IPython import nbformat

from IPython.nbconvert import NotebookExporter


import sys

class FilterCellsPreprocessor(Preprocessor):

    expression = Unicode('True', config=True, help="Cell tag expression.")

    def preprocess(self, nb, resources):

        
        print '\n\nFiltering notebook with expression:   "%s"\n\n' %self.expression
        # Set all expression tags to False
        expr_tags = [e for e in self.expression.split(' ') if e not in ['and', 'or']]
        for e in expr_tags:
          exec e + ' = False'
        
        # Report this to screen
        #for e in expr_tags:
        #  print('%s is %s' %(e,eval(e)))        
        
        # Loop through each cell, remove cells that dont match the query.
        remove_indices = []; keep_indices = []
        for index, cell in enumerate(nb.cells):
        
          # for each cell, first set all expression tags to False by default
          for e in expr_tags: exec e + ' = False'

          # then for those cell tags in the metadata, set those variables to be 
          # whatever value the tags are
          if 'cell_tags' in cell.metadata:
            for _name,_val in cell.metadata.cell_tags.items():
              exec '%s = %s' %(_name, _val)
            #except NameError as Error:  
              '' #  print('tags not found')
              
            
          # now evaluate the expression for that cell. if False, remove the cell
          res = eval(self.expression)
          
          if res: keep_indices.append(index)
          else: remove_indices.append(index)
            
          
        # the [::-1] index here flips the list so that the highest numbers come first. 
        # this is essential, otherwise the cells referred to by each index
        # would change on each iteration of the loop. 
        for remove_index in remove_indices[::-1]: 
          del nb.cells[remove_index]

        print('\n\nfiltered out cells: \n\n%s' %remove_indices)
        
        print('\n\nkept cells: \n\n%s \n\n' %keep_indices)

        resources['notebook_copy'] = deepcopy(nb)
        return nb, resources

        
def filter_notebook(expr,in_file,out_file=None):
    
  c = Config() 
  c.FilterCellsPreprocessor.expression = expr

  exporter = NotebookExporter(preprocessors=[FilterCellsPreprocessor], config=c)
  body,resources = exporter.from_file(in_file)

  if out_file:
    write_nb(body,resources,out_file)
    print 'written to: %s \n\n' %out_file
  else:
    return (body,resources)


def write_nb(output, resources, outfilename):
  with open(outfilename, 'w') as outfile:
    nbformat.write(resources['notebook_copy'], outfile)
    
    
if __name__ == '__main__':
    
  expr = sys.argv[1]
  in_file = sys.argv[2]
  out_file=sys.argv[3]  
     
  filter_notebook(expr,in_file,out_file)
