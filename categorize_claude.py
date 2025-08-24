import anthropic
import json
import jsonl
import re
from collections import defaultdict
from rich.progress import track
from dotenv import load_dotenv
from anthropic.types import Message
from util._categorize import (
    CATEGORY_PROMPT_TPL,
    SUMMARIZE_PROMPT,
    SYSTEM_PROMPT,
    format_changed_files,
    Classif,
    write_structured_md,
)


load_dotenv()
# Initialize the Claude client using the new API interface.
client = anthropic.Anthropic()
print(f"Client API key: {client.api_key}")
print(f"Base URL: {client.base_url}")
MODEL_NAME = "claude-sonnet-4-0"
MAX_TOKENS = 256
rep_pattern = re.compile(r"<rep>(.*?)</rep>", re.DOTALL)


def summarize_and_categorize(long_description: str, changes: str, *, system_prompt=""):
    cat_prompt = CATEGORY_PROMPT_TPL.format(
        merge_request_description=long_description, changes=changes
    )
    _rep_start = "Here's your JSON:\n<rep>\n{"
    first_response: Message = client.messages.create(
        max_tokens=MAX_TOKENS,
        model=MODEL_NAME,
        system=system_prompt,
        messages=[
            {"role": "user", "content": cat_prompt},
            {"role": "assistant", "content": _rep_start},
        ],
    )
    block0 = first_response.content[0]
    rep1_text = _rep_start + block0.text
    print(rep1_text)
    json_text = rep_pattern.search(rep1_text).group(1).strip()
    print("json:", json_text)

    categorization = Classif.model_validate_json(json_text)

    resp2: Message = client.messages.create(
        max_tokens=MAX_TOKENS,
        model=MODEL_NAME,
        system=system_prompt,
        messages=[
            {"role": "user", "content": cat_prompt},
            {"role": "assistant", "content": rep1_text},
            {"role": "user", "content": SUMMARIZE_PROMPT},
        ],
    )
    short_summary = resp2.content[0].text.strip()
    return short_summary, categorization


if __name__ == "__main__":
    input_file = "eigen_mrs_with_summary.jsonl"
    categorised_mrs = {key: defaultdict(list) for key in {"supported", "unsupported"}}

    num_lines = 0
    INPUT_DATA = list(jsonl.load(input_file))
    # INPUT_DATA = INPUT_DATA[80:]
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
        # if num_lines == 10:
        #     break

    print(f"Categorized {num_lines} lines:")
    category_line_file = "categorized_mr_summaries_claude.json"
    with open(category_line_file, "w") as fp:
        json.dump(categorised_mrs, fp, indent=2)
    print(f"Saved categorised MRs to {category_line_file}")

    output_file = "changes_50_claude.md"
    write_structured_md(categorised_mrs, output_file)
