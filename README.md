You Do Not Need a Vector Database
================================= 
RAG (Retrieval Augmented Generation) has become the primary method to add
"memory" to an LLM, allowing the LLM to read and reference documents from
anywhere.  Vector databases have risen in popularity as the method of choice to
find and retrieve these ocuments.  In this notebook, I’d like to make the case
that you do not need a vector database for RAG.

Blog Post [here](http://about.xethub.com/blog/you-dont-need-a-vector-database)
and Notebook [here](you_do_not_need_a_vector_database.ipynb)

To run the notebook:
Install the git-xet extension from 
[https://github.com/xetdata/xet-tools/releases/](https://github.com/xetdata/xet-tools/releases/)

```
git xet clone --lazy git@github.com:xetdata/RagIRBench.git
```

Or to clone everything:

```
git xet clone git@github.com:xetdata/RagIRBench.git
```

Memoization
-----------
We use a custom jupyter extension to memoize costly / slow computations 
(like openai calls etc). This memo is stored together with the repo. 
and makes things a lot easier to run. 

When used with git-xet extension, the lazy clone can be used
```
git xet clone --lazy git@github.com:xetdata/RagIRBench.git
```

this extension will selectively download what is needed so the entire collection
of memos do not need to be all downloaded on clone.


