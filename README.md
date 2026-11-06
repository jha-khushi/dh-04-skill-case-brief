# Assignment 04: Creating a SKILL for an LLM: Indian Case-Brief Writer

[SKILL.md](SKILL.md) teaches an LLM to write structured case briefs of Indian Supreme Court and High Court judgments. It works only from the judgment text it is given, keeps the majority separate from any dissent, and must not invent a quotation, paragraph number or citation.

## Example

| File | What it is |
|---|---|
| [examples/request.md](examples/request.md) | The request given to the LLM |
| [examples/govind_judgment.pdf](examples/govind_judgment.pdf) | The judgment: *Govind v. State of Madhya Pradesh* (1975), Indian Kanoon text |
| [examples/govind_brief.md](examples/govind_brief.md) | The brief the LLM wrote with this skill |

The example brief was written by an LLM (Claude) following SKILL.md, and I checked it against the judgment. All 9 quotations in it appear word for word in the judgment:

```bash
python check_quotes.py examples/govind_brief.md examples/govind_judgment.pdf
# 9 of 9 quotations found word for word in the judgment.
```

## How to use the skill

**In the browser (easiest).** The [Assignment 04 page](https://jha-khushi.github.io/digital-humanities-website/assignment-04.html#run-the-skill) has a *Run the skill* section: pick the judgment and options, copy the full prompt into any chatbot with the judgment PDF, then paste the brief back to check its quotations.

**Any AI chatbot (simplest, works anywhere).** Open ChatGPT, Gemini or Claude. Paste the whole of SKILL.md as your first message, with "Follow these instructions for the rest of this chat." Then upload a judgment PDF and ask, for example: "Brief this judgment, focusing on the right to privacy."

**Claude.ai as a Skill.** Put SKILL.md in a folder named `indian-case-brief-writer`, zip the folder, and upload it under Settings → Capabilities → Skills (if Skills are available on your plan). In a new chat, attach the judgment and ask for a brief; Claude loads the skill on its own.

**Claude Code.** Copy the folder to `~/.claude/skills/indian-case-brief-writer/` and ask for a brief in a session where the judgment PDF is available.

**Then check the brief.** Save the answer as `brief.md` and run `python check_quotes.py brief.md judgment.pdf` (needs `pdftotext`, from Poppler). Any quotation marked NOT FOUND has to be fixed or removed.

## Limitations

- I have tested the skill on one full judgment (*Govind*, 1975). It still needs testing on more judgments, including long ones with several opinions.
- It cannot check a citation or a later case that is not in the text it is given; it marks those *to be verified*.
- Different chatbots follow instructions differently, so every brief still needs a person to read it against the judgment.

---

**Khushi Jha** · MA Digital Humanities · Department of Humanities and Social Sciences, IIT (ISM) Dhanbad · Monsoon Semester 2026
Portfolio: https://jha-khushi.github.io/digital-humanities-website/
