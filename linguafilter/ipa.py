import panflute as pf
import linguafilter.ipa_mappings as mappings

MOD_CHARS = set(['\'', '=', '`', '~'])

class Segment:
    def __init__(self, base=None, mods=None):
        self.base = base
        if mods is None:
            mods = []
        self.mods = mods

    def __eq__(self, other):
        return self.base == other.base and self.mods == other.mods

    def __str__(self):
        base = '' if self.base is None else self.base
        return '{ ' + base + ', ' + str(self.mods) + ' }'
    def __repr__(self):
        return str(self)


def get_combos(l):
    ret = []
    for elt in l:
        for i in range(len(ret)):
            new_elt = ret[i] + [elt]
            ret.append(new_elt)
        ret.append([elt])
    ret.append([])
    return sorted(ret, key=lambda e: len(e), reverse=True)

def remove_mods(mods, to_remove):
    ret_mods = []
    for mod in mods:
        if mod not in to_remove:
            ret_mods.append(mod)
    return ret_mods

def reduce_mods(mods, output_format='html'):
    combos = get_combos(mods)
    for combo in combos:
        key = tuple(sorted(combo))
        if key in mappings.MOD_MAP:
            func = mappings.MOD_MAP[key][output_format]
            return [func] + reduce_mods(remove_mods(mods, combo), output_format)
    return []

def reduce_seg(seg, output_format='html'):
    combos = get_combos(seg.mods)
    for combo in combos:
        key = (seg.base,) + tuple(sorted(combo))
        if key in mappings.BASE_MAP:
            char = mappings.BASE_MAP[key][output_format]
            mods = remove_mods(seg.mods, combo)
            return char, mods
    # unrecognized segments just get passed through
    return seg.base, seg.mods

def stringify(seg, output_format='html'):
    char, mods = reduce_seg(seg, output_format)
    mod_funcs = reduce_mods(mods, output_format)
    for func in mod_funcs:
        char = func(char)
    return char

def process_chars(chars):
    segs = []
    curr_seg = Segment()
    in_mod_mode = False
    for char in chars:
        if in_mod_mode:
            if char == '_':
                raise Exception('two underscore characters cannot appear next to each other')
            # _j and ' are equivalent
            if char == 'j':
                mod = '\''
            else:
                mod = char
            curr_seg.mods.append(mod)
            in_mod_mode = False
        else:
            if char in MOD_CHARS:
                if curr_seg.base is None:
                    raise Exception('modifier characters must appear after a base character')
                curr_seg.mods.append(char)
            elif char == '_':
                if curr_seg.base is None:
                    raise Exception('underscore characters must appear after a base character')
                in_mod_mode = True
            else:
                if curr_seg.base is not None:
                    segs.append(curr_seg)
                    curr_seg = Segment()

                # P and v\ are equivalent
                if char == 'P':
                    base = 'v\\'
                else:
                    base = char
                curr_seg.base = base
    if in_mod_mode:
        raise Exception('dangling modifier character')
    segs.append(curr_seg)
    return segs

def tokenize(s):
    chars = []
    for char in s:
        if char == '\\':
            if len(chars) == 0:
                raise Exception('backslashes can only appear after a character')
            chars[-1] += '\\'
        else:
            chars.append(char)
    return chars

def strings_to_ipa(elem, doc):
    if isinstance(elem, pf.Str):
        chars = tokenize(elem.text)
        segs = process_chars(chars)
        text = ''
        for seg in segs:
            text += stringify(seg, doc.format)
        if doc.format == 'latex':
            text = '\\textipa{' + text + '}'
        return pf.RawInline(text, format=doc.format)

def parse(elem, doc):
    if isinstance(elem, pf.Span) and 'ipa' in elem.classes:
        return elem.walk(strings_to_ipa, doc=doc)
