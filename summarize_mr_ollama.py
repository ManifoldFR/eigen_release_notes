import orjson
import jsonl
import ollama
import argparse
from pydantic import BaseModel
from typing import Literal

client = ollama.Client()
# MODEL_NAME = "qwen2.5:3b-instruct-q5_K_M"
# MODEL_NAME = "qwen3:4b-instruct"
MODEL_NAME = "qwen3:1.7b"

SYSTEM_PROMPT = """You are a merge request summarization and categorization assistant for a C++ linear algebra library.

Focus on the most important aspects of the MR (avoid getting lost in minor details): major code modifications (key changes), new features and improvements, impact on the codebase.
Make each section in the summary short (a few lines at most).
If any field is marked NA, exclude it from the summary.
Ensure macro names from Eigen (i.e. starting with `EIGEN_`) are formatted in backticks.
Paste the author name and MR title as they were given to you.
Break line after the section headings.

The structured summary is of the following form and has the sections:

## Title:
<title>
## Author:
<author>
## Summary
### Key Changes:
<key changes>
### Improvements:
<improvements>
### Impact:
<impact>
"""
# """
# JSON output field 'short_summary' is a one-line short summary, like a line in a set of release notes.
# Prefer starting with a non-conjugated verb or past tense say "Fix" or "Fixed" instead of "Fixes":
#   - Implemented consistent default forwarding behavior for packet min/max operations with different NaN propagation modes
#   - Fix ARM32 float division accuracy and related numerical stability issues through improved reciprocal calculations

# For the fields 'supported' and 'category':
# You will classify the MR by support status ('supported', 'unsupported') and category ('major_changes', 'breaking_changes', 'other_improved', 'other_fixed', 'other_added', 'other_removed').
#   - 'supported' or 'unsupported' means whether the changes affect supported or unsupported modules (e.g. changes to Eigen's tensor module in `<unsupported/Eigen/CXX11/Tensor>`, or the threadpools, etc).
#   - 'major_changes' means "Highlights big new features"
#   - 'breaking_changes' means "Big breaks most users should be aware of".
# """


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


def get_completion(prompt: str, *, system_prompt="", prefill=""):
    response: ollama.ChatResponse = client.chat(
        MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": prefill},
        ],
        think=False,
        options={
            "temperature": 0.0,  # deterministic
        },
    )
    return response.message


def summarize_merge_request(client: ollama.Client, mr):
    # Construct the instructions (prompt) for the summarization.
    _author = mr["author"]
    input_v = (
        "Summarize the following MR:\n"
        f"<title>{mr.get('title', 'NA')}</title>\n"
        f"<author>{_author['name']} ({_author['username']})</author>\n"
        f"<labels>{mr.get('labels', 'NA')}</labels>\n"
        f"<description>{mr.get('description', 'NA')}</description>\n"
    )

    message = get_completion(input_v, system_prompt=SYSTEM_PROMPT)
    print(f"Parsed summary for MR#{mr['iid']}:")
    summary = message.content.rstrip()
    print(summary)
    return summary


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

    print(">>>>>>>> BEGIN <<<<<<<<")
    print(">>>>>>>>>>>>>>>>>>>>>>>")

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
        summary = summarize_merge_request(client, mr)
        mr["summary"] = summary
        mr["author"] = {key: mr["author"][key] for key in ("name", "username")}
        print("-" * 60 + "\n")
        chunk.append(mr)
        count_processed += 1

        if len(chunk) % chunk_size == 0:
            append_chunk_dump(chunk)
            chunk.clear()

    # finish
    append_chunk_dump(chunk)

    print(f"Summaries saved to {output_file}")
