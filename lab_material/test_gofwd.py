
from my_functions import create_decoder_ngram, create_decoder_goforward


# Define the path of the file to process
file_path = 'ps_data/example/goforward.raw'

# Instantiate the decoder
decoder = create_decoder_ngram()  # use the N-gram language model
#decoder = create_decoder_goforward()  # use the custom grammar

# Start the decoder
decoder.start_utt()

# Open the file to decode
stream = open(file_path, 'rb')
uttbuf = stream.read(-1)

# Process the file with the decoder
if uttbuf:
    decoder.process_raw(uttbuf, False, True)
else:
    print("Error reading speech data")
    exit()
decoder.end_utt()

# test for empty hypothesis and replace the output with an empty string if needed
if decoder.hyp() is None:
    best_hypothesis = ''
else:
    best_hypothesis = decoder.hyp().hypstr

# Print the results
print('Best hypothesis: ', best_hypothesis,
      "\n model score: ", decoder.hyp().best_score,
      "\n confidence: ", decoder.get_logmath().exp(decoder.hyp().prob))

print('Best hypothesis segments: ', [seg.word for seg in decoder.seg()])

# Access N best decodings
N = 8
print('Best ' + str(N) + ' hypothesis: ')
for best, i in zip(decoder.nbest(), range(N)):
    print(best.hypstr, best.score)
