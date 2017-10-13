import panflute as pf

def parse(elem, doc):
    if isinstance(elem, pf.Span) and 'phonfeat' in elem.classes:
        content = [c for c in elem.content if not isinstance(c, pf.Space)]

        elem.content = []
        if doc.format == 'html':
            elem.content.append(pf.RawInline('[', format=doc.format))
            for i in range(len(content)):
                elem.content.append(content[i])
                if i < len(content)-1:
                    elem.content.append(pf.RawInline(',', format=doc.format))
                    elem.content.append(pf.Space())
            elem.content.append(pf.RawInline(']', format=doc.format))
        elif doc.format == 'latex':
            elem.content.append(pf.RawInline('\\phonfeat{', format=doc.format))
            for i in range(len(content)):
                elem.content.append(content[i])
                if i < len(content)-1:
                    elem.content.append(pf.Space())
                    elem.content.append(pf.RawInline('\\\\', format=doc.format))
                    elem.content.append(pf.Space())
            elem.content.append(pf.RawInline('}', format=doc.format))
