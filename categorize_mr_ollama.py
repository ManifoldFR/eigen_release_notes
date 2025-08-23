import ollama
import jsonl
import json
from argparse import ArgumentParser
from rich.progress import track
from collections import defaultdict
from util._categorize import (
    SYSTEM_PROMPT,
    SUMMARIZE_PROMPT,
    CATEGORY_PROMPT_TPL,
    format_changed_files,
    Classif,
    write_structured_md,
)

client = ollama.Client()
# MODEL_NAME = "qwen3:1.7b"
MODEL_NAME = "gemma3:4b-it-qat"
# MODEL_NAME = "gemma2:2b"


MODEL_OPTIONS = {
    "think": False,
    "options": {"temperature": 0.1},
}


def summarize_and_categorize(long_description: str, changes: str, *, system_prompt=""):
    cat_prompt = CATEGORY_PROMPT_TPL.format(
        merge_request_description=long_description, changes=changes
    )
    first_response: ollama.ChatResponse = client.chat(
        MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": cat_prompt},
        ],
        **MODEL_OPTIONS,
        format=Classif.model_json_schema(),
    )
    resp1_text = first_response.message.content
    categorization = Classif.model_validate_json(resp1_text)

    resp2: ollama.ChatResponse = client.chat(
        MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": cat_prompt},
            {"role": "assistant", "content": resp1_text},
            {"role": "user", "content": SUMMARIZE_PROMPT},
        ],
        **MODEL_OPTIONS,
    )
    short_summary = resp2.message.content.strip()
    return short_summary, categorization


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
        print(line["summary"])
        print("---")
        changed_files = "".join(map(format_changed_files, line["changes"]))
        short_summary, resp = summarize_and_categorize(
            line["summary"],
            changed_files,
            system_prompt=SYSTEM_PROMPT,
        )
        print("SHORT SUMMARY:", short_summary)
        print("SUPPORTED:", resp.sup)
        print("CATEGORY:", resp.category)
        line.update(resp.model_dump())
        mr_id = line["iid"]
        line_content = "[#{iid}]({url}): {summary}".format(
            iid=mr_id, url=line["web_url"], summary=short_summary
        )
        categorised_mrs[resp.sup][resp.category].append(line_content)
        num_lines += 1
        # if num_lines == 40:
        #     break

    print(f"Categorized {num_lines} lines:")
    category_line_file = "categorized_mr_summaries.json"
    with open(category_line_file, "w") as fp:
        json.dump(categorised_mrs, fp, indent=2)
    print(f"Saved categorised MRs to {category_line_file}")

    output_file = "changes_50.md"
    write_structured_md(categorised_mrs, output_file)
