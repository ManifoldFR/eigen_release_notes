import orjson
import jsonl
import ollama
import argparse
from pydantic import BaseModel
from typing import Literal

client = ollama.Client()
# MODEL_NAME = "qwen2.5:3b-instruct-q5_K_M"
MODEL_NAME = "qwen3:1.7b"
# MODEL_NAME = "qwen3:4b-instruct"

SYSTEM_PROMPT = """
You are a merge request summarization assistant for the Eigen C++ linear algebra template library.
Your output is a JSON object.

In the 'md_text' response field, you will return a structured and concise summary.

Identify the key changes and improvements introduced by the merge request.
Focus on the most important aspects of the MR (avoid getting lost in minor details):
   - Major code modifications (key changes), including API changes
   - New features and improvements
   - Impact on the wider codebase

If any field in the input is NA, exclude the corresponding section from the summary.
Ensure macro names from Eigen (i.e. starting with `EIGEN_`) are formatted in backticks.

The structured summary should be in the form and have the sections (and only those sections) as follows:
## Title:
<MR title>
## Author:
<author>
## Summary
### Key Changes:
<key changes>
### Improvements:
<improvements>
### Impact:
<impact>

Precise instructions:
  - paste the author name as it was given to you (as "name (username)").
  - paste the title string as it was given to you.
  - you will break line after the section headings.
  - do not include any other sections than the given ones.
---

To fill in the 'short_summary' field:
The one-line short summary (field: 'short_summary') must be like a line in a set of release notes: prefer starting with a non-conjugated verb or past tense, e.g. say "Fix" or "Fixed" instead of "Fixes":
  - Implemented consistent default forwarding behavior for packet min/max operations with different NaN propagation modes
  - Fix ARM32 float division accuracy and related numerical stability issues through improved reciprocal calculations

To fill in the 'supported', 'category' fields:
You will classify the MR by support status ('supported', 'unsupported') and category ('major_changes', 'breaking_changes', 'other_improved', 'other_fixed', 'other_added', 'other_removed').
  - 'supported' or 'unsupported' means whether the changes affect supported or unsupported modules (e.g. changes to Eigen's tensor module in `<unsupported/Eigen/CXX11/Tensor>`, or the threadpools, etc).
  - 'major_changes' means "Highlights big new features"
  - 'breaking_changes' means "Big breaks most users should be aware of".
"""


class MyResponse(BaseModel):
    md_text: str
    supported: Literal["supported", "unsupported"]
    category: Literal[
        "major_changes",
        "breaking_changes",
        "other_improved",
        "other_fixed",
        "other_added",
        "other_removed",
    ]
    short_summary: str


def summarize_merge_request(client: ollama.Client, mr):
    # Construct the instructions (prompt) for the summarization.
    _author = mr["author"]
    input_v = (
        f"Title: {mr.get('title', 'NA')}\n"
        f"Author: {_author['name']} ({_author['username']})\n"
        f"Labels: {mr.get('labels', 'NA')}\n"
        f"Description: {mr.get('description', 'NA')}\n"
    )

    response: ollama.ChatResponse = client.chat(
        MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": input_v},
        ],
        think=False,
        options={
            "num_ctx": 2048,
            "temperature": 0.0,  # deterministic
        },
        format=MyResponse.model_json_schema(),
    )
    message: ollama.Message = response.message
    meta = MyResponse.model_validate_json(message.content)
    print(f"Parsed summary for MR#{mr['iid']}:")
    summary = meta.md_text.rstrip()
    print(summary)
    print("-----")
    print("Parsed classification:")
    classif = {
        "sup": meta.supported,
        "category": meta.category,
        "summary": meta.short_summary,
    }
    print(classif)
    return summary, classif


if __name__ == "__main__":
    parser = argparse.ArgumentParser("summarizer")
    parser.add_argument("--resume-from", type=int)
    args = parser.parse_args()

    input_file = "milestone_mrs.json"
    output_file = "eigen_mrs_with_summary.jsonl"

    # Read the merge request data from input
    with open(input_file, newline="", encoding="utf-8") as fp:
        mrs = orjson.loads(fp.read())

    with open(output_file, "wb") as fp:
        # wipe out file
        pass

    print(">>>> begin <<<<")

    chunk = []
    chunk_size = 16
    count_processed = 0

    if args.resume_from is not None:
        for i, mr in enumerate(mrs):
            if mr["iid"] == args.resume_from:
                mrs = mrs[i:]
                break

    def append_chunk_dump(chunk: list):
        if len(chunk) == 0:
            print("Empty chunk. Skipping")
            return
        print(f"Appending chunk of size {len(chunk)} to file {output_file}.")
        print(f"Current total MRs processed: {count_processed}")
        print("=" * 60)
        with open(output_file, "ab") as fp:
            jsonl.dump(chunk, fp, text_mode=False, json_dumps=orjson.dumps)

    # Process each merge request to get its summary
    for i, mr in enumerate(mrs):
        mr: dict
        # if i == 12:
        #     break
        summary, classif = summarize_merge_request(client, mr)
        mr["summary"] = summary
        mr["classif"] = classif
        mr["author"] = mr["author"]["name"]
        print("-" * 60 + "\n")
        chunk.append(mr)
        count_processed += 1

        if len(chunk) % chunk_size == 0:
            append_chunk_dump(chunk)
            chunk.clear()

    # finish
    append_chunk_dump(chunk)

    print(f"Summaries saved to {output_file}")
