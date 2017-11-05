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
    config['merge_root'] = 'merge_root' in attrs

    return config

def replace_fields(fields, elem):
    if isinstance(elem, pf.Str):
        for field in fields:
            elem.text = elem.text.replace('{'+field+'}', fields[field])

def parse(elem, doc):
    if isinstance(elem, pf.Div) and 'lexicon' in elem.classes:
        config = get_config(elem.attributes)
        if config['merge_root']:
            if len(elem.content) != 1:
                raise Exception('if merge_root is specified, there can be only one node under the lexicon div')
            content = elem.content[0].content
            elem.content[0].content = []
        else:
            content = elem.content
            elem.content = []
        with io.open(config['file'], newline='') as f:
            reader = csv.DictReader(f, delimiter=config['delimiter'], quotechar=config['quote'])
            for row in reader:
                for c in content:
                    # don't copy parent, because otherwise it will copy the
                    # entire document or some nonsense
                    old_parent = c.parent
                    c.parent = None
                    new_c = copy.deepcopy(c)
                    c.parent = old_parent
                    new_c.parent = old_parent

                    func = lambda elem, doc: replace_fields(row, elem)
                    new_c.walk(func)
                    if config['merge_root']:
                        elem.content[0].content.append(new_c)
                    else:
                        elem.content.append(new_c)
