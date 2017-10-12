import panflute as pf

def parse(elem, doc):
    if isinstance(elem, pf.Span) and 'phonrule' in elem.classes:
        content = [c for c in elem.content if not isinstance(c, pf.Space)]
        if len(content) != 4:
            raise Exception('invalid phonrule syntax')

        if doc.format == 'html':
            text = pf.stringify(content[0]) + ' -&gt; '
            text += pf.stringify(content[1]) + '/'
            text += pf.stringify(content[2]) + '_'
            text += pf.stringify(content[3])
        elif doc.format == 'latex':
            text = '\\phonb{' + pf.stringify(content[0]) + '}'
            text += '{' + pf.stringify(content[1]) + '}'
            text += '{' + pf.stringify(content[2]) + '}'
            text += '{' + pf.stringify(content[3]) + '}'

        elem.content = [pf.RawInline(text, format=doc.format)]
