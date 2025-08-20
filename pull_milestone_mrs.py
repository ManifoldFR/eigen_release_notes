import gitlab
import os
import orjson
from dotenv import load_dotenv
from gitlab.v4.objects.merge_requests import ProjectMergeRequest

load_dotenv()

gl = gitlab.Gitlab(private_token=os.environ.get("GITLAB_API_KEY"))

EIGEN_PROJECT_ID = 15462818
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

mr_filtered_entries = []
i = 0

for mr in merge_requests:
    mr: ProjectMergeRequest
    # skip open or closed MRs
    if mr.state != "merged":
        continue
    changes = mr.changes()
    print(f"[{i: 4d}] MR #{mr.iid} - '{mr.title}' (merged at {mr.merged_at})")
    data = {key: changes[key] for key in field_names}
    data["changes"] = [m["diff"] for m in data["changes"]]
    mr_filtered_entries.append(data)
    i += 1
    # if i == 40:
    #     break

print(f"Processed {len(mr_filtered_entries)} entries.")

with open("milestone_mrs.json", "wb") as fp:
    json_data = orjson.dumps(mr_filtered_entries)
    fp.write(json_data)
