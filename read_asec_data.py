from ingestion import read_asec_dictionary

asec_dict = read_asec_dictionary('asec2016_dd.txt')

with open('asec2016_pubuse_v2.dat') as f:
    records = []
    counter = 0
    for line in f:
        if counter > 10:
            break
        unit_type = asec_dict['first_digit'][line[0]]
        this_record = {}
        for (field_name, field_dict) in asec_dict[unit_type].items():
            begin = field_dict['begin']
            size = field_dict['size']
            this_record[field_name] = line[begin-1:begin-1+size] # -1 for 1-indexing

        records.append(this_record)
        counter += 1

    print(records)
