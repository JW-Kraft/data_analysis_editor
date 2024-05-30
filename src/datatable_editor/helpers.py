#%%
import pandas as pd
from datatable_editor.relational_df import RelationalDf

def read_sub_data(data_dict, data_info, output_dict, current_table_id, current_parent_element_id=None):
    """
    Function to read data of nested dict
    - can be recursively called to read data from lower level of nested dict

    :param data_dict:
    :param data_info:
    :param output_dict:
    :param current_table_id:
    :param current_parent_element_id:
    :return:
    """

    # Loop through data_dict
    for row_name, row in data_dict.items():
        # Get this rows id -> must be passed to link potential sub-data
        if output_dict[current_table_id].df.empty:  # if it is the first row
            row_id = 0  # row_id is 0
        else:
            row_id = output_dict[current_table_id].df.index[-1] + 1  # row_id is previous' row_id + 1

        # Create dict to contain this new row's data
        new_row = {'name': row_name}

        # Check if this tables entries are linked to parents
        if current_parent_element_id is not None:
            # Add entry for foreign key column with the corresponding parent element ID
            new_row[data_info[current_table_id]['fk_column']] = current_parent_element_id

        # Loop through sub-dict of data in this row of the data_dict
        for key, item in row.items():
            if key in data_info.keys():
                print(f'Entry {key} contains sub-data')
                output_dict = read_sub_data(item, data_info, output_dict, key, row_id)

            else:
                print(f'Entry {key} contains no sub-data')
                # Add entry to new_row
                new_row[key] = str(item)

        # Turn new_row into dataframe
        new_row_df = pd.DataFrame(new_row, index=[row_id])

        if output_dict[current_table_id].df.empty:  # If it is the first row (df is empty)
            output_dict[current_table_id].df = new_row_df  # Set df to be new_row
        else:
            # Else, concat row
            output_dict[current_table_id].df = pd.concat([output_dict[current_table_id].df, new_row_df], axis=0)

    return output_dict

def nested_dict_to_editor_input(input_dict, main_table, data_info):
    """
    Converts nested dict to editor input

    :param input_dict: nested dict to be converted
    :param main_table: name (dict key) of the main table that does not have parents (to be displayed first in editor)
    :param data_info: dict containing information about the data in the following shape:
        table_id: {'table_name: (required), 'parent_table': (optional), 'fk_column': (optional)}'

    :return: dict of relational_dfs to be passed to datatable_editor to be displayed
    """
    # Preallocate dict containing relational dfs
    output_dict = {}
    for key, item in data_info.items():
        output_dict[key] = RelationalDf(key, item['table_name'], pd.DataFrame())

    # Define all parent and child tables
    for key, relational_df in output_dict.items():
        if 'parent_table' in data_info[key]:  # If this table has parent table
            # Add to relational_df
            relational_df.add_parent_table(output_dict[data_info[key]['parent_table']], data_info[key]['fk_column'])

    output_dict = read_sub_data(input_dict, data_info, output_dict, main_table)

    # Make each dataframe's index id column
    for key, item in output_dict.items():
        output_dict[key].df.insert(loc=0, column='id', value=output_dict[key].df.index)

    return output_dict
