import pandas as pd
import numpy as np

def read_asec_dictionary(filename):
    '''
    Function to parse the data dictionary text file for the 2016 March ASEC supplement to the US census. The object
    returned is a dict

    File URl: http://thedataweb.rm.census.gov/pub/cps/march/Asec2016_Data_Dict_Full.txt
    Documentation: http://www2.census.gov/programs-surveys/cps/techdocs/cpsmar16.pdf
    :param filename:
    :return:
    '''
    import re
    re.MULTILINE = True

    with open(filename) as f:
        data = f.read()

    # Since they apparently don't feel that they should maintain the same linebreak character between versions,
    # we'll strip all the carriage returns to be safe
    data = data.replace('\r', '')
    units = re.split('([a-zA-Z]*) RECORD', data)[1:]
    unit_dict = {'first_digit': {}}
    for i in range(0, len(units), 2):

        unit_name = units[i].lower()
        field_dict = {}
        fields = re.split('\nD ', units[i+1])[1:]
        fields = ['\nD ' + x for x in fields]

        for field in fields:
            header = re.findall('D .*(?:\n(?![DUV] ).*)*', field)[0]
            header_record = re.split('\s*', re.split('\n', header)[0])
            header_desc = ' '.join([x.strip() for x in re.split('\n', header)[1:]])

            d = {
                'name': header_record[1],
                'description': header_desc,
                'size': int(header_record[2]),
                'begin': int(header_record[3]),
            }
            if len(header_record) == 5:
                d['range'] = header_record[4]
            universe = re.search('U (.*)\n', field)
            if universe:
                # Drop the 'U ' and '\n' at the beginning/end, respectively
                d['universe'] = universe.group(0)[2:-1]

            values = re.findall('V\s*[-0-9][-0-9]*\s*\..*(?:\nV\s*\..*)*', field)
            v = {}
            for value in values:
                key = re.match('V\s*([-0-9]*)', value).groups(0)[0]
                description = ' '.join(re.findall('V[-0-9\s]*\.(.*)', value))
                v[key] = description
            d['values'] = v


            field_dict[d['name']] = d

        # For each of the three levels in the hierarchical data structure of ASEC,
        # i.e. household -> family -> person, there is a field with a 'begin' value
        # of 1, and 1 possible value; since this is the digit that actually determines which
        # of the three unit types the record corresponds to, it's bizarre that it
        # is listed in the data dictionary as three separate fields with only one possible
        # value each. We move this into the top level dictionary, so that, when reading
        # a record, it will be easy to do, e.g., asec_dict[asec_dict['first_digit'][first_digit]]
        # to get into the field dictionary corresponding to the right unit level.
        identifier_fields = [x for x in field_dict.values() if x['begin'] == 1]
        if len(identifier_fields) > 1:
            raise ValueError('Cannot have more than one identifier field per unit level')
        identifier_field = identifier_fields[0]
        identifier_values = identifier_field['values'].keys()
        if len(identifier_values) > 1:
            raise ValueError('Cannot have more than one identifier value per unit level')
        identifier_value = identifier_values[0]
        unit_dict['first_digit'][identifier_value] = unit_name

        unit_dict[unit_name] = field_dict
        
    return unit_dict

def read_asec_data(data_filename, data_dictionary_filename, unit_type, field_list,
                   as_df=False, limit=None):
    dd = read_asec_dictionary(data_dictionary_filename)
    field_list = [x.upper() for x in field_list]
    with open(data_filename) as f:
        counter = 0
        records = []
        for line in f:
            if limit is not None and counter > limit:
                break
            this_record = {}
            if dd['first_digit'][line[0]] == unit_type:
                for field_name in field_list:
                    field_dict = dd[unit_type][field_name]
                    begin = field_dict['begin']
                    size = field_dict['size']
                    value = line[begin-1:begin-1+size] # -1 for 1-indexing
                    if field_name in ['HSUP_WGT', 'FSUP_WGT', 'A_FNLWGT', 'A_ERNLWT', 'MARSUPWT', 'A_HRSPAY']:
                        value = float(value)/100
                    else:
                        value = int(value)
                    this_record[field_name.lower()] = value
                records.append(this_record)
            counter += 1
    if as_df:
        return pd.DataFrame(records)
    else:
        return records

def add_quantiles(df, metrics, weight='marsupwt'):
    if isinstance(metrics, str):
        metrics = [metrics]
    for metric in metrics:
        df = df.sort_values(metric)
        samp_prob = df[weight]/df[weight].sum()
        df['{}_quantile'.format(metric)] = np.cumsum(samp_prob) / samp_prob.sum()
    return df
