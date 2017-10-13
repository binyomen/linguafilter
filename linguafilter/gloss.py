import panflute as pf

import linguafilter.common as common

def parse(elem, doc):
    if isinstance(elem, pf.Span) and 'gloss' in elem.classes:
        content = [c for c in elem.content if type(c) not in common.SPACE_TYPES]
        if len(content) != 3:
            raise Exception('invalid gloss syntax')

        elem.content = []
        if doc.format == 'html':
            elem.content.append(content[0])
            elem.content.append(pf.RawInline('<br/>', format=doc.format))
            elem.content.append(content[1])
            elem.content.append(pf.RawInline('<br/>', format=doc.format))
            elem.content.append(content[2])
        elif doc.format == 'latex':
            elem.content.append(pf.RawInline('\\begin{exe}\n', format=doc.format))
            elem.content.append(pf.RawInline('\\ex\n', format=doc.format))
            elem.content.append(pf.RawInline('\\gll', format=doc.format))
            elem.content.append(pf.Space())
            elem.content.append(content[0])
            elem.content.append(pf.RawInline('\\\\\n', format=doc.format))
            elem.content.append(content[1])
            elem.content.append(pf.RawInline('\\\\\n', format=doc.format))
            elem.content.append(pf.RawInline('\\trans', format=doc.format))
            elem.content.append(pf.Space())
            elem.content.append(content[2])
            elem.content.append(pf.RawInline('\n', format=doc.format))
            elem.content.append(pf.RawInline('\\end{exe}', format=doc.format))
