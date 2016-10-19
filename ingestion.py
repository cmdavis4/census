def read_asec_dictionary(filename):
    import re
    re.MULTILINE = True

    with open(filename) as d:
        data = d.read()
        
        units = re.split('\n([a-zA-Z]*) RECORD\n', data)[1:]
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

