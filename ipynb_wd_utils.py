# =====================
# ipynb-workdocs utils
# ====================



from IPython import get_ipython
mgc = get_ipython().magic

import os

from datetime import datetime
import ipynb_wd_utils as iwu

def run_nbconvert(nb_pfx,nb_list=None,pdf_title='',pdf_author = '',tex_changes=None, ipynb_wd_version='0.1', do_html_nb=True,do_html_file=True,do_slides_nb=True,do_slides_file=True,do_pdf_nb=True,do_pdf_file=True,remove_additional_files=False):

  # ipynb-workdocs nbconvert:
  # =========================

  # Using ipynb-workdocs to 

  # a) filter out rough notes
  # b) identify pdf cells
  # c) identify slideshow cells
  # e) identify html cells (maybe)

  # Only need to do the 'second round' of ipynb-wordocs conversion for html and slides, not pdf
  # (...running the pdf conversion anyway. But note that the main pdf for the chapter is compiled 
  # using the cam uni thesis template)


  # Re: Use of ipynb-workdocs cell tags in this doc: 
  # 
  # - cells with notes / commented out text are marked as rough notes
  # - cells with code in that is executed but no figure rendered are marked as 'omit_slides' + 'omit_pdf' + 'omit_html'
  #   (because don't want to include all the functional code in the html, pdf, or slides files)
  # 

  # Usage
  # ----

  # > os.chdir('DoctoralThesis/notebooks/Chapter1')
  # > import ipynb_wd_utils as iwu
  # > iwu.run_nbconvert(nb_pfx='Chapter1',doc_title = 'Chapter 1', doc_author = 'J.D. Griffiths')
  

  # Get the date
  today = str(datetime.now()).split(' ')[0]


  ipynb_wd_loc = '/'.join(iwu.__file__.split('/')[0:-1])

  # If multiple notebooks, concatenate and run html convert separately for each 
  if type(nb_list) == list:
     
    print '\n\nMultiple notebooks provided. Will run nbconvert on each separately and on concatenated notebook.\n'
    # concatenate the notebooks
    cat_cmd = 'python ' + ipynb_wd_loc + '/misc/nbcat.py ' # function borrowed from  ipython tutorial code
    for n in nb_list:

      # Run this functionon the individual files
      # (just for html) 
      iwu.run_nbconvert(n,do_pdf_nb=False,do_pdf_file=False,
                          do_slides_nb=False,do_slides_file=False,
                          remove_additional_files=False,ipynb_wd_version='0.2')
       
      # Add to the concatenate list
      cat_cmd += ' %s__master_nb.ipynb' %n    
 
    cat_cmd += ' > %s__master_nb.ipynb' %nb_pfx
    res = mgc('system $cat_cmd')
    print '\n%s\n\n%s' %(cat_cmd,'\n'.join(res))
    



  # Make new folder and go there
  cwd = os.getcwd()
  outdir = cwd + '/%s__workdocs__%s' %(nb_pfx,today)
  mgc('system rm -r $outdir')
  mgc('system mkdir $outdir')
 
  print '\ngoing to outdir and running stuff there'
  os.chdir(outdir)



  # Specify some filenames
  master_nb = '%s__master_nb.ipynb' %nb_pfx # already exists
  mother_nb = '%s__mother_nb__%s.ipynb' %(nb_pfx, today) # doesn't yet exist

  cherrypick_class_file = 'ipynb_wd_cherry_picking_preprocessor_3.py'
  config_file = 'ipynb_wd_ipython_nbconvert_config_3.py'
  copy_writer_file = 'notebook_copy_writer.py'


  ipynb_wd_loc = '/'.join(iwu.__file__.split('/')[0:-1])
  cherry_picker_loc = ipynb_wd_loc + '/notebook_cherry_picker'

  cherrypick_template =  'ipython nbconvert %s --CherryPickingPreprocessor.expression="%s" '\
               '--config %s' 


  cp_cmd = 'cp %s/%s %s/' %(cwd,master_nb,outdir)
  res = mgc('system $cp_cmd')
  print '\n%s\n\n%s' %(cp_cmd,'\n'.join(res))

  cp_cmd = 'cp %s/%s %s/' %(cherry_picker_loc,cherrypick_class_file,outdir)
  res = mgc('system $cp_cmd')
  print '\n%s\n\n%s' %(cp_cmd,'\n'.join(res))

  cp_cmd = 'cp %s/%s %s/' %(cherry_picker_loc,copy_writer_file, outdir)
  res = mgc('system $cp_cmd')
  print '\n%s\n\n%s' %(cp_cmd,'\n'.join(res))

  cp_cmd = 'cp %s/%s %s/' %(cherry_picker_loc,config_file, outdir)
  res = mgc('system $cp_cmd')
  print '\n%s\n\n%s' %(cp_cmd,'\n'.join(res))



  # Make mother notebook (remove rough notes)

  if ipynb_wd_version=='0.1': 
    thisexpr = "not rough_notes"
  elif ipynb_wd_version=='0.2':
    #thisexpr = '(not pdf) or (not html) or (not slides)'
    #thisexpr = 'pdf or html or slides'
    #thisexpr = 'not (not pdf) or not (not html) or not (not slides)'
    thisexpr = 'pdf or html or slides'

  in_nb = master_nb
  out_nb = mother_nb

  nbc_cmd = cherrypick_template %(in_nb, thisexpr, config_file)
  mv_cmd = 'mv %s.output.ipynb %s' %(in_nb.split('.ipynb')[0], out_nb)

  print '\nMaking mother notebook...' 

  res = mgc('system $nbc_cmd')
  print '\nrunning nbconvert:\n\n%s\n\nresult:\n\n%s' %(nbc_cmd,'\n'.join(res))

  res = mgc('system $mv_cmd')
  print '\nrenaming output:\n\n%s\n\n\n%s' %(mv_cmd,'\n'.join(res))


  # Make html notebook 
  if do_html_nb:

    html_nb = '%s__html_nb__%s.ipynb' %(nb_pfx, today) 

    if ipynb_wd_version=='0.1': 
      thisexpr = "(not omit_html) or html_only"
    elif ipynb_wd_version=='0.2':
      thisexpr = 'html'

    in_nb = mother_nb
    out_nb = html_nb

    nbc_cmd = cherrypick_template %(in_nb, thisexpr, config_file)
    mv_cmd = 'mv %s.output.ipynb %s' %(in_nb.split('.ipynb')[0], out_nb)

    print '\nMaking html notebook...' 

    res = mgc('system $nbc_cmd')
    print '\nrunning nbconvert:\n\n%s\n\nresult:\n\n%s' %(nbc_cmd,'\n'.join(res))

    res = mgc('system $mv_cmd')
    print '\nrenaming output:\n\n%s\n\n\n%s' %(mv_cmd,'\n'.join(res))


  

  # Make slides notebook 
  if do_slides_nb:

    slides_nb = '%s__slides_nb__%s.ipynb' %(nb_pfx, today)

    if ipynb_wd_version=='0.1': 
      thisexpr = "(not omit_slides) or slides_only"
    elif ipynb_wd_version=='0.2':
      thisexpr = "slides"

    in_nb = mother_nb
    out_nb = slides_nb

    nbc_cmd = cherrypick_template %(in_nb, thisexpr, config_file)
    mv_cmd = 'mv %s.output.ipynb %s' %(in_nb.split('.ipynb')[0], out_nb)

    print '\nMaking slides notebook...' 

    res = mgc('system $nbc_cmd')
    print '\nrunning nbconvert:\n\n%s\n\nresult:\n\n%s' %(nbc_cmd,'\n'.join(res))
    res = mgc('system $mv_cmd')
    print '\nrenaming output:\n\n%s\n\n\n%s' %(mv_cmd,'\n'.join(res))



  # Make pdf notebook 
  if do_pdf_nb:


    pdf_nb = '%s__pdf_nb__%s.ipynb' %(nb_pfx, today)

    if ipynb_wd_version=='0.1': 
      thisexpr = "(not omit_pdf) or pdf_only"
    elif ipynb_wd_version=='0.2':
      thisexpr = "not (not pdf)"

    in_nb = mother_nb
    out_nb = pdf_nb

    nbc_cmd = cherrypick_template %(in_nb, thisexpr, config_file)
    mv_cmd = 'mv %s.output.ipynb %s' %(in_nb.split('.ipynb')[0], out_nb)

    print '\nMaking pdf notebook...' 

    res = mgc('system $nbc_cmd')
    print '\nrunning nbconvert:\n\n%s\n\nresult:\n\n%s' %(nbc_cmd,'\n'.join(res))
    res = mgc('system $mv_cmd')
    print '\nrenaming output:\n\n%s\n\n\n%s' %(mv_cmd,'\n'.join(res))


  if do_html_file:

    html_file = '%s__html__%s.html' %(nb_pfx, today)

    print '\nMaking html file...' 
        
    nbc_cmd = 'ipython nbconvert --to html %s' %html_nb
    res = mgc('system $nbc_cmd')
    print '\nrunning nbconvert:\n\n%s\n\nresult:\n\n%s' %(nbc_cmd,'\n'.join(res))


  if do_pdf_file:

    # Make pdf file

    # If no changes to texfile are required, just use
    # 'nbconvert --to latex --post PDF'...

    # If changes to texfile are required, use 
    # 'nbconvert --to latex'... 
    # 'tidy_texfile()'...
    # 'pdflatex'...

    print '\nMaking pdf file...' 

    pdf_file = '%s__pdf__%s.pdf' %(nb_pfx, today)
    nbc2pdf_template = 'nbc_tpl__latex_report_nocode.tplx'

    # Get the pdf template
    cp_cmd = 'cp %s/templates/%s %s/' %(ipynb_wd_loc,nbc2pdf_template, outdir)
    res = mgc('system $cp_cmd')
    print '\n%s\n\n%s' %(cp_cmd,'\n'.join(res))

    # Fill in doc title and doc author in the pdf template
    temp_tpl = '/tmp/tmp_tplx.tplx'
    res = mgc('system cp $nbc2pdf_template $temp_tpl')
    open(nbc2pdf_template, 'w+').write(open(temp_tpl, 'r')\
                             .read().replace('DOC_TITLE', pdf_title)\
                             .replace('DOC_AUTHOR', pdf_author))

    if tex_changes is None:

      nbc_cmd = 'ipython nbconvert --to latex --post PDF --template %s %s' %(nbc2pdf_template, pdf_nb)

      res = mgc('system $nbc_cmd')
      print '\nrunning nbconvert:\n\n%s\n\nresult:\n\n%s' %(nbc_cmd,'\n'.join(res))

      # Rename output
      mv_cmd = 'mv %s %s' %(pdf_nb.replace('.ipynb', '.pdf'), pdf_file)
      res = mgc('system $mv_cmd')
      print '\nrenaming output:\n\n%s\n\n\n%s' %(mv_cmd,'\n'.join(res))


    else:

      # Nbconvert to latex
      nbc_cmd = 'ipython nbconvert --to latex --template %s %s' %(nbc2pdf_template,pdf_nb)
      print '\nMaking tex file...'
      res = mgc('system $nbc_cmd')
      print '\nrunning nbconvert:\n\n%s\n\nresult:\n\n%s' %(nbc_cmd,'\n'.join(res))

      # Tidy texfile
      orig_texfile = pdf_nb.split('.ipynb')[0]+'.tex'
      new_texfile = pdf_nb.split('.ipynb')[0]+'_tidied.tex'
      tidy_texfile(orig_texfile,
                  tex_changes=tex_changes,
                  new_texfile = new_texfile)



      # Run pdflatex
      print 'running pdflatex'

      _cmd = 'pdflatex -interaction=nonstopmode %s' %new_texfile
   
      res1 = mgc('system $_cmd') 
      print '\nrunning pdflatex:\n\n%s\n\nresult:\n\n%s' %(_cmd,'\n'.join(res1))

      res2 = mgc('system $_cmd')
      print '\nrunning pdflatex:\n\n%s\n\nresult:\n\n%s' %(_cmd,'\n'.join(res1))

      res3 = mgc('system $_cmd')  
      print '\nrunning pdflatex:\n\n%s\n\nresult:\n\n%s' %(_cmd,'\n'.join(res3))


      # Rename to the name of pdf_nb
      mv_cmd = 'mv ' + new_texfile.split('.tex')[0]+'.ipynb' + ' ' + pdf_file
      res = mgc('system $mv_cmd') 
      print '\nrenaming output:\n\n%s\n\nresult:\n\n%s' %(_cmd,'\n'.join(res3))

  


 
  # Make slides file
  if do_slides_file:
 
    slides_file = '%s__slides__%s.slides.html' %(nb_pfx, today)
    nbc2slides_template = 'nbc_tpl__slides_reveal_output_toggle.tpl'

    # get the slides template
    cp_cmd = 'cp %s/templates/%s %s/' %(ipynb_wd_loc,nbc2slides_template, outdir)
    res = mgc('system $cp_cmd')
    print '\n%s\n\n%s' %(cp_cmd,'\n'.join(res))


    nbc_cmd = 'ipython nbconvert --to slides --template %s %s' %(nbc2slides_template, slides_nb)
    mv_cmd = 'mv %s %s' %(slides_nb.replace('.ipynb', '.slides.html'), slides_file)

    print '\nMaking slides file...' 

    res = mgc('system $nbc_cmd')
    print '\nrunning nbconvert:\n\n%s\n\nresult:\n\n%s' %(nbc_cmd,'\n'.join(res))

    res = mgc('system $mv_cmd')
    print '\nrenaming output:\n\n%s\n\n\n%s' %(mv_cmd,'\n'.join(res))



  


  if remove_additional_files:
    mgc('system rm *.py*')
    mgc('system rm *.tex')
    mgc('system rm *.toc')
    mgc('system rm *.tpl*')
    


  # return to start dir
  os.chdir(cwd)

  print '\n\n\n\nDone! :) \n\n'




