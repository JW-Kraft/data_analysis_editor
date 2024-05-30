#%% Simple demo running Datatable editor with nested dict as input
from datatable_editor.core import DatatableEditor
from datatable_editor.helpers import nested_dict_to_editor_input

from datatable_editor.demo_data import nested_input_data_dict

data_info = {
    'users': {
        'table_name': 'Users',
    },
    'appliances': {
        'table_name': 'Electrical Appliances',
        'parent_table': 'users',
        'fk_column': 'user_id',
    },
    'cooking_demands': {
        'table_name': 'Cooking Demands',
        'parent_table': 'users',
        'fk_column': 'user_id',
    },
    'drinking_water_demand': {
        'table_name': 'Drinking Water Demand',
        'parent_table': 'users',
        'fk_column': 'user_id',
    },
    'service_water_demands': {
        'table_name': 'Service Water Demand',
        'parent_table': 'users',
        'fk_column': 'user_id',
    },
    'agro_processing_machines': {
        'table_name': 'Agro Processing Machines',
        'parent_table': 'users',
        'fk_column': 'user_id',
    }
}

# Initiated editor object
editor = DatatableEditor(datatables=nested_dict_to_editor_input(nested_input_data_dict,'users', data_info),
                         port=1000,
                         debug=False)

# Run the editor -> will run at localhost:<specified_port>
editor.run_app()