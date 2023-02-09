# Causal Chain Extractor
This code implements a tool to extract causal chains from text by summarizing the text using the `bart-cause-effect` model from [Hugging Face Transformers](https://huggingface.co/taskload/bart-cause-effect) and then linking the causes and effects with cosine similarity calculated using the `Sentence Transformer` model.

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

## Methods:

The class "CausalChain" has the following methods:

1. `create_effects`: This method uses the pipeline from the transformers library to analyze the text for cause-effect relationships. The text is first split into chunks, with each chunk containing a maximum of 3 sentences. This is done to limit the output length and avoid memory issues. The pipeline then generates summaries of the cause-effect relationships in the text. The triggers and effects of these relationships are stored in separate lists.

2. `create_connections`: This method uses the SentenceTransformer from the sentence-transformers library to encode the triggers and effects generated in the create_effects method. The method then calculates the cosine similarity between the triggers and effects to determine if there is a cause-effect relationship between them. If the cosine similarity score is above a certain threshold (default is 0.6), a connection is established between the trigger and effect. The connections between triggers and effects are stored in a dictionary.

3. `find_biggest_chain`: This method finds the longest chain of cause-effect relationships in the text. It starts from an effect and follows the connections stored in the connections dictionary to find other effects that are connected to it. The method continues this process until there are no more connections or the chain reaches a certain length (default is 10). The longest chain found is stored in the biggest_chain attribute.

4. `plot_chain`: This method creates a graph of the biggest chain found in the find_biggest_chain method. The graph is created using the pydot library and is saved as a .png file.

5. display_chain: This method displays the graph created in the plot_chain method.

## Example Usage:

```python
from causal_chain_extractor import CausalChain, util
import wikipedia 

text = wikipedia.page("ChristopherColumbus").content
chunks util.create_chunks(text)
cc = CausalChain(chunks,device=0)
cc.create_connections()
biggest_chain = cc.biggest_chain
cc.visualize(biggest_chain)
```python

![gif](Untitled_presentation_-_Google_Slides_-_Brave_2023-01-24_20-01-37_AdobeExpress.gif)