def tidy_texfile(texfile, tex_changes, new_texfile=None):
  """
  Do some simple parsing and modifying of a texfile
  Helps iron out some of the wrinkles of the nbconvert-latex-pdf 
  conversion.

  'tex_changes' is a dictionary containing one or both of 
  'addstrs' and 'replacestrs'

  'addstrs' is a list of strings to append to the beginning of the file. 

  'replacestrs' is a list of 2 item lists, each item being the 
  text string to be replaced, and the new string to replace it with. 
  Strings to be removed are simply replaced with ''. 


  Example:
  --------

  # strings to remove
  replacestrs = [ [r'% Add a bibliography block to the postdoc', '' ],
                  [r'\bibliographystyle{apalike}', ''],
                  [r'\bibliography{Thesis}', '' ],
                  [r'\end{document}', ''],
                  [r'{ \hspace*{\fill} \\}', ''],
                  [r'max size={0.9\linewidth}{0.9\paperheight}',
                   r'max size={0.99\linewidth}{0.99\paperheight}'],
                  [r'\end{tabular}', r'\end{tabular} \\ \vspace{10 mm}'],
                  ['Chapters_1_2_3_4_5_6_7_files', 'Figures']             ]
 
  tex_changes = {'replacestrs': replacestrs}
  tidy_texfile('texfile.tex',
               tex_changes = tex_changes
               newtexfile='newtexfile.tex')


  """

  thetex = open(texfile, 'r').read()
    
  # Add strings
  if 'addstrs' in tex_changes:
    alladdstrs = [a + '\n' for a in tex_changes['addstrs']]
    thetex = alladdstrs + thetex

  # Replace strings
  if 'replacestrs' in tex_changes:
    for r in tex_changes['replacestrs']: thetex = thetex.replace(r[0],r[1])
   
  open(new_texfile,'w').writelines(thetex)







