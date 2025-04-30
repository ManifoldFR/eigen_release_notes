import csv
import json
import os
import time
from dotenv import load_dotenv
from anthropic import Anthropic
from anthropic.types import Message


load_dotenv()
# Initialize the Claude client using the new API interface.
client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)
print(f"Client API key: {client.api_key}")
print(f"Base URL: {client.base_url}")
try:
    batch_client = client.beta.messages.batches
    print("Batch API is available")
except AttributeError:
    print("Batch API is not available in your client version")

def read_csv(file_path: str):
    """Read CSV file and return a list of dictionaries."""
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)


def construct_message(mr: dict):
    input_v = ("Here are the merge request details:\n"
        f"Title: {mr.get('title_subject', 'NA')}\n"
        f"Link: {mr.get('mr_id_link', 'NA')}\n"
        f"Summary: {mr.get('summary', 'NA')}\n"
        f"Merge Date: {mr.get('merge_date', 'NA')}\n\n"
        "Output only a valid JSON object.")

    msg = {
        "role": "user",
        "content": input_v
    }
    return msg


def generate_json_for_mr(mr: dict, debug=False):
    """
    Generate a JSON object for a single merge request.

    The output JSON object has the following structure:
      {
        "#<MR_Number>": {
          "<sup>/<category>": "[#<MR_Number>](<Link>): <One line summary>"
        }
      }
    """
    system_prompt = (
        "You are a release notes categorizer for the Eigen C++ library. "
        "Given the following merge request details, output a JSON object with a single key-value pair. "
        "The key should be the merge request number prefixed with a '#' (for example, '#606'). "
        "The value in that key-value pair should be an object itself with one key, of the format '<sup>/<category>' where <sup> and <category> "
        "are described below."
        "The value corresponding to that key should be a single-line markdown summary that includes the merge request number "
        "as a markdown link (e.g., [#606](https://gitlab.com/libeigen/eigen/-/merge_requests/606)) followed by a concise description. "
        """
            To clarify, the output JSON object has the following structure:
          {
            "#<MR_Number>": {
              "<sup>/<category>": "[#<MR_Number>](<Link>): <One line summary>"
            }
          }
        where:
        - <sup> is one of: supported, unsupported.
        - <category> is one of: major_changes, breaking_changes, other_improved, other_fixed, other_added, other_removed.

        'supported' or 'unsupported' means whether the changes affect supported or unsupported modules from Eigen (e.g. Eigen/Unsupported/Tensor).
        'major_changes' means "Highlights big new features"
        'breaking_changes' means "Big breaks most users should be aware of"
        """
        "Do not include any extra text or commentary. "
    )

    msg = construct_message(mr)

    if debug:
      count = client.beta.messages.count_tokens(
          model="claude-3-5-haiku-latest",
          messages=[msg],
          system=system_prompt
      )
      print("Input tokens:", count.input_tokens)
    else:
      response: Message = client.messages.create(
          max_tokens=120,
          system=system_prompt,
          messages=[msg],
          model="claude-3-5-haiku-latest",
      )
      print(f"This request had the following usage: {response.usage}")
      data = response.content[0].text
      return data

def main():
    input_csv = "eigen_mr_summary.csv"
    output_file = "mr_release_notes.jsonl"
    bad_output_file = "mr_release_notes.txt"
    first_try = True
    # Read the CSV file containing merge request details.
    rows = read_csv(input_csv)
    rows = rows[300:600]

    with open(output_file, "a", encoding="utf-8") as outfile:
      with open(bad_output_file, "a", encoding="utf-8") as bad_outfile:
          for idx, mr in enumerate(rows, start=1):
              if first_try:
                  import pdb; pdb.set_trace()
                  first_try = False
              try:
                  debug = False
                  mr_json_str = generate_json_for_mr(mr, debug)
                  mr_json_str.replace("```json", "")
                  mr_json_str.replace("```", "")
                  if debug:
                    continue

                  # Validate that the output is valid JSON.
                  try:
                    mr_json = json.loads(mr_json_str)
                    # Write the JSON object as one line.
                    outfile.write(json.dumps(mr_json) + "\n")
                  except Exception as e:
                    print(f"Error parsing JSON for MR {idx}: {e}")
                    bad_outfile.write(f"{mr_json_str}\n")
                  print(f"Processed MR {idx}/{len(rows)}")
                  print("Output:", mr_json_str)
              except Exception as e:
                  print(f"Error processing MR {idx}: {e}")
                  import pdb; pdb.set_trace()
              sleep_time = 0.1
              if idx % 50 == 0:
                  print("Sleeping for 40s")
                  outfile.flush()
                  sleep_time = 40
              # Adjust delay if necessary to avoid rate limits.
              time.sleep(sleep_time)

    print(f"All MR release notes have been written to {output_file}")

if __name__ == "__main__":
    main()
