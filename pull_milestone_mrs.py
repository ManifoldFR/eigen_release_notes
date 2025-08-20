import gitlab
import os
import orjson
import re
from rich.progress import track
from dotenv import load_dotenv
from gitlab.v4.objects.merge_requests import ProjectMergeRequest

load_dotenv()

gl = gitlab.Gitlab(private_token=os.environ.get("GITLAB_API_KEY"))

EIGEN_PROJECT_ID = 15462818
comment_pattern = re.compile(r"<!--.*?-->", re.DOTALL)
project = gl.projects.get(EIGEN_PROJECT_ID)

project.pprint()
milestone = project.milestones.get(id=6059786)
merge_requests = milestone.merge_requests()

total_mrs = merge_requests.total
print(f"Milestone MRs have {total_mrs} items / {merge_requests.total_pages} pages")

field_names = [
    "iid",
    "title",
    "web_url",
    "description",
    "created_at",
    "merged_at",
    "author",
    "changes",
    "changes_count",
    "labels",
    "state",
]
author_keep_keys = {"id", "username", "name"}


def filter_dict(d: dict, keys_keep: set):
    keys = set(d.keys())
    keys_to_del = keys.difference(keys_keep)
    for key in keys_to_del:
        del d[key]


mr_filtered_entries = []
i = 0

for mr in track(merge_requests):
    mr: ProjectMergeRequest
    # skip open or closed MRs
    if mr.state != "merged":
        continue
    changes = mr.changes()
    print(f"MR #{mr.iid} - '{mr.title}' (merged at {mr.merged_at})")
    item = {key: changes[key] for key in field_names}
    filter_dict(item["author"], author_keep_keys)
    # strip multiline comment
    item["description"] = comment_pattern.sub("", item["description"]).strip()
    mr_filtered_entries.append(item)
    i += 1
    # if i == 40:
    #     break

print(f"Processed {len(mr_filtered_entries)} entries.")

with open("milestone_mrs.json", "wb") as fp:
    json_data = orjson.dumps(mr_filtered_entries)
    fp.write(json_data)
