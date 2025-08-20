import orjson
import jsonl
import anthropic
from dotenv import load_dotenv
from anthropic.types import Message
# from datetime import datetime

# Set your API key for the model provider
load_dotenv()
client = anthropic.Anthropic()
print(f"Client API key: {client.api_key}")
print(f"Base URL: {client.base_url}")

CLAUDE_MODEL = "claude-3-7-sonnet-latest"
SYSTEM_PROMPT = """
You are a summarization assistant for the Eigen C++ linear algebra template library. Summarize the following merge request.
If any field in the input is marked as NA, do not include it in the summary.

Identify the key changes and improvements introduced by this merge request.
Focus on the most important aspects of the MR (avoid getting lost in minor details):
   - Major code modifications (key changes)
   - New features or functionality
   - Bug fixes or performance improvements
   - Changes to existing APIs or interfaces

Make each section quick and concise, but give comprehensive understanding of the MR's purpose and impact.

Then, finish by providing a one-line summary and a classification of the MR.
This must be valid JSON separated from the rest with "---".
The one-line summary must be like a line in a set of release notes; prefer starting with a non-conjugated verb or past tense, e.g. say "Fix" or "Fixed" instead of "Fixes":
<example>
    Implemented consistent default forwarding behavior for packet min/max operations with different NaN propagation modes
</example>
<example>
    Fix ARM32 float division accuracy and related numerical stability issues through improved reciprocal calculations
</example>
You will classify the MR by support status ('supported', 'unsupported') and category ('major_changes', 'breaking_changes', 'other_improved', 'other_fixed', 'other_added', 'other_removed').
  - 'supported' or 'unsupported' means whether the changes affect supported or unsupported modules (e.g. changes to Eigen's tensor module in `<unsupported/Eigen/CXX11/Tensor>`, or the threadpools, etc).
  - 'major_changes' means "Highlights big new features"
  - 'breaking_changes' means "Big breaks most users should be aware of".

Ensure macro names from Eigen (i.e. starting with `EIGEN_`) are in formatted in backticks.

The summary must be organized as follows:
## Authors:
## Summary
### Key Changes:
### Improvements:
### Impact:
---
{"sup": <support-status>, "category": <category>, "summary": <one-line-summary>}
"""


def summarize_merge_request_with_claude(client, mr):
    # Construct the instructions (prompt) for the summarization.
    _author = mr["author"]
    input_v = (
        f"Title: {mr.get('title', 'NA')}\n"
        f"Description: {mr.get('description', 'NA')}\n"
        f"Author: {_author['name']}\n"
        f"Merge Date: {mr.get('merged_at', 'NA')}\n"
        f"Labels: {mr.get('labels', 'NA')}"
    )

    response = client.messages.with_raw_response.create(
        max_tokens=480,
        model=CLAUDE_MODEL,
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": input_v}],
    )
    headers = response.headers
    tokens_remaining = headers.get("anthropic-ratelimit-output-tokens-remaining'")
    requests_remaining = headers.get("anthropic-ratelimit-requests-remaining")
    reset_time = headers.get("anthropic-ratelimit-requests-reset")
    print("Rate limit:")
    print(
        f" - Remaining requests: {requests_remaining}\n"
        f" - Tokens remaining: {tokens_remaining}\n"
        f" - Reset time: {reset_time}\n"
    )
    # reset_dt = datetime.fromisoformat(reset_time)
    message: Message = response.parse()
    summary = message.content[0].text
    summary, classif = summary.split("---")
    return summary, orjson.loads(classif), message.usage


if __name__ == "__main__":
    input_file = "milestone_mrs.json"
    output_file = "eigen_mrs_with_summary.json"

    # Read the merge request data from input
    with open(input_file, newline="", encoding="utf-8") as fp:
        mrs = orjson.loads(fp.read())

    with open(output_file, "wb") as fp:
        # wipe out file
        pass

    print(">>>> begin <<<<")

    import random

    random.shuffle(mrs)
    chunk = []
    chunk_size = 3
    count_processed = 0

    def append_chunk_dump(chunk: list):
        if len(chunk) == 0:
            print("Empty chunk. Skipping")
            return
        print("=" * 60)
        print(f"Appending chunk of size {len(chunk)} to file {output_file}.")
        print(f"Current total MRs processed: {count_processed}")
        with open(output_file, "ab") as fp:
            jsonl.dump(chunk, fp, text_mode=False, json_dumps=orjson.dumps)

    # Process each merge request to get its summary
    for i, mr in enumerate(mrs):
        mr: dict
        if i == 12:
            break
        summary, classif, usage = summarize_merge_request_with_claude(client, mr)
        mr["summary"] = summary
        mr["classif"] = classif
        mr["author"] = mr["author"]["name"]
        print(f"Summary for MR {mr.get('iid', 'NA')}:\n{mr['summary']}")
        print("classif:", classif)
        print(">>> usage <<<<")
        print(usage.model_dump_json(indent=2))
        print("-" * 60 + "\n")
        chunk.append(mr)
        count_processed += 1

        if len(chunk) % chunk_size == 0:
            append_chunk_dump(chunk)
            chunk.clear()

    # finish
    append_chunk_dump(chunk)

    print(f"Summaries saved to {output_file}")
