import os
import ipfs_api
import json
import shutil
from datetime import datetime, UTC
#from gpt4all import GPT4All
from ocr.transcription import transcribe_image
from utils.utils import ensure_dir_exists
#model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.ggf")
####################################################################################
####################################################################################


def generate_id(file_path):
    return ipfs_api.publish(file_path)

####################################################################################

def read_markdown_file(md_path):
    with open(md_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

#####################################################################################

def categorize_text(content, gpt):
    response = gpt.predict(f"PROMT {content}")      # put promt in, to search for specific data in the text
    return response

#####################################################################################

def curate_pngs(input_dir):
    # erstellen der output Ordner
    output_dir = ensure_dir_exists(os.path.abspath("curated_files"))
    output_dir_png= ensure_dir_exists(os.path.join(output_dir, "Pages"))

    output_dir_md = ensure_dir_exists(os.path.join(output_dir, "Transcripts"))

    output_dir_json = ensure_dir_exists(os.path.join(output_dir, "PageMetadata"))

    output_dir_multi = ensure_dir_exists(os.path.join(output_dir, "MultiPageDocs"))

    #####################################################################################

    png_ids = []

    for filename in os.listdir(input_dir):
        if not filename.endswith(".png"):
            continue
        original_png = os.path.join(input_dir, filename)
        ipfs_id = generate_id(original_png)
        png_ids.append(ipfs_id)
        png_path = os.path.join(output_dir_png, ipfs_id+".png")
        shutil.copy(original_png, png_path)
        
        md_path = os.path.join(output_dir_md, ipfs_id+".md")

        json_path = os.path.join(output_dir_json, ipfs_id+".json")
        if os.path.exists(json_path):
            continue

        if not os.path.exists(md_path):
            transcribe_image(png_path, md_path)
        #ipfs_id = generate_id(png_path)
        transcript_id = generate_id(md_path)
        #category = categorize_text(content, gpt)
        metadata = {
            "ipfs_id": ipfs_id,
            "transcripts": [{
                "ipfs_id" : transcript_id,
                "transcriber" : "ChatGPT",
                "timestamp" : datetime.now(UTC).strftime("%Y-%m-%d")
            }],
            "content": {

            },
            "source" : {
                "original_medium": original_medium,
                "digitisation_date": digitalisation_date,
                "digitiser": digitiser
            }
        }

        with open(json_path, 'w+') as f:
            json.dump(metadata, f, indent=4)

    ipfs_id = generate_id(output_dir_multi)

    {
        "pages": png_ids,
        "ipfs_id": ipfs_id,
        "pages": png_ids,
        "content": {

        },
        "source": {
            
        }
    }



    ### to dos
    ### - arbeiten mit unterordnern
    ### - GPT4all einbinden und content und source in einer extra function schreiben
    ### - make an Ordner.json to group pages together for the curation