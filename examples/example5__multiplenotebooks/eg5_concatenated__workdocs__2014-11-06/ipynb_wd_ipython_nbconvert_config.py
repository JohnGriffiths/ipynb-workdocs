c = get_config()

#Export all the notebooks in the current directory to the sphinx_howto format.
c.Exporter.preprocessors = ['ipynb_wd_cherry_picking_preprocessor.CherryPickingPreprocessor']
c.NbConvertApp.writer_class = 'notebook_copy_writer.NotebookCopyWriter'
