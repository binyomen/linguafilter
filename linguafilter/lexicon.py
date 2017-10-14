import copy
import csv
import io
import panflute as pf

import linguafilter.common as common

def get_config(attrs):
    config = {}
    if 'file' not in attrs:
        raise Exception('filename required')
    config['file'] = attrs['file']
    if 'delim' in attrs:
        config['delimiter'] = '\t' if attrs['delim']=='\\t' else attrs['delim']
    else:
        config['delimiter'] = ','
    config['quote'] = attrs['quote'] if 'quote' in attrs else '"'
    return config

def replace_fields(fields, elem):
    if isinstance(elem, pf.Str):
        for field in fields:
            elem.text = elem.text.replace('{'+field+'}', fields[field])

def parse(elem, doc):
    if isinstance(elem, pf.Div) and 'lexicon' in elem.classes:
        config = get_config(elem.attributes)
        content = elem.content
        elem.content = []
        with io.open(config['file'], newline='') as f:
            reader = csv.DictReader(f, delimiter=config['delimiter'], quotechar=config['quote'])
            for row in reader:
                new_content = copy.deepcopy(content)
                for c in new_content:
                    func = lambda elem, doc: replace_fields(row, elem)
                    c.walk(func)
                elem.content.extend(new_content)
