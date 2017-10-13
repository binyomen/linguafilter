import panflute as pf

import linguafilter.common as common

def parse(elem, doc):
    if isinstance(elem, pf.Span) and 'phonrule' in elem.classes:
        content = [c for c in elem.content if not isinstance(c, common.SPACE_TYPES)]
        if len(content) != 4:
            raise Exception('invalid phonrule syntax')

        elem.content = []
        if doc.format == 'html':
            elem.content.append(content[0])
            elem.content.append(pf.Space())
            elem.content.append(pf.RawInline('-&gt;', format=doc.format))
            elem.content.append(pf.Space())
            elem.content.append(content[1])
            elem.content.append(pf.RawInline('/', format=doc.format))
            elem.content.append(content[2])
            elem.content.append(pf.RawInline('_', format=doc.format))
            elem.content.append(content[3])
        elif doc.format == 'latex':
            elem.content.append(pf.RawInline('\\phonb{', format=doc.format))
            elem.content.append(content[0])
            elem.content.append(pf.RawInline('}', format=doc.format))
            elem.content.append(pf.RawInline('{', format=doc.format))
            elem.content.append(content[1])
            elem.content.append(pf.RawInline('}', format=doc.format))
            elem.content.append(pf.RawInline('{', format=doc.format))
            elem.content.append(content[2])
            elem.content.append(pf.RawInline('}', format=doc.format))
            elem.content.append(pf.RawInline('{', format=doc.format))
            elem.content.append(content[3])
            elem.content.append(pf.RawInline('}', format=doc.format))
