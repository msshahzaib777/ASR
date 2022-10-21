from os import environ, path, walk
from pocketsphinx import *
from sphinxbase import *
import fnmatch


def create_folder(path):
    """Create a folder if it doesn't already exist"""
    if not os.path.isdir(path):
        os.makedirs(path)
    return


def find_files(directory, pattern='*.raw'):
    """Recursively finds all files matching the pattern."""
    files = []
    for root, dirnames, filenames in walk(directory):
        for filename in fnmatch.filter(filenames, pattern):
            files.append(path.join(root, filename))

    # sort the list, to avoid mismatch in the output files
    files = sorted(files)

    return files


def create_decoder_ngram():
    """Create a decoder based on the Ngram language model"""
    config = Decoder.default_config()
    config.set_string('-hmm', 'ps_data/model/en-us')  # acoustic model
    config.set_string('-dict', 'ps_data/lex/turtle.dict')  # lexicon / dictionary
    config.set_string('-lm', 'ps_data/lm/turtle.lm.bin')  # language model
    decoder_ngram = Decoder(config)
    return decoder_ngram


def create_decoder_goforward():
    """Create a decoder based on the goforward custom grammar"""
    config = Decoder.default_config()
    config.set_string('-hmm', 'ps_data/model/en-us')  # acoustic model
    config.set_string('-dict', 'ps_data/lex/turtle.dict')  # lexicon / dictionary
    decoder_gofwd = Decoder(config)

    # Now we use a custom language model
    # Prepare the grammar to be used
    jsgf = Jsgf('ps_data/jsgf/goforward.jsgf')  # load the grammar file
    rule = jsgf.get_rule('goforward.move2')  # choose the rule
    fsg = jsgf.build_fsg(rule, decoder_gofwd.get_logmath(), 7.5)  # build the grammar rule
    fsg.writefile('outputs/goforward.fsg')  # write the compiled grammar rule as an external file

    # Now set the fsg grammar rule in the decoder
    decoder_gofwd.set_fsg("outputs/goforward", fsg)  # load the pre-recorded compiled grammar rule in the decoder
    decoder_gofwd.set_search("outputs/goforward")  # and set it as the grammar to use

    return decoder_gofwd

# EOF
