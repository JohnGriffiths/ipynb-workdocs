

class cloudfiles_nb(object):
    
  def __init__(self,access_token):#app_key,app_secret)

    from dropbox.client import DropboxClient
    from dropbox.session import DropboxSession    
  
    self.client = DropboxClient(access_token)
    
    self.base_dir = 'workdocs-cloudfiles'        
    self.folders_list = [p['path'].replace('/%s/' %self.base_dir, '')\
                         for p in self.client.metadata(self.base_dir)['contents']]
    self.upload_file_res = {}
    
  def initialize_folder(self,folder_name):
    

    self.thisfolder = '%s/%s' %(self.base_dir,folder_name)
    
    if folder_name in self.folders_list:
      print 'folder already exists'
      res = None
    else:
      print 'creating folder'
      res = self.client.file_create_folder(self.thisfolder)
        
    # do something for error
    
    return res

    
  def upload_file(self,filepath):
        
    f = open(filepath, 'r')
    filename = filepath.split('/')[-1]

    newfile = '%s/%s' %(self.thisfolder,filename)
    
    # if filename alread exists, delate and replace
    #filecheck = self.client.search(self.thisfolder, filename)
    #if filecheck: del_res = self.client.file_delete(newfile)
        
    res = self.client.put_file(newfile, f, overwrite=True)
 
    return res


  def get_file_link(self,getfile):
        
    res = self.client.media('%s/%s' %(self.thisfolder,getfile))
    
    # something for error
    
    return res


class nb_fig(object):
    
  def __init__(self, local_file,label,cap,fignum,dropbox_obj,upload_file=True,size=(500,400),filetype='image'):
    self.local_file = local_file
    self.size = size
    self.cap = cap
    self.label = label
    self.fignum = fignum
    self.filetype=filetype

    if upload_file:
      res1 = dropbox_obj.upload_file(local_file)
    res2 = dropbox_obj.get_file_link(local_file.split('/')[-1])
    
    self.cloud_file = res2['url']
    
  def _repr_html_(self):

    if self.filetype == 'image':


      html_str = '<center><img src="%s" alt="broken link" \
                  title="Figure %s. %s. %s" height="%spx" width="%spx" />\
                  Figure %s. %s. %s </center>' %(self.cloud_file,
                                                 self.fignum, self.cap,self.label,
                                                 self.size[0],self.size[1],
                                                 self.fignum,self.label,self.cap)
    elif self.filetype == 'movie':

        
      html_str = '<center><iframe \
                  height="%s" \
                  width="%s" \
                  src="%s" \
                  frameborder="0" \
                  allowfullscreen \
                  ></iframe></center> \
                  <center>Figure %s. %s. %s</center>' %(self.size[0],self.size[1],self.cloud_file,
                                                        self.fignum, self.cap,self.label)
                  


    return html_str

  # the 'newpage' here could possibly be replace with something a bit better. 
  # I put it in because otherwise figures seem to break up text and section headings
  # in rather scrappy ways. 
  def _repr_latex_(self):

    if self.filetype == 'image':

      ltx_str = r'\begin{figure}[htbp!] \centering \vspace{20pt} \begin{center} \
                  \adjustimage{max size={0.9\linewidth}{0.9\paperheight}}{%s} \
                  \end{center}{ \hspace*{\fill} \\} \caption[%s]{%s} \label{fig:%s} \
                  \end{figure} \newpage' %(self.local_file,self.label,self.cap,self.label)

    elif self.filetype == 'movie':

      ltx_str = r'\begin{figure}[htbp!] \centering \vspace{20pt} \begin{center} \
                  \includemovie[poster,text={\small(Loading Video...)}]{6cm}{4cm}{%s} \
                  \end{center}{ \hspace*{\fill} \\} \caption[%s]{%s} \label{fig:%s} \
                  \end{figure} \newpage' %(self.local_file,self.label,self.cap,self.label)


    return ltx_str 





# JG Custom dataframe display class                                                     **(init cell)**
# -----------------------------------

class jg_df(object):

  def __init__(self,s, caption=None, show_index=True, show_columns=True,tablenum=''):

    #self._repr_html_ = s._repr_html_
    self._show_index = show_index
    self._show_columns=show_columns
    self._h = s.to_html(index=show_index,header=show_columns)
    self._tablenum = tablenum

    def fff(x): return '%1.2f' % x  # Float format function
    #remove_index=True
    self._ltx = s.to_latex(float_format=fff, index=show_index, header=show_columns)

    if caption: self.caption=caption
    elif caption is None: self.caption = 'THIS IS AN EXAMPLE CAPTION'

  def _repr_html_(self):
    #return self._h
    return '<center>%s</center> <p> <center> %s </center> .</p>' %(self._h,
    'Table %s. %s' %(self._tablenum, self.caption)) #.format(self._h)

  def _repr_latex_(self):

    _ltx = self._ltx.replace('\\toprule', '\\hline')\
                    .replace('\\midrule', '\\hline')\
                    .replace('\\bottomrule', '\\hline')

    _ltx= u'\\begin{table}[ht] \n '\
           '\\begin{center} \n '\
           + _ltx + ' \n '\
            '\caption{'+self.caption+'} \n'\
            '\\end{center} \n '\
            '\\end{table}[ht]'
    return _ltx

  @property
  def latex(self):
    return Latex(self._repr_latex_())




    
