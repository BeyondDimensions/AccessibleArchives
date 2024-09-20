import os
import ipfs_api
import json
from datetime import datetime, UTC
from gpt4all import GPT4All
model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.ggf")

####################################################################################
# REVISE!!!!!!!!!!!

def generate_id(file_path):
    return ipfs_api.publish(file_path)

####################################################################################

def read_markdown_file(md_path):
    with open(md_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

#####################################################################################

def categorizing_text(content, gpt):
    response = gpt.predict(f"PROMT {content}")      # put promt in, to search for specific data in the text
    return response

#####################################################################################

def transcribe(png_path, md_path):
    pass

def main():
    input_dir = "PATH I STILL HAVE TO ENTER"
    output_dir = "document_metadata.json"
    metadata = []

for filename in os.listdir(input_dir):
    if not filename.endswith(".png"):
        continue
    png_path = os.path.join(input_dir, filename)
    md_dir = os.path.join(input_dir, "transcripts")
    if not os.path.exists(md_dir):
        os.makedirs(md_dir)
    md_path = os.path.join(md_dir, filename+".md")

    json_dir = os.path.join(input_dir, "Metadata")
    if not os.path.exists(json_dir):
        os.makedirs(json_dir)
    json_path = os.path.join(json_dir, filename+".json")
    if os.path.exists(json_path):
        continue



    if not os.path.exists(md_path):
        transcribe(png_path, md_path)
    ipfs_id = generate_id(png_path)
    transcript_id = generate_id(md_path)
    category = catogorize_text(content, gpt)
    metadata.append({
        "ipfs_id": ipfs_id,
        "transcripts": [{
            "ipfs_id" : transcript_id,
            "transcriber" : "ChatGPT",
            "date" : datetime.now(UTC).strftime("%Y-%m-%d")
        }],
        "content": {

        },
        "source" : {

        }
    })

    with open(json_path, 'w+') as f:
        json.dump(metadata, f, indent=4)


if __name__ == "__main__":
    main()



    ### to dos
    ### - arbeiten mit unterordnern
    ### - GPT4all einbinden und content und source in einer extra function schreiben
    ### - make an Ordner.json to group pages together for the curation