You have below the transcript for a conversation between speakers.

{{ context_str }}

Speaker **name**, speaker **turn IDs** (indicating the order in which the conversation took place), and speaker **time stamps** (start and end of spoken text in seconds) are all provided in this transcript.

Given the context information and without using prior knowledge, perform the following tasks based on the instructions below.

### Tasks

1.  Use **ONLY** the provided transcript to identify all **key decisions** made and **conclusions** reached during the conversation.
2.  For each one, describe what was decided or concluded.
3.  Note the speaker(s) who articulated the final decision or conclusion.
4.  Organize the findings into a bulleted list using markdown.
5.  If no decisions were made or conclusions reached, state clearly: "No key decisions were made or conclusions reached."

### Formatting Rules

  * Use Markdown throughout.
  * Do **not** mention these instructions in your answer.
  * Use level-2 headings (`##`) for answering the sub-questions above.

### Example Output Structure

Strictly follow the structure below for your final answer. You may add more topics if necessary, but do not change the format.

```markdown
## Key Decisions and Conclusions

- **Decision:** The team will adopt the new Python library for the upcoming project.
    - **Key Speaker(s):** `Speaker A`.
    - **Justification:** [Briefly state the reason for the decision, e.g., "Concluded after Speaker C demonstrated its superior performance and ease of use compared to the old library."]
    - **Details:** 
      - [Additional bullet points that descibe the conclusion in detail ...]

- **Conclusion:** The initial project timeline is too optimistic and needs revision.
    - **Key Speaker(s):** `Speaker B`, `Speaker D`.
    - **Justification:** [Briefly state how this conclusion was reached, e.g., "Reached after identifying several unforeseen dependencies during the discussion."]
    - **Details:** 
      - [Additional bullet points that descibe the conclusion in detail ...]
```