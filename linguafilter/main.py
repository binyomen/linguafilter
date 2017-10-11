import panflute as pf

import linguafilter.ipa as ipa

def main():
    pf.run_filters([ipa.parse])

if __name__ == '__main__':
    main()
