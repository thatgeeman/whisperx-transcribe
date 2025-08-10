You have below the transcript for a specific speaker {{ speaker }} from a conversation.

{{ context_str }}

Given the context information and without using prior knowledge, perform the following tasks based on the instructions below.

**Task**

1. Read the provided transcript that contains only segments spoken by {{ speaker }}.
2. Identify the key topics that {{ speaker }} addressed in a markdown list.
3. Organize the topics into a clear, hierarchical structure, capturing the main points raised by {{ speaker }}.
4. Finish with a short **TL;DR / Core ideas** section (less than 8 lines) that summarizes the key takeaways from {{ speaker }}'s contributions.

**Formatting rules**

- Use Markdown throughout.
- Do **not** mention these instructions in your answer.
- Use level-2 headings (`##`) for the topic list.
- In the TL;DR section, summarize the core ideas as bullet points without quoting the transcript verbatim.

**Example Output Structure**

Strictly follow the structure below for your final answer. You may add more topics if necessary, but do not change the format or headings.

```markdown
## Topic 1 Title

- Main point 1
- Main point 2
- ...

## Topic 2 Title

- Main point 1
- Main point 2
- ...

## TL;DR / Core ideas

- Key takeaway 1
- Key takeaway 2
- ...
```
