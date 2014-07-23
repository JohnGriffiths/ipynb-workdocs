
from datetime import datetime
import os


class tools(object):

  """
  ==============
  Ipynb wd tools
  ==============


  Usage
  -----    

  ipynb_wd_tools_dir = '/media/sf_WINDOWS_D_DRIVE/Neurodebian/code/git_repos/notebook_cherry_picker/ipynb_workdocs'
  import sys
  sys.path.append(ipynb_wd_tools_dir)

  from ipynb_wd_tools import tools
  t = tools(nb_pfx = 'rolldoc', code_dir = ipynb_tools_dir)
  t.make_all(newdir = 'run_all_tester3', delete_orig=False)
  
  
  

  """
 
  def __init__(self,nb_pfx,nb_orig_dir = '.', code_dir = '.'):
 
    import os
    
    today = str(datetime.date(datetime.now()))
    self.today = today

    # Files
    self.nb_pfx = nb_pfx
    self.nb_master = '%s__master.ipynb' %nb_pfx
    self.nb_nonrough = '%s__notebook__%s.ipynb' %(nb_pfx,today)
    self.nb_pdf = '%s__pdf__%s.ipynb' %(nb_pfx, today)
    self.nb_slides = '%s__slides__%s.ipynb' %(nb_pfx, today)
    self.nb_html = '%s__html__%s.ipynb' %(nb_pfx, today) 

    self.nbc_config = 'ipynb_wd_ipython_nbconvert_config.py'
    self.nb_copywriter = 'notebook_copy_writer.py'    
    self.cherry_picking_preprocessor = 'ipynb_wd_cherry_picking_preprocessor.py'
    self.ipynb_wd_tools_file = 'ipynb_wd_tools.py'

    self.nbc_template_pdf_filename = 'nbc_tpl__latex_report_nocode.tplx' #%code_dir
    self.nbc_template_slides_filename = 'nbc_tpl__slides_reveal_output_toggle.tpl' #%code_dir


    # Nbconvert commands
    self.chpck_cmd_configfile = 'ipython nbconvert %s --CherryPickingPreprocessor.expression="%s" --config=%s' 
    self.chpck_cmd  = 'ipython nbconvert %s --CherryPickingPreprocessor.expression="%s" '\
                             '--Exporter.preprocessors = ["ipynb_wd_tools.CherryPickingPreprocessor"] '\
                             '--NbConvertApp.writer_class = "ipynb_wd_tools.NotebookCopyWriter" '



    self.nbc_cmd__nb_master_2_nb_nonrough = self.chpck_cmd_configfile %(self.nb_master,"not rough_notes", self.nbc_config)

    self.nbc_cmd__nb_nonrough_2_nb_pdf =  self.chpck_cmd_configfile  %(self.nb_nonrough,"not omit_pdf", self.nbc_config)
    self.nbc_cmd__nb_pdf_2_pdf = 'ipython nbconvert --to pdf --template %s %s' %(self.nbc_template_pdf_filename, self.nb_pdf)

    self.nbc_cmd__nb_nonrough_2_nb_slides = self.chpck_cmd_configfile  %(self.nb_nonrough,"not omit_slides", self.nbc_config) 
    self.nbc_cmd__nb_slides_2_slides = 'ipython nbconvert --to slides --template %s %s' %(self.nbc_template_slides_filename, self.nb_slides)

    self.nbc_cmd__nb_nonrough_2_nb_html = self.chpck_cmd_configfile  %(self.nb_nonrough,"not omit_html", self.nbc_config)
    self.nbc_cmd__nb_html_2_html = 'ipython nbconvert --to html %s' %(self.nb_html)
         

    self.code_dir = code_dir
 
    self.nb_orig_dir = nb_orig_dir


    self.cherry_picking_ipython_nbconvert_config_text = """\
c = get_config()

#Export all the notebooks in the current directory to the sphinx_howto format.
c.Exporter.preprocessors = ['ipynb_wd_tools.CherryPickingPreprocessor']
c.NbConvertApp.writer_class = 'ipynb_wd_tools.NotebookCopyWriter'""" #%(code_dir,code_dir)



  def make_all(self,newdir=None,delete_orig=False):

    import os

    start_dir = os.getcwd()
    if newdir is not None:
      print 'making and moving to new dir: %s' %(newdir)    
      if os.path.isdir(newdir):
        os.system('rm -r %s' %newdir)

      os.mkdir(newdir)
      os.chdir(newdir)
      #for f in [self.nb_master, self.nbc_config, self.nb_copywriter,self.cherry_picking_preprocessor]:
      #  os.system('cp %s/%s .' %(self.code_dir,f))

      os.system('cp %s/%s .' %(self.code_dir,self.ipynb_wd_tools_file))
      with open(self.nbc_config, 'wb') as f:
        f.writelines(self.cherry_picking_ipython_nbconvert_config_text)

      os.system('cp %s/%s .' %(self.nb_orig_dir,self.nb_master))
      
      os.system('cp %s/%s .' %(self.code_dir, self.nbc_template_pdf_filename))
      os.system('cp %s/%s .' %(self.code_dir, self.nbc_template_slides_filename))


      if delete_orig:
        print 'removing orig file %s' %('%s/%s' %(self.code_dir,self.nb_master))
        os.system('rm %s/%s' %(self.code_dir,self.nb_master))

        
    self.make_nonrough_notebook()
    self.make_pdf()
    self.make_slides()
    self.make_html()
    
    os.chdir(start_dir)

  def make_nonrough_notebook(self): 
    
    # Make new notebook from master with rough notes removed
    print '\n\n\nMaking non-rough notebook:\n'
    
    print '\n\n%s\n\n' %self.nbc_cmd__nb_master_2_nb_nonrough
    os.system(self.nbc_cmd__nb_master_2_nb_nonrough)

    mv_cmd = 'mv %s.output.ipynb %s' %(self.nb_master.split('.ipynb')[0],self.nb_nonrough)
    print '\n\n%s\n\n' %mv_cmd
    os.system(mv_cmd)
 
    print '\nDone.'


  def make_pdf(self, remove_pdf_notebook=True):

    # Make PDF notebook from non-rough notebook with 'omit_pdf' tagged cells removed 
    print '\n\n\nMaking PDF notebook:\n'

    print '\n\n%s\n\n' %self.nbc_cmd__nb_nonrough_2_nb_pdf
    os.system(self.nbc_cmd__nb_nonrough_2_nb_pdf)

    mv_cmd = 'mv %s.output.ipynb %s' %(self.nb_nonrough.split('.ipynb')[0],self.nb_pdf)
    print '\n\n%s\n\n' %mv_cmd
    os.system(mv_cmd)


    # Convert to PDF
    print '\n\nNbconverting to PDF'
    nbc_cmd = self.nbc_cmd__nb_pdf_2_pdf
    print 'running with command: \n%s\n' %nbc_cmd
    os.system(nbc_cmd)
   

    # Remove unwanted files
    if remove_pdf_notebook:
      os.system('rm %s' %self.nb_pdf)
 
    print '\n\nDone.'



  def make_slides(self,remove_slides_notebook=True):
    
    # Make Slides notebook from non-rough notebook with 'omit_pdf' tagged cells removed
    print '\n\n\nMaking slides notebook:\n'

    print '\n\n%s\n\n' %self.nbc_cmd__nb_nonrough_2_nb_slides
    os.system(self.nbc_cmd__nb_nonrough_2_nb_slides)

    mv_cmd = 'mv %s.output.ipynb %s' %(self.nb_nonrough.split('.ipynb')[0],self.nb_slides)
    print '\n\n%s\n\n' %mv_cmd
    os.system(mv_cmd)


    # Convert to slides
    print '\n\nNbconverting to slides'
    nbc_cmd = self.nbc_cmd__nb_slides_2_slides
    print 'running with command: \n%s\n' %nbc_cmd
    os.system(nbc_cmd)

    # Remove unwanted files
    if remove_slides_notebook:
      os.system('rm %s' %self.nb_slides)


    print '\n\nDone.'


  def make_html(self, remove_html_notebook=True):

    # Make html notebook from non-rough notebook with 'omit_html' tagged cells removed
    print '\n\n\nMaking slides notebook:\n'

    print '\n\n%s\n\n' %self.nbc_cmd__nb_nonrough_2_nb_html
    os.system(self.nbc_cmd__nb_nonrough_2_nb_html)

    mv_cmd = 'mv %s.output.ipynb %s' %(self.nb_nonrough.split('.ipynb')[0],self.nb_html)
    print '\n\n%s\n\n' %mv_cmd
    os.system(mv_cmd)


    # Convert to HTML
    print '\n\nNbconverting to html'
    nbc_cmd = self.nbc_cmd__nb_html_2_html
    print 'running with command: \n%s\n' %nbc_cmd
    os.system(nbc_cmd)

    # Remove unwanted files
    if remove_html_notebook: 
      os.system('rm %s' %self.nb_html)


    print '\n\nDone.'






