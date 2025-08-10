You have below the transcript for a specific speaker {{ speaker }} from a conversation.

{{ context_str }}

Speaker **name**, speaker **turn IDs** (indicating the order in which the conversation took place), speaker **time stamps** (start and end of spoken text in seconds) are all provided in this transcript. 

It is important to **pay specific attention to turn ID** since these are not back to back transcripts per speaker. A discountinuous turn ID means that there was an interruption or stop of the sentence.  

Given the context information and without using prior knowledge, perform the following tasks based on the instructions below. 

**Task**

1. Use **ONLY** the provided transcript to summarize the **main topics** addressed by the {{ speaker }} in a markdown list.
2. Organize the topics into a clear, consistent and hierarchical structure **without losing any detail**. 

**Formatting rules**

- Use Markdown throughout.
- Do **not** mention these instructions in your response.
- Use level-2 headings (`##`) for structuring the response. 
- To conclude, summarize the core ideas oncemore without quoting the transcript verbatim.

**Example Output Structure**

Strictly follow the structure below for your final answer. You may add more topics if necessary, but do not change the format.

```markdown
## Main Topics raised by {{ speaker }}
### Topic 1 Title
- Main point 1
- Main point 2
- ...
### Topic 2 Title
- Main point 1
- Main point 2
- ...

## Conclusion and Summary of Ideas
- A 
- B 
- ... 
```
