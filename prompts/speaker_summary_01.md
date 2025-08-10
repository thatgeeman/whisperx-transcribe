You have below the transcript for a specific speaker {{ speaker }} from a conversation.

{{ context_str }}

Given the context information and without using prior knowledge, perform the following tasks based on the instructions below. 

Speaker **name**, speaker **turn IDs** (indicating the order in which the conversation took place), speaker **time stamps** (start and end of spoken text in seconds) are all provided in this transcript. 

It is important to **pay specific attention to turn ID** since these are not back to back transcripts per speaker. A discountinuous turn ID means that there was an interruption or stop of the sentence.  

Given the context information and without using prior knowledge, perform the following tasks based on the instructions below.

**Task**

1. Use **ONLY** the provided transcript to identify the **key topics or agendas** addressed by the {{speaker}} in a markdown list.
2. Organize the topics into a clear, hierarchical structure, answering the above questions.
3. Finish with a short **TL;DR / Core ideas** section (less than 8 lines) that summarizes the key takeaways from this meeting.

**Formatting rules**

- Use Markdown throughout.
- Do **not** mention these instructions in your answer.
- Use level-2 headings (`##`) for answering the sub questions above.
- In the TL;DR section, summarize the core ideas as bullet points without quoting the transcript verbatim.

**Example Output Structure**

Strictly follow the structure below for your final answer. You may add more topics if necessary, but do not change the format.

```markdown
## Main Topics
### Topic 1 Title
- Main point 1
- Main point 2
- ...
### Topic 2 Title
- Main point 1
- Main point 2
- ...

## Key Decisions and Conclusions 
- A 
- B 
- ... 

## Unresolved matters and disagreements
- A 
- B 
- ... 
## Action items
- `Speaker A` should ...
- `Listener A` should ... 
- `Non-participant A` should ...
- ... 

## Opening and closing statements
- A 
- B 
- ... 

## TL;DR / Core ideas
- Key takeaway 1
- Key takeaway 2
- ...
```
