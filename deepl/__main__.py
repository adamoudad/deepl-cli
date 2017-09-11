import argparse
import locale
import sys

from deepl import translator


def print_results(result, verbose=False):
    if verbose:
        print("Translated from {} to {}".format(result["source"], result["target"]))
    print(result["translation"])

def main():
    parser = argparse.ArgumentParser(description="Translate text to other languages using deepl.com")
    parser.add_argument("-s", "--source", help="Source language", metavar="lang")
    parser.add_argument("-t", "--target", help="Target language", metavar="lang")
    parser.add_argument("-v", "--verbose", help="Print additional information", action="store_true")
    parser.add_argument("text", nargs='*')

    args = parser.parse_args()

    locale_ = locale.getdefaultlocale()
    preferred_langs = [locale_[0].split("_")[0].upper()]

    if not args.source is None:
        source = args.source.upper()
    else:
        source = 'auto'
    if not args.target is None:
        target = args.target.upper()
    else:
        target = None

    if len(args.text) == 0:
        if sys.stdin.isatty():
            print("Please input text to translate")
            while True:
                text = input("> ")
                result = translator.translate(text, source, target, preferred_langs)
                print_results(result, args.verbose)

                if result["source"] not in preferred_langs:
                    preferred_langs.append(result["source"])
                if result["target"] not in preferred_langs:
                    preferred_langs.append(result["target"])
        else:
            text = sys.stdin.read()
            result = translator.translate(text, source, target, preferred_langs)
            print_results(result, args.verbose)

    else:
        text = " ".join(args.text)
        result = translator.translate(text, source, target, preferred_langs)
        print_results(result, args.verbose)


if __name__ == "__main__":
    main()