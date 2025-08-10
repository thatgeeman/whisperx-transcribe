You have below the transcript for a conversation between speakers.

`{{ context_str }}`

Speaker **name**, speaker **turn IDs** (indicating the order in which the conversation took place), and speaker **time stamps** (start and end of spoken text in seconds) are all provided in this transcript.

Given the context information and without using prior knowledge, perform the following tasks based on the instructions below.

### Tasks

1.  Use **ONLY** the provided transcript to generate a concise summary of the meeting's most important takeaways.
2.  The summary should synthesize the main decisions, conclusions, and outcomes of the conversation.
3.  The final output must be presented under a single heading and **must not exceed 8 lines**.
4.  If the conversation is too short or lacks substantive content for a summary, state clearly: "A summary could not be generated due to insufficient content."

### Formatting Rules

  * Use Markdown throughout.
  * Do **not** mention these instructions in your answer.
  * The only output should be a level-2 heading (`##`) and the summary text.

### Example Output Structure

Strictly follow the structure below for your final answer. The entire response should only contain the following.

```markdown
## TL;DR / Core Ideas

The team approved the Q3 budget but decided to revise the marketing allocation for the "Phoenix" project. The project launch is now set for early Q4 2025. Key next steps involve finalizing the project scope, with a draft due from `Speaker C` by next week. The discussion on the annual offsite event was postponed. `Speaker A` will follow up with new proposals.
```