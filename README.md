# topolang
A deterministic acyclic finite state automaton (DAFSA) implementation with an interface to expose its innards, for the purpose of doing topological analysis on the structures of minimal DAFSAs.

# <b class="icon-lightbulb">Preamble</b>
Yesterday, I had an interesting discussion regarding auto-categorization (of documents) problems in computational linguistics. Following the conversation, I went back to finish off a trie implementation I had been working on that morning for a customized repetative search dictionary (original meaning of dictionary).

But, my mind had already gone off to theory-land, and was determined not to let me implement this simply, and to somehow find its way back to the topic of the earlier discussion. It occurred to me that I could <i>drastically</i> compact the trie by collapsing isomorphic structures within the language (ie, this group of words can all have the same endings), but then it wouldn't be a trie anymore. So, I went searching (with the inkling this would probably be related to formal grammars, and therefore represented as some sort of FSM) and quickly discovered an implementation using... finite state machines! Particulary, deterministic acyclic finite state automata (DAFSAs). It turns out that this is actually VERY effective, and there are some decent algorithms out there for constructing minimal DAFSAs.

At this point, I realized that the structure of minimal DAFSAs could potentially be extremely useful for topological analysis of language morphologies. All the DAFSA implementations I found of course had all their innards compartmentalized, as they're primarily used as look-up mechanisms. So, I decided I should build one with an additional sub-interface to allow us to query information on the internal structural implemntation. The primary motivation for this is to provide a tool to start doing some exploratory analysis on this and go from there. I'm not sure exactly the form this is going to take yet, as their is very little published on this. In fact, on this particular topic, I could only find one paper [1]. It's a good one, and looks like it'll be a great place to start, but it appears this is a pretty fresh topic.


## references:
[1] Steinberg, B. (2013, June 6). Topological dynamics and recognition of languages. [1306.1468] Topological dynamics and recognition of languages. https://arxiv.org/abs/1306.1468. 


