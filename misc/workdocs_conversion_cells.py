
## ---New cell---


#nb_pfx = 'Endeavour_project_rolldoc'
nb_pfx = 'tvb_param_exploration'

## ---New cell---

from datetime import datetime
today = str(datetime.now()).split(' ')[0]
today

## ---New cell---


import os
cwd = os.getcwd()

## ---New cell---



#workdocs_dir = '/home/jgriffiths/Code/git_repos_of_mine/bitbucket/work/workdocs'
#workdocs_dir = '/media/sf_SharedFolder/Code/git_repos_of_mine/bitbucket/Work/workdocs'
workdocs_dir = '/home/jgriffiths/Code/libraries_of_mine/bitbucket/Work/workdocs'

os.chdir(workdocs_dir + '/nbconverted')

## ---New cell---


#!cp $workdocs_dir/masters/$nb_pfx__master_nb.ipynb .
#!cp ../masters/Endeavour_project_rolldoc__master_nb.ipynb .
cp_cmd = 'cp %s/masters/%s__master_nb.ipynb %s/nbconverted/' %(workdocs_dir,
                                                               nb_pfx,workdocs_dir)

! $cp_cmd

## ---New cell---

tex_changes = {'replacestrs': [[r'\usepackage[utf8x]{inputenc} % Allow utf-8 characters in the tex document',
                               r'% \usepackage[utf8x]{inputenc} % Allow utf-8 characters in the tex document'\
                               '% IPYNB TEX CHANGE - COMMENTED OUT']] }


## ---New cell---

# for the blog this is principally to just remove 
# rough notes; copy the 'mother' notebook to the blog folder
import sys
#sys.path.append('/media/sf_SharedFolder/Code/git_repos_of_mine/ipynb-workdocs') # (main ipynb-workdocs dir)
sys.path.append('/home/jgriffiths/Code/libraries_of_mine/github/ipynb-workdocs')
import ipynb_wd_utils as iwu
#iwu.run_nbconvert(nb_pfx = nb_pfx,
#                  pdf_title = nb_pfx,
#                  pdf_author = 'J. D. Griffiths', 
#                  tex_changes=tex_changes)

res = iwu.run_nbconvert(nb_pfx = nb_pfx, 
                        ipynb_wd_version = '0.2',
                        pdf_title=nb_pfx, #pdf_title,
                        pdf_author='J. D. Griffiths', #pdf_author,
                        tex_changes=tex_changes)

## ---New cell---

fname =  nb_pfx + '__workdocs__' + today + '/' + nb_pfx\
         + '__pdf_nb__' + today + '_tidied.pdf'
    

## ---New cell---
    
!okular $fname

## ---New cell---

!okular EP_rd__workdocs__2014-12-08/EP_rd__pdf_nb__2014-12-08_tidied.pdf


## ---New cell---

#!okular Endeavour_project_rolldoc__workdocs__2014-09-05/
!okular EP_rd__workdocs__2014-10-25/EP_rd__pdf_nb__2014-10-25_tidied.pdf
#Endeavour_project_rolldoc__workdocs__2014-09-05/
today


## ---New cell---


from IPython.nbconvert.postprocessors import ServePostProcessor
server = ServePostProcessor(port=8053)
server('%s/%s' %(outdir,slides_file))