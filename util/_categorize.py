import typing
from mdutils.mdutils import MdUtils
from typing import Any, Literal
from pydantic import BaseModel

SYSTEM_PROMPT = "You are a technical assistant that analyzes Eigen library merge requests. You provide precise, factual responses based only on the information given."

CATEGORY_PROMPT_TPL = """
Analyze this Eigen library merge request and categorize it.

Input:
<description>
{merge_request_description}
</description>

<changed-files>
{changes}
</changed-files>

STEP 1: Identify what is being changed.
Look for file paths, class names, or module names mentioned in the input.

STEP 2: Determine module type ('sup'):
- 'unsupported': ONLY if the changes are ONLY to:
  * Files containing "Tensor" in the name (TensorRef, TensorBase, etc.)
  * Files in unsupported/ directory
  * FFT, BVH, SparseExtra, or KroneckerProduct modules
- 'supported': If the MR touches anything else including:
  * CI and CMake (build) files (like `CMakeLists.txt`)
  * Documentation infrastructure
  * Core Eigen modules (files in `Eigen/...`, `Eigen/src/Core`)
  * General fixes

STEP 3: Determine change type ('category'):
- 'other_fixed': Fixes bugs, warnings, or broken functionality
- 'other_improved': Improves existing features
- 'other_added': Adds new features
- 'other_removed': Removes features
- 'major_changes': Major behavior changes
- 'breaking_changes': Breaks compatibility

Return valid JSON output with the keys 'sup' and 'category', between tags <rep></rep>.
Do not return anything else than the JSON.
"""

SUMMARIZE_PROMPT = """
Good. Now write a 1-2 line summary of this merge request that:
1. Starts with an action verb matching your categorization
2. Mentions the specific component affected
3. Briefly explains what was done

Just return the summary as plain text.
"""


def format_changed_files(diff: dict):
    s = "<change>\n"
    if diff["deleted_file"]:
        s += f"  Deleted {diff['old_path']}"
    elif diff["new_file"]:
        s += f"  Added {diff['new_path']}"
    elif diff["renamed_file"]:
        s += f"  Renamed {diff['old_path']} to {diff['new_path']}"
    else:
        s += f"  Modified {diff['old_path']}"
    s += "\n</change>\n"
    return s


CategoryType = Literal[
    "breaking_changes",
    "major_changes",
    "other_improved",
    "other_fixed",
    "other_added",
    "other_removed",
]


class Classif(BaseModel):
    sup: Literal["supported", "unsupported"]
    category: CategoryType


def write_structured_md(categorised_mrs, output_file: str):
    md_file = MdUtils(output_file)
    md_file.new_header(1, "Changelog")
    md_file.new_header(level=2, title="5.0")

    def add_changes_to_md(change_set: dict[str, Any]):
        for key in typing.get_args(CategoryType):
            sublist = change_set[key]
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
