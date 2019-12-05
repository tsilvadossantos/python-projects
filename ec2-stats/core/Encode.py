from File import File
import json
import yaml

class Encode(object):

    def __init__(self, file_path, aws_regions):
        if config_file != None:
            self.config_file = config_file
        self.encode = {}

    def set_encode(self, outer_label, inner_data):
        self.encode[outer_label].append(inner_data)

    def get_encode(self):
        return self.encode

    def json_dump_model(self, f_id, f_desc, f_name, f_mdate):
        inner_data = {}
        self.encode = {'file_descriptor': []}
        for id_key, id_value in f_id.items():
            inner_data = {}
            inner_data = {'file_id' : id_value, 'description' : f_desc[id_value], 'file' : f_name[id_value], 'modified_date' : f_mdate[id_value]}
            self.set_encode('file_descriptor', inner_data)
        jdump = (json.dumps(self.get_encode(), indent=4))
        return jdump
