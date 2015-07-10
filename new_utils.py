

class cloudfiles_nb(object):
    
  def __init__(self,api_type,keys):

    self.api_type = api_type
    
    
    if api_type == 'aws': 
    
      from boto.s3.connection import S3Connection
        
      aws_key,aws_secret = keys 
      self.conn = S3Connection(aws_key, aws_secret)
        
        
        
    elif api_type == 'dropbox':
        
      from dropbox.client import DropboxClient
      from dropbox.session import DropboxSession    
 
      access_token = keys
        
      self.uploaded_files = {}
      self.client = DropboxClient(access_token)
      self.base_dir = 'workdocs-cloudfiles'        
      self.folders_list = [p['path'].replace('/%s/' %self.base_dir, '')\
                           for p in self.client.metadata(self.base_dir)['contents']]
      self.upload_file_res = {}

    
  def initialize_folder(self,folder_name):
    

    if self.api_type == 'aws':
        
      self.bucket = self.conn.create_bucket(folder_name)
      self.folder_name = folder_name
        
    
    elif self.api_type == 'dropbox':
        
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
        
        
    if self.api_type == 'aws':
        
      from boto.s3.key import Key
        
      filename = filepath.split('/')[-1]
    
      k = Key(self.bucket)
      k.key = filename
    
      k.set_contents_from_filename(filepath)        
      k.set_acl('public-read')        
      if '.png' in k.key: k.set_metadata('Contet-Type', 'image/png')
 
        
    elif self.api_type == 'dropbox':
        
      f = open(filepath, 'r')
      filename = filepath.split('/')[-1]

      newfile = '%s/%s' %(self.thisfolder,filename)
    
      # if filename alread exists, delate and replace
      #filecheck = self.client.search(self.thisfolder, filename)
      #if filecheck: del_res = self.client.file_delete(newfile)
          
      res = self.client.put_file(newfile, f, overwrite=True)
 
      return res

        

  def get_file_link(self,filename):
        

    if self.api_type == 'aws':
        
      thiskey = self.bucket.get_key(filename) 
      res = 'https://%s.s3.amazonaws.com/%s' %(self.bucket.name,filename)   
      # something for error
    
      return res


    elif self.api_type == 'dropbox':
        
      res = self.client.media('%s/%s' %(self.thisfolder,filename))['url']
      # something for error
   
      return res

  def get_nbviewer_link(self,filename):

    file_link = self.get_file_link(filename)
    nbv_pfx = 'http://nbviewer.ipython.org/urls'
    res = nbv_pfx + '/' + file_link.replace('https://', '')     

    return res

  def get_slideviewer_link(self,filename):

    file_link = self.get_file_link(filename)
    sv_pfx = 'https://slideviewer.herokuapp.com/urls'
    res = sv_pfx + '/' + file_link.replace('https://', '')
  
    return res
            

class nb_fig(object):


  
  def __init__(self, local_file,label,cap,api_obj,fignum=None,upload_file=True,
               size=(500,400),filetype='image',iframe_test=True,show_fignum=True):
    
    self.api_obj = api_obj
    self.local_file = local_file
    self.size = size
    self.cap = cap
    self.label = label
    self.fignum = fignum
    self.filetype=filetype
    self.show_fignum = show_fignum


    if self.show_fignum: fignum_str = 'Figure %s.' %fignum
    else: fignum_str = ''
    self.fignum_str = fignum_str

    from IPython.display import IFrame

    if upload_file:
      res1 = api_obj.upload_file(local_file)


    fname = local_file.split('/')[-1]
 
    res2 = api_obj.get_file_link(fname)
    
    self.cloud_file = res2
  
    # this is a hacky solution to an odd bug I have noticed, 
    # where after uploading an image (seems to be when this is 
    # repeated a few times), the displayed image is sometimes
    # not the latest uploaded image. This seems to be resolved 
    # by creating an IFrame with the dropbox link; so just do 
    # this here with a temporary one, and then delete immediately 
    if iframe_test:
      tmp = IFrame(self.cloud_file,width=500,height=500)
      del tmp
	
    
  def _repr_html_(self):

    if self.filetype == 'image':


      html_str = '<center><img src="%s" alt="broken link" \
                  title="%s %s. %s" height="%spx" width="%spx" />\
                  %s %s. %s </center>' %(self.cloud_file,
                                                 self.fignum_str,self.cap,self.label,
                                                 self.size[0],self.size[1],
                                                 self.fignum_str,self.label,self.cap)
    elif self.filetype == 'movie':

        
      html_str = '<center><iframe \
                  height="%s" \
                  width="%s" \
                  src="%s" \
                  frameborder="0" \
                  allowfullscreen \
                  ></iframe></center> \
                  <center>%s %s. %s</center>' %(self.size[0],self.size[1],
                                                        self.cloud_file,self.fignum_str,
                                                        self.label,self.cap)
                  


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
  
  

# JG Custom dataframe display class                                                  
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




    
