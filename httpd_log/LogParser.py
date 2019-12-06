import re
import pandas as pd


class LogParser(object):

    def parse_logfile(self, filepath):
        client_ip_list, http_verb_list, endpoint_list, status_code_list = [], [], [], []

        rx_dict = {
            'client_ip': re.compile(r'\b([0-9]{1,3}\.){3}[0-9]{1,3}\b'),
            'http_verb': re.compile(r'\b(GET|POST|DELETE)\b'),
            'endpoint': re.compile(r'\b([a-z]).{1,}\/[a-z]{1,}\b'),
            'status_code': re.compile(r'\b(200|302|404)\b')
        }

        with open(filepath) as f:
            for log_entry in f:
                for key, rx in rx_dict.items():
                    match = rx.search(log_entry)
                    if match:
                        if key == 'client_ip':
                            client_ip_list.append(match.group())
                        elif key == 'http_verb':
                            http_verb_list.append(match.group())
                        elif key == 'endpoint':
                            endpoint_list.append(match.group())
                        elif key == 'status_code':
                            status_code_list.append(match.group())

        features_dict = {
            'client_ip': client_ip_list,
            'http_verb': http_verb_list,
            'endpoint': endpoint_list,
            # 'status_code': status_code_list
        }

        data = self._create_dataset_from_dict(features_dict)
        return data

    def _create_dataset_from_dict(self, data):
        dataset = pd.DataFrame.from_dict(data)
        return dataset


if __name__ == '__main__':
    fp = LogParser()
    print(fp.parse_logfile('access_log'))
