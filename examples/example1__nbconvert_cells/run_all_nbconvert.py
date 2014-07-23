
# Example 1 Nbconvert commmands 
# -------------------

# (for loading into notebook)


# Get the date
from datetime import datetime
today = str(datetime.now()).split(' ')[0]
today

# Get folder locations
import os
cwd = os.getcwd()
outdir = cwd + '/outputs'
!rm -r $outdir
!mkdir $outdir
ipynb_wd_loc = cwd.split('/examples')[0]
cherry_picker_loc = ipynb_wd_loc + '/notebook_cherry_picker'


# Specify some filenames
nb_pfx = 'example1'
master_nb = '%s__master_nb.ipynb' %nb_pfx

cherrypick_template =  'ipython nbconvert %s --CherryPickingPreprocessor.expression="%s" '\
             '--config %s' 

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


# Got to outdir and run stuff
print '\ncopying to outdir and running stuff there'

os.chdir(outdir)
cp_cmd = 'cp %s/%s %s/' %(cwd,master_nb,outdir)
res = %system $cp_cmd
print '\n%s\n\n%s' %(cp_cmd,'\n'.join(res))

cp_cmd = 'cp %s/%s %s/' %(cherry_picker_loc,cherrypick_class_file,outdir)
res = %system $cp_cmd

cp_cmd = 'cp %s/%s %s/' %(cherry_picker_loc,copy_writer_file, outdir)
res = %system $cp_cmd
print '\n%s\n\n%s' %(cp_cmd,'\n'.join(res))

cp_cmd = 'cp %s/%s %s/' %(cherry_picker_loc,config_file, outdir)
res = %system $cp_cmd
print '\n%s\n\n%s' %(cp_cmd,'\n'.join(res))

cp_cmd = 'cp %s/templates/%s %s/' %(ipynb_wd_loc,nbc2pdf_template, outdir)
res = %system $cp_cmd
print '\n%s\n\n%s' %(cp_cmd,'\n'.join(res))

cp_cmd = 'cp %s/templates/%s %s/' %(ipynb_wd_loc,nbc2slides_template, outdir)
res = %system $cp_cmd
print '\n%s\n\n%s' %(cp_cmd,'\n'.join(res))



#!cp ../../notebook_cherry_picker/$cherrypick_class_file .
#!cp ../../notebook_cherry_picker/$config_file .
#!cp ../../notebook_cherry_picker/$copy_write_file .
#!cp ../../templates/$nbc2pdf_template .
#!cp ../../templates/$nbc2slides_template .#


# Fill in some variables in the templates
temp_tpl = '/tmp/tmp_tplx.tplx'
doc_title = 'Project X Rolldoc'
doc_author = 'J.D. Griffiths'
!cp $nbc2pdf_template $temp_tpl
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

res = %system $nbc_cmd
print '\nrunning nbconvert:\n\n%s\n\nresult:\n\n%s' %(nbc_cmd,'\n'.join(res))

res = %system $mv_cmd
print '\nrenaming output:\n\n%s\n\n\n%s' %(mv_cmd,'\n'.join(res))


# Make html notebook (remove rough notes)

thisexpr = "(not omit_html) or html_only"
in_nb = mother_nb
out_nb = html_nb

nbc_cmd = cherrypick_template %(in_nb, thisexpr, config_file)
mv_cmd = 'mv %s.output.ipynb %s' %(in_nb.split('.ipynb')[0], out_nb)

print '\nMaking html notebook...' 

res = %system $nbc_cmd
print '\nrunning nbconvert:\n\n%s\n\nresult:\n\n%s' %(nbc_cmd,'\n'.join(res))

res = %system $mv_cmd
print '\nrenaming output:\n\n%s\n\n\n%s' %(mv_cmd,'\n'.join(res))


# Make slides notebook (remove rough notes)

thisexpr = "(not omit_slides) or slides_only"
in_nb = mother_nb
out_nb = slides_nb

nbc_cmd = cherrypick_template %(in_nb, thisexpr, config_file)
mv_cmd = 'mv %s.output.ipynb %s' %(in_nb.split('.ipynb')[0], out_nb)

print '\nMaking slides notebook...' 

res = %system $nbc_cmd
print '\nrunning nbconvert:\n\n%s\n\nresult:\n\n%s' %(nbc_cmd,'\n'.join(res))

res = %system $mv_cmd
print '\nrenaming output:\n\n%s\n\n\n%s' %(mv_cmd,'\n'.join(res))



# Make pdf notebook (remove rough notes)

thisexpr = "(not omit_pdf) or pdf_only"
in_nb = mother_nb
out_nb = pdf_nb

nbc_cmd = cherrypick_template %(in_nb, thisexpr, config_file)
mv_cmd = 'mv %s.output.ipynb %s' %(in_nb.split('.ipynb')[0], out_nb)

print '\nMaking pdf notebook...' 

res = %system $nbc_cmd
print '\nrunning nbconvert:\n\n%s\n\nresult:\n\n%s' %(nbc_cmd,'\n'.join(res))

res = %system $mv_cmd
print '\nrenaming output:\n\n%s\n\n\n%s' %(mv_cmd,'\n'.join(res))




# Make pdf file

nbc_cmd = 'ipython nbconvert --to latex --post PDF --template %s %s' %(nbc2pdf_template, pdf_nb)
mv_cmd = 'mv %s %s' %(pdf_nb.replace('.ipynb', '.pdf'), pdf_file)

print '\nMaking pdf file...' 

res = %system $nbc_cmd
print '\nrunning nbconvert:\n\n%s\n\nresult:\n\n%s' %(nbc_cmd,'\n'.join(res))

res = %system $mv_cmd
print '\nrenaming output:\n\n%s\n\n\n%s' %(mv_cmd,'\n'.join(res))



# Make slides file

nbc_cmd = 'ipython nbconvert --to slides --template %s %s' %(nbc2slides_template, slides_nb)
mv_cmd = 'mv %s %s' %(slides_nb.replace('.ipynb', '.slides.html'), slides_file)

print '\nMaking slides file...' 

res = %system $nbc_cmd
print '\nrunning nbconvert:\n\n%s\n\nresult:\n\n%s' %(nbc_cmd,'\n'.join(res))

res = %system $mv_cmd
print '\nrenaming output:\n\n%s\n\n\n%s' %(mv_cmd,'\n'.join(res))


# return to start dir
os.chdir(cwd)

print '\n\n\n\nDone! :) \n\n'