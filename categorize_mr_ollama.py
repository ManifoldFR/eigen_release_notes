import ollama
import jsonl
import json
import pprint
from argparse import ArgumentParser
from rich.progress import track
from mdutils.mdutils import MdUtils
from collections import defaultdict
from typing import Any, Literal
from pydantic import BaseModel

client = ollama.Client()
MODEL_NAME = "qwen3:1.7b"
CATEGORY_PROMPT = """You are a categorizer and summarizer for merge requests of a large C++ linear algebra library.

Your output is a JSON object.

JSON output field 'short_summary' is a one-line short summary, like a line in a set of release notes.
Prefer starting with a non-conjugated verb or past tense say "Fix" or "Fixed" instead of "Fixes":
<example>
  Implemented consistent default forwarding behavior for packet min/max operations with different NaN propagation modes
</example>
<example>
  Fix ARM32 float division accuracy and related numerical stability issues through improved reciprocal calculations
</example>
For documentation MRs, focus on what the documentation being changed is for, and include mention of it in the summary.

For the fields 'supported' and 'category':
You will classify the MR by support status ('supported', 'unsupported') and category ('major_changes', 'breaking_changes', 'other_improved', 'other_fixed', 'other_added', 'other_removed').
  - 'supported', 'unsupported' means whether the changes affect supported or unsupported modules respectively.
  - 'major_changes' means "Highlights big new features"
  - 'breaking_changes' means "Big breaks most users should be aware of".

Hints about unsupported modules [IMPORTANT]:
  - The related filepaths might start with `unsupported/`.
  - The Tensor module (main include `<unsupported/Eigen/CXX11/Tensor>`), and everything to do with `Eigen::Tensor`, are unsupported. Look out for the word Tensor in the title, summary, and changes.
  - The threadpool module *was* unsupported (one of the MRs moves it to core, I think #1289).
  - Look out for the word 'unsupported' in the title or summary.
  - Also look out for: EulerAngles, FFT, BVH, KroneckerProduct, SparseExtra, SpecialFunctions.

<example>
    MR #1848, "Clean up TensorDeviceThreadPool.h", touches the UNSUPPORTED module.
</example>
"""


class Classif(BaseModel):
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


def categorize(prompt: str, *, system_prompt="", prefill=""):
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
        format=Classif.model_json_schema(),
    )
    message = response.message
    return Classif.model_validate_json(message.content)


if __name__ == "__main__":
    parser = ArgumentParser("MR categorizer")
    parser.add_argument(
        "--only-markdown",
        help="Will skip categorizing and load JSON result to create Markdown file.",
    )
    args = parser.parse_args()

    input_file = "eigen_mrs_with_summary.jsonl"
    categorised_mrs = {key: defaultdict(list) for key in {"supported", "unsupported"}}

    num_lines = 0
    INPUT_DATA = list(jsonl.load(input_file))
    for line in track(INPUT_DATA, "Categorizing MRs..."):
        print(f"========== Summary (MR #{line['iid']}) ==========")
        prompt = (
            "Given the following summary of the merge request, give me the JSON response:\n"
            f"{line['summary']}"
        )

        resp = categorize(prompt, system_prompt=CATEGORY_PROMPT)
        print("Short summary:", resp.short_summary)
        print("Category:", resp.category)
        print("Supported:", resp.supported)
        line.update(resp.model_dump())
        mr_id = line["iid"]
        line_content = "[#{iid}]({url}): {summary}".format(
            iid=mr_id, url=line["web_url"], summary=resp.short_summary.capitalize()
        )
        categorised_mrs[resp.supported][resp.category].append(line_content)
        num_lines += 1
        if num_lines == 149:
            break

    print(f"Categorized {num_lines} lines:")
    pprint.pp(categorised_mrs)

    category_line_file = "categorized_mr_summaries.json"
    with open(category_line_file, "w") as fp:
        json.dump(categorised_mrs, fp, indent=2)
    print(f"Saved categorised MRs to {category_line_file}")

    output_file = "changes_50.md"
    md_file = MdUtils(output_file)
    md_file.new_header(1, "Changelog")
    md_file.new_header(level=2, title="5.0")

    def add_changes_to_md(change_set: dict[str, Any]):
        for key, sublist in change_set.items():
            title = key.capitalize().replace("_", " ")
            md_file.new_header(level=4, title=title)
            md_file.new_list(sublist)
            md_file.write("\n")

    md_file.new_header(level=3, title="Supported modules")
    add_changes_to_md(categorised_mrs["supported"])

    md_file.new_header(level=3, title="Unsupported modules")
    add_changes_to_md(categorised_mrs["unsupported"])
    print(md_file.get_md_text())
    md_file.create_md_file()
