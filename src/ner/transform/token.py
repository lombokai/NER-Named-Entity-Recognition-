from collections import Counter


class Token:
    def __init__(self, special_first=True):
        self.special_first = special_first
        self.token_vocab = {}
        self.reverse_token_vocab = {}

        self.output_vocab = {}
        self.reverse_output_vocab = {}

        self.special_token = ["<unk>", "<pad>"]
        self.special_output = ["<pad>"]

    def build_vocab(self, sentences):
        # Build vocabulary for tokens
        token_counter = Counter(token for sentence in sentences for token in sentence["tokens"])
        sorted_tokens = sorted(token_counter.keys(), key=lambda x: (-token_counter[x], x))

        if self.special_token:
            if self.special_first:
                sorted_tokens = self.special_token + sorted_tokens
            else:
                sorted_tokens = sorted_tokens + self.special_token

        self.token_vocab = {token: idx for idx, token in enumerate(sorted_tokens)}
        self.reverse_token_vocab = {idx: token for idx, token in enumerate(sorted_tokens)}

    def build_output_vocab(self, sentences):
        # Build vocabulary for NER outputs
        output_counter = Counter(token for sentence in sentences for token in sentence["ner_outputs"])
        sorted_outputs = sorted(output_counter.keys(), key=lambda x: (-output_counter[x], x))

        if self.special_output:
            if self.special_first:
                sorted_outputs = self.special_output + sorted_outputs
            else:
                sorted_outputs = sorted_outputs + self.special_output

        self.output_vocab = {token: idx for idx, token in enumerate(sorted_outputs)}
        self.reverse_output_vocab = {idx: token for idx, token in enumerate(sorted_outputs)}

    def encode(self, tokens, is_token=True):
        if is_token:
            return [self.token_vocab.get(token, self.token_vocab["<unk>"]) for token in tokens]
        else:
            return [self.output_vocab.get(token, self.output_vocab["<pad>"]) for token in tokens]

    def decode(self, indices, is_token=True):
        if is_token:
            return [self.reverse_token_vocab.get(idx, "<unk>") for idx in indices]
        else:
            return [self.reverse_output_vocab.get(idx, "<pad>") for idx in indices]