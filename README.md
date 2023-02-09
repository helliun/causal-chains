# Causal Chain Extractor
This code implements a tool to extract causal chains from text by summarizing the text using the `BartCauseEffect` model from [Hugging Face Transformers](https://huggingface.com/models) and then linking the causes and effects with cosine similarity calculated using the `Sentence Transformer` model.

## Requirements
- torch
- transformers
- sentence-transformers
- tqdm
- pydot

## Usage
1. Initialize a `CausalChain` object with a list of chunks of text as input.
2. Run the `create_effects` method to get the cause and effect pairs from the text and then link the events based on cosine similarity of their embeddings.
3. Run the `visualize` method to see the largest chain.

```python
from causal_chain_extractor import CausalChain, util
import wikipedia 

text = wikipedia.page("ChristopherColumbus").content
chunks util.create_chunks(text)
cc = CausalChain(chunks)
cc.create_connections()
biggest_chain = cc.biggest_chain
cc.visualize(biggest_chain)
