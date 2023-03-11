import os
from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.decoders import ByteLevel as ByteLevelDecoder
from tokenizers.normalizers import NFKC, Sequence
from tokenizers.pre_tokenizers import ByteLevel
from tokenizers.trainers import BpeTrainer
from pathlib import Path

class BPE_token(object):
    def __init__ (self):
        self.tokenizer = Tokenizer(BPE())
        self.tokenizer.normalizer = Sequence([NFKC()])
        self.tokenizer.pre_tokenizer = ByteLevel()
        self.tokenizer.decoder = ByteLevelDecoder()

    def bpe_train (self, paths):
        trainer = BpeTrainer(
            vocab_size=50000, 
            show_progress=True,  
            initial_alphabet=ByteLevel.alphabet(),
            special_tokens=[
                "<s>", 
                "<pad>",
                "</s>",
                "<unk>",
                "<mask>"
            ]
        )
        self.tokenizer.train(paths, trainer)
    
    def save_tokenizer (self, location, prefix=None):
        if not os.path.exists(location):
            os.makedirs(location)
        self.tokenizer.model.save(location, prefix)

# Tokenize our data
paths = [str(x) for x in Path("./data/text/text/").glob("**/*.txt")]
tk = BPE_token()
tk.bpe_train(paths)
save_path = './data/tokenized_data/'
tk.save_tokenizer(save_path)
