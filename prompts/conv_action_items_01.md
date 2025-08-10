You have below the transcript for a conversation between speakers.

`{{ context_str }}`

Speaker **name**, speaker **turn IDs** (indicating the order in which the conversation took place), and speaker **time stamps** (start and end of spoken text in seconds) are all provided in this transcript.

Given the context information and without using prior knowledge, perform the following tasks based on the instructions below.

### Tasks

1.  Use **ONLY** the provided transcript to identify all **action items** that were assigned.
2.  For each action item, specify **who** it was assigned **to** and **by whom**.
3.  Pay specific attention to any **deadlines** or dates mentioned in relation to the action item.
4.  Organize the findings into a clear, bulleted list using markdown.
5.  If no action items were assigned, state clearly: "No action items were assigned."

### Formatting Rules

  * Use Markdown throughout.
  * Do **not** mention these instructions in your answer.
  * Use level-2 headings (`##`) for answering the sub-questions above.

### Example Output Structure

Strictly follow the tabular structure below for your final answer. You may add more rows if necessary, but do not change the format.

```markdown
## Action Items

| #   | Action item | Assigned by | Assigned to | Due Date |
| --- | ----------- | ----------- | ----------- | -------- |
|     |             |             |             |          |
|     |             |             |             |          |
|     |             |             |             |          |
|     |             |             |             |          |
```