from copy import deepcopy
from IPython.nbconvert.preprocessors import Preprocessor
from IPython.utils.traitlets import Unicode

class CherryPickingPreprocessor(Preprocessor):

    expression = Unicode('True', config=True, help="Cell tag expression.")

    def preprocess(self, nb, resources):

        # Loop through each cell, remove cells that dont match the query.
        for worksheet in nb.worksheets:
            remove_indicies = []
            for index, cell in enumerate(worksheet.cells):
                if not self.validate_cell_tags(cell):
                    remove_indicies.append(index)

            for index in remove_indicies[::-1]:
                del worksheet.cells[index]

        resources['notebook_copy'] = deepcopy(nb)
        return nb, resources


    def validate_cell_tags(self, cell):

        #print 'tag expression = %s' %self.expression

        if 'cell_tags' in cell['metadata']:
            return self.eval_tag_expression(cell['metadata']['cell_tags'], self.expression)
        else:
           return True

    def eval_tag_expression(self, tags, expression):

        # Create the tags as True booleans.  This allows us to use python
        # expressions.
        #for tag in tags:
        #    exec tag + " = True"
        for tag in tags:
            thing = tags[tag]
            exec tag + '= thing'
        # Attempt to evaluate expression.  If a variable is undefined, define
        # the variable as false.



        # Attempt to evaluate expression.  If a variable is undefined, define
        # the variable as false.

        # while True:
        #    try:
        #        return eval(expression)
        #    except NameError as Error:
        #        exec str(Error).split("'")[1] + " = False"
        try:
         res= eval(expression)
        except NameError as Error:
         exec str(Error).split("'")[1] + " = False"
         res = eval(expression)
        return res





import IPython.nbformat.current as nbformat

from IPython.nbconvert.writers.base import WriterBase

class NotebookCopyWriter(WriterBase):

    def write(self, output, resources, notebook_name=None, **kw):
        with open(notebook_name + '.output.ipynb', 'w') as outfile:
            nbformat.write(resources['notebook_copy'], outfile, u'ipynb')




#c = get_config()

#Export all the notebooks in the current directory to the sphinx_howto format.
#c.Exporter.preprocessors = ['ipynb_wd_cherry_picking_preprocessor.CherryPickingPreprocessor']
#c.NbConvertApp.writer_class = 'notebook_copy_writer.NotebookCopyWriter'







