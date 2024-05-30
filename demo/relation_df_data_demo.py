#%% Simple demo for running Datatable editor with RelationalDfs
# See demo_data.py for definition of input data

from datatable_editor.core import DatatableEditor

# Import example data
from datatable_editor.demo_data import display_relational_dfs

# Initiated editor object
editor = DatatableEditor(datatables=display_relational_dfs, port=1000, debug=False)

# Run the editor -> will run at localhost:<specified_port>
editor.run_app()
