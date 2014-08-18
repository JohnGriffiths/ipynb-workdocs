# =====================
# ipynb-workdocs utils
# ====================



from IPython import get_ipython
#ipython = get_ipython()
mgc = get_ipython().magic


def run_nbconvert(nb_pfx,doc_title = '', doc_author = ''):

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
  from datetime import datetime
  today = str(datetime.now()).split(' ')[0]
  today

  # Specify some filenames
  #nb_pfx = 'Chapter1'
  master_nb = '%s__master_nb.ipynb' %nb_pfx

  cherrypick_class_file = 'ipynb_wd_cherry_picking_preprocessor.py'
  config_file = 'ipynb_wd_ipython_nbconvert_config.py'
  copy_writer_file = 'notebook_copy_writer.py'

  nbc2pdf_template = 'nbc_tpl__latex_report_nocode.tplx'
  nbc2slides_template = 'nbc_tpl__slides_reveal_output_toggle.tpl'

  # files to be produced:
  mother_nb = '%s__mother_nb__%s.ipynb' %(nb_pfx, today) 
  html_nb = '%s__html_nb__%s.ipynb' %(nb_pfx, today) 
  pdf_nb = '%s__pdf_nb__%s.ipynb' %(nb_pfx, today)
  slides_nb = '%s__slides_nb__%s.ipynb' %(nb_pfx, today)

  html_file = '%s__html__%s.html' %(nb_pfx, today) 
  pdf_file = '%s__pdf__%s.pdf' %(nb_pfx, today)
  slides_file = '%s__slides__%s.slides.html' %(nb_pfx, today)


  # Get folder locations
  import os
  cwd = os.getcwd()
  outdir = cwd + '/%s__workdocs__%s' %(nb_pfx,today)
  mgc('system rm -r $outdir')
  mgc('system mkdir $outdir')
  ipynb_wd_loc = '/media/sf_SharedFolder/Code/git_repos_of_mine/ipynb-workdocs' #cwd.split('/examples')[0]
  cherry_picker_loc = ipynb_wd_loc + '/notebook_cherry_picker'



  cherrypick_template =  'ipython nbconvert %s --CherryPickingPreprocessor.expression="%s" '\
               '--config %s' 


  # Got to outdir and run stuff
  print '\ncopying to outdir and running stuff there'

  os.chdir(outdir)
  cp_cmd = 'cp %s/%s %s/' %(cwd,master_nb,outdir)
  res = mgc('system $cp_cmd')
  print '\n%s\n\n%s' %(cp_cmd,'\n'.join(res))

  cp_cmd = 'cp %s/%s %s/' %(cherry_picker_loc,cherrypick_class_file,outdir)
  res = mgc('system $cp_cmd')

  cp_cmd = 'cp %s/%s %s/' %(cherry_picker_loc,copy_writer_file, outdir)
  res = mgc('system $cp_cmd')

  print '\n%s\n\n%s' %(cp_cmd,'\n'.join(res))

  cp_cmd = 'cp %s/%s %s/' %(cherry_picker_loc,config_file, outdir)
  res = mgc('system $cp_cmd')
  print '\n%s\n\n%s' %(cp_cmd,'\n'.join(res))

  cp_cmd = 'cp %s/templates/%s %s/' %(ipynb_wd_loc,nbc2pdf_template, outdir)
  res = mgc('system $cp_cmd')

  print '\n%s\n\n%s' %(cp_cmd,'\n'.join(res))

  cp_cmd = 'cp %s/templates/%s %s/' %(ipynb_wd_loc,nbc2slides_template, outdir)
  res = mgc('system $cp_cmd')

  print '\n%s\n\n%s' %(cp_cmd,'\n'.join(res))



  #!cp ../../notebook_cherry_picker/$cherrypick_class_file .
  #!cp ../../notebook_cherry_picker/$config_file .
  #!cp ../../notebook_cherry_picker/$copy_write_file .
  #!cp ../../templates/$nbc2pdf_template .
  #!cp ../../templates/$nbc2slides_template .#

  # Fill in some variables in the templates
  temp_tpl = '/tmp/tmp_tplx.tplx'
  #doc_title = 'Endeavour Project: \n Rolldoc'
  #doc_title = 'Chapter 1'
  #doc_title = 'TVB tools: \n tvb-scripting, tvb-sumatra, tvb-nipype'
  #doc_author = 'J.D. Griffiths'
  #!cp $nbc2pdf_template $temp_tpl
  res = mgc('system cp $nbc2pdf_template $temp_tpl')

  open(nbc2pdf_template, 'w+').write(open(temp_tpl, 'r')\
                             .read().replace('DOC_TITLE', doc_title)\
                             .replace('DOC_AUTHOR', doc_author))


  # Make mother notebook (remove rough notes)

  thisexpr = "not rough_notes"
  in_nb = master_nb
  out_nb = mother_nb

  nbc_cmd = cherrypick_template %(in_nb, thisexpr, config_file)
  mv_cmd = 'mv %s.output.ipynb %s' %(in_nb.split('.ipynb')[0], out_nb)

  print '\nMaking mother notebook...' 

  res = mgc('system $nbc_cmd')
  #res = %system $nbc_cmd
  print '\nrunning nbconvert:\n\n%s\n\nresult:\n\n%s' %(nbc_cmd,'\n'.join(res))

  res = mgc('system $mv_cmd')
  #res = %system $mv_cmd
  print '\nrenaming output:\n\n%s\n\n\n%s' %(mv_cmd,'\n'.join(res))


  # Make html notebook (remove rough notes)

  thisexpr = "(not omit_html) or html_only"
  in_nb = mother_nb
  out_nb = html_nb

  nbc_cmd = cherrypick_template %(in_nb, thisexpr, config_file)
  mv_cmd = 'mv %s.output.ipynb %s' %(in_nb.split('.ipynb')[0], out_nb)

  print '\nMaking html notebook...' 

  #res = %system $nbc_cmd
  res = mgc('system $nbc_cmd')
  print '\nrunning nbconvert:\n\n%s\n\nresult:\n\n%s' %(nbc_cmd,'\n'.join(res))

  #res = %system $mv_cmd
  res = mgc('system $mv_cmd')
  print '\nrenaming output:\n\n%s\n\n\n%s' %(mv_cmd,'\n'.join(res))


  # Make slides notebook (remove rough notes)

  thisexpr = "(not omit_slides) or slides_only"
  in_nb = mother_nb
  out_nb = slides_nb

  nbc_cmd = cherrypick_template %(in_nb, thisexpr, config_file)
  mv_cmd = 'mv %s.output.ipynb %s' %(in_nb.split('.ipynb')[0], out_nb)

  print '\nMaking slides notebook...' 

  #res = %system $nbc_cmd
  res = mgc('system $nbc_cmd')
  print '\nrunning nbconvert:\n\n%s\n\nresult:\n\n%s' %(nbc_cmd,'\n'.join(res))

  #res = %system $mv_cmd
  res = mgc('system $mv_cmd')
  print '\nrenaming output:\n\n%s\n\n\n%s' %(mv_cmd,'\n'.join(res))



  # Make pdf notebook (remove rough notes)

  thisexpr = "(not omit_pdf) or pdf_only"
  in_nb = mother_nb
  out_nb = pdf_nb

  nbc_cmd = cherrypick_template %(in_nb, thisexpr, config_file)
  mv_cmd = 'mv %s.output.ipynb %s' %(in_nb.split('.ipynb')[0], out_nb)

  print '\nMaking pdf notebook...' 

  #res = %system $nbc_cmd
  res = mgc('system $nbc_cmd')
  print '\nrunning nbconvert:\n\n%s\n\nresult:\n\n%s' %(nbc_cmd,'\n'.join(res))

  #res = %system $mv_cmd
  res = mgc('system $mv_cmd')
  print '\nrenaming output:\n\n%s\n\n\n%s' %(mv_cmd,'\n'.join(res))




  # Make pdf file

  nbc_cmd = 'ipython nbconvert --to latex --post PDF --template %s %s' %(nbc2pdf_template, pdf_nb)
  mv_cmd = 'mv %s %s' %(pdf_nb.replace('.ipynb', '.pdf'), pdf_file)

  print '\nMaking pdf file...' 

  #res = %system $nbc_cmd
  res = mgc('system $nbc_cmd')
  print '\nrunning nbconvert:\n\n%s\n\nresult:\n\n%s' %(nbc_cmd,'\n'.join(res))

  # res = %system $mv_cmd
  res = mgc('system $mv_cmd')
  print '\nrenaming output:\n\n%s\n\n\n%s' %(mv_cmd,'\n'.join(res))



  # Make slides file

  nbc_cmd = 'ipython nbconvert --to slides --template %s %s' %(nbc2slides_template, slides_nb)
  mv_cmd = 'mv %s %s' %(slides_nb.replace('.ipynb', '.slides.html'), slides_file)

  print '\nMaking slides file...' 

  #res = %system $nbc_cmd
  res = mgc('system $nbc_cmd')
  print '\nrunning nbconvert:\n\n%s\n\nresult:\n\n%s' %(nbc_cmd,'\n'.join(res))

  #res = %system $mv_cmd
  res = mgc('system $mv_cmd')
  print '\nrenaming output:\n\n%s\n\n\n%s' %(mv_cmd,'\n'.join(res))


  # return to start dir
  os.chdir(cwd)

  print '\n\n\n\nDone! :) \n\n'



