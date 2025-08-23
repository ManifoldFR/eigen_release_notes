import orjson
import jsonl
import ollama
import argparse
import re
from rich.progress import track

client = ollama.Client()
# MODEL_NAME = "qwen3:4b-instruct"
MODEL_NAME = "qwen3:1.7b"

thinking_pattern = re.compile(r"<think>.*?</think>", re.DOTALL)

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


def format_paths(diff):
    """Format high-level changed file info."""
    # from pprint import pformat
    # diff = {
    #     key: diff[key]
    #     for key in ["new_path", "old_path", "new_file", "renamed_file", "deleted_file"]
    # }
    s = "<change>\n"
    if diff["deleted_file"]:
        s += f"  DELETED file {diff['old_path']}"
    elif diff["new_file"]:
        s += f"  ADDED FILE {diff['new_path']}"
    elif diff["renamed_file"]:
        s += f"  RENAMED FILE {diff['old_path']} to {diff['new_path']}"
    else:
        s += f"  MODIFIED FILE {diff['old_path']}"

    # s += pformat(diff, indent=2)
    s += "\n</change>"
    return s


def summarize_merge_request(mr):
    # Construct the instructions (prompt) for the summarization.
    _author = mr["author"]
    input_v = (
        "Summarize the following MR:\n"
        f"<title>{mr.get('title', 'NA')}</title>\n"
        f"<author>{_author['name']} ({_author['username']})</author>\n"
        f"<labels>{mr.get('labels', 'NA')}</labels>\n"
        f"<description>{mr.get('description', 'NA')}\n</description>\n"
    )
    input_v += "<changes>\n"
    for diff in mr["changes"]:
        input_v += format_paths(diff)
    input_v += "\n<changes>\n"

    message = get_completion(input_v, system_prompt=SYSTEM_PROMPT)
    print(f"Parsed summary for MR#{mr['iid']}:")
    summary = message.content.strip()
    summary = thinking_pattern.sub("", summary).strip()

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
    print(">>>>>>>> MODEL NAME: {}".format(MODEL_NAME))
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
    i = 0
    for mr in track(mrs, "Summarizing MRs..."):
        mr: dict
        # if i == 12:
        #     break
        summary = summarize_merge_request(mr)
        mr["summary"] = summary
        mr["author"] = {key: mr["author"][key] for key in ("name", "username")}
        print("-" * 60 + "\n")
        chunk.append(mr)
        count_processed += 1

        if len(chunk) % chunk_size == 0:
            append_chunk_dump(chunk)
            chunk.clear()
        i += 1

    # finish
    append_chunk_dump(chunk)

    print(f"Summaries saved to {output_file}")
