import panflute as pf

import linguafilter.gloss as gloss
import linguafilter.ipa as ipa
import linguafilter.phonfeat as phonfeat
import linguafilter.phonrule as phonrule

def main():
    pf.run_filters([gloss.parse, ipa.parse, phonfeat.parse, phonrule.parse])

if __name__ == '__main__':
    main()
