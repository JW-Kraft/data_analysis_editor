#%%
import pandas as pd
from datatable_editor.relational_df import RelationalDf
from datatable_editor.demo_input_dict import input_dict

#%% Generate table data clean

"""
1. Provide dict of tables data
    - table_id (matching dict)
    - table_name (to be displayed in editor)
    - child tables, fk_column name
2. Prepare output_dict containing relational_dfs
    - add relational_df to output_dict for every table_name
3. Fill dataframes
    3.1 Loop through input_dict
        - detect if 
"""

main_table = 'users'
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
    'service_water_demand': {
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

output_dict = {}
for key, item in data_info.items():
    output_dict[key] = RelationalDf(key, item['table_name'], pd.DataFrame())

def read_data(data_dict, this_table_id, parent_element_id, output_dict):
    new_row = {}
    # Check if dict is nested (->
    # Loop through elements (=rows in df) in passed dict
    for element_name, element_data in data_dict.items():

        # Loop through each entry of data
        for key, data in element_data.items():

            return 
def has_nested_dict(dct):
    return any(isinstance(value, dict) for value in dct.values())
#%%
def generate_table_data(input_dict, this_table, parent_table, parent_item_id, subdata_tables, output_dict):

    # Get row_id of last element of the current output
    data = output_dict[this_table]['data']

    row_id = 0
    new_row = None

    if input_dict == {}:
        return output_dict

    for key, entry in input_dict.items():  # loop through every entry of outer dict

        if isinstance(entry, dict):  # If this entry is a dict -> multiple rows to add
            # All contents of outer dict are added to main_table
            new_row = {
                'id': row_id,  # add numeric id
                'name': key,  # add value for name
            }

            if parent_table:
                new_row[f'{parent_table}_id'] = parent_item_id

            for key, value in entry.items():  # Loop through value in sub-dict
                if key not in subdata_tables:  # This value is not an id of a sub-data table -> does not contain sub-data
                    new_row[key] = value  # Add as value to new row
                else:  # This value contains data of a sub-data table
                    output_dict[this_table]['child_tables'].append(key)  # Add to list of child data ids

                    # Get the data and add to dict
                    output_dict = generate_table_data(input_dict=value,
                                                      this_table=key,
                                                      parent_table=this_table,
                                                      parent_item_id=row_id,
                                                      subdata_tables=subdata_tables,
                                                      output_dict=output_dict)

            # Add new row to output_dict data
            output_dict[this_table]['data'].append(new_row)
            row_id = + 1

    if not isinstance(next(iter(input_dict)), dict):  # if the first item is not a dict
        # Only one row to add

        new_row = {
            'id': row_id,  # add numeric id TODO get ID from previous item
            'name': key,  # add value for name
        }

        if parent_table:
            new_row[f'{parent_table}_id'] = parent_item_id

        new_row.update(input_dict)

    # Add new row to output_dict data
    output_dict[this_table]['data'].append(new_row)

    return output_dict

subdata_ids = ['appliances', 'cooking_demands', 'drinking_water_demand', 'service_water_demands', 'agro_processing_machines']

output_dict = {'users': {'data': [], 'child_tables': []}}
for k in subdata_ids:
    output_dict[k] = {'data':[], 'child_tables':[]}

output_dict = generate_table_data(input_dict, 'users', None, None, subdata_ids, output_dict)

editor_input_dict = {}
for table_id, table_data in output_dict.items():
    editor_input_dict[table_id] = RelationalDf(table_id, table_id, pd.DataFrame(table_data['data']))
    # Remove duplicates from each elements list of child tables
    output_dict[table_id]['child_tables'] = list(set(output_dict[table_id]['child_tables']))

for table_id, table_data in output_dict.items():

    if table_data['child_tables']:
        for child_table in table_data['child_tables']:
            editor_input_dict[table_id].add_child_table(editor_input_dict[child_table], f'{table_id}_id')

print(editor_input_dict)

#%%
from datatable_editor.core import DatatableEditor

# Initiated editor object
editor = DatatableEditor(datatables=editor_input_dict, port=1000, debug=False)

# Run the editor -> will run at localhost:<specified_port>
editor.run_app()
