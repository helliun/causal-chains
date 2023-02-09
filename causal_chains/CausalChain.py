from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
import sentence_transformers
import torch
from tqdm import tqdm
import pydot
from IPython.display import Image, display

class util:
    def cos_sim(x,y):
        return sentence_transformers.util.cos_sim(x,y)

    def create_chunks(text,link_length=3):
        def batch(iterable, n=1):
          l = len(iterable)
          for ndx in range(0, l, n):
              yield iterable[ndx:min(ndx + n, l)]
        sentences = text.split(". ")
        chunks = [". ".join(a)+"." for a in batch(sentences, link_length)]
        chunks = [a[:500] for a in chunks]
        return chunks
    
    def data_generator(l):
        i = 0
        while i<len(l):
            yield l[i]
            i+=1

class CausalChain:
    def __init__(self,chunks=[], device="cpu"):
        self.summarizer = pipeline("summarization", model="taskload/bart-cause-effect", device=0)
        self.embmodel = SentenceTransformer('sentence-transformers/all-mpnet-base-v1').to(device)
        self.chunks = chunks
        self.chunks = [a[:500] for a in self.chunks]
        self.triggers = []
        self.effects = []
        self.outlines = []
        self.connections = {}
    
    def create_effects(self,batch_size=16):
        print("Analyzing causation...")
        output = self.summarizer(util.data_generator(self.chunks), batch_size=batch_size, max_length=100, min_length=30, do_sample=False)
        for out in tqdm(output):
            text = out[0]["summary_text"]
            self.outlines.append(text)
            trigger = text[len("Event Trigger:  "):text.find("Event Description:")].replace("\n","")
            effect = text[text.find("Event Description:")+len("Event Description: "):].replace("\n","")
            self.triggers.append(trigger)
            self.effects.append(effect)
    
    def create_connections(self,batch_size=16,chain_threshold=0.6):
        self.connections = {}
        if self.effects==[]:
          self.create_effects()
        print("Linking events...")
        trigger_embs = self.embmodel.encode(self.triggers,convert_to_tensor=True)
        effect_embs = self.embmodel.encode(self.effects,convert_to_tensor=True)

        all_cos_scores = util.cos_sim(effect_embs,trigger_embs)
        
        for n in tqdm(range(len(all_cos_scores))):
            cos_scores = all_cos_scores[n]#util.cos_sim(effect_embs[n],trigger_embs)
            best = torch.topk(cos_scores, k=len(self.triggers))
            top_indices = best[1]#[0]
            top_scores = best[0]#[0]
            top_effects = [self.effects[i] for i in top_indices if cos_scores[i] > chain_threshold]
            top_triggers = [self.triggers[i] for i in top_indices if cos_scores[i] > chain_threshold]
            top_scores = [round(cos_scores[i].item(), 3) for i in top_indices if cos_scores[i] > chain_threshold]
            for found, score in zip(top_effects, top_scores):
              if self.effects[n] != found:
                try:
                  self.connections[self.effects[n]].append((found, score))
                except:
                  self.connections[self.effects[n]] = [(found, score)]
        self.biggest_chain = []
        self.biggest_chain = self.find_biggest_chain()

    def find_chains(self, start_effect, link_length):
        chains = []
        chain = [start_effect]
        while len(chain) <= link_length:
            last_effect = chain[-1]
            try:
                next_effects = self.connections[last_effect]
                for next_effect, _ in next_effects:
                    chains.append(chain + [next_effect])
                chain = chain[1:] + [next_effect]
            except KeyError:
                break

        return chains
    
    def find_biggest_chain(self):
      max_len = 0
      biggest_chain = []
      for key in self.connections:
          chain = [key]
          current = key
          for link in self.connections[key]:
              chain.append(link[0])
              current = link[0]
              if len(chain) > max_len:
                  biggest_chain = chain
                  max_len = len(chain)
      return biggest_chain

    def view_pydot(self,pdot):
      plt = Image(pdot.create_png())
      display(plt)

    def visualize(self, chain, path='chain.png'):
      graph = pydot.Dot(graph_type='digraph', rankdir='LR')
      for effect in chain:
          node = pydot.Node(effect, style="filled", fillcolor="yellow")
          graph.add_node(node)
          if effect in self.connections:
              for connection, score in self.connections[effect]:
                if connection in chain:
                    edge = pydot.Edge(effect, connection, label=str(score))
                    graph.add_edge(edge)
      graph.write_png(path)
      self.view_pydot(graph)
