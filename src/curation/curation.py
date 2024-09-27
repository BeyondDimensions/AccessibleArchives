import os
import ipfs_api
import json
import shutil
from datetime import datetime, UTC
from ocr.transcription import transcribe_image
from utils.utils import ensure_dir_exists
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

def curate_pngs(input_dir, output_dir,original_medium, pdf_path):
    # erstellen der output Ordner
    ensure_dir_exists(output_dir)
    output_dir_png= ensure_dir_exists(os.path.join(output_dir, "Pages"))

    output_dir_md = ensure_dir_exists(os.path.join(output_dir, "Transcripts"))

    output_dir_json = ensure_dir_exists(os.path.join(output_dir, "PageMetadata"))

    output_dir_multi = ensure_dir_exists(os.path.join(output_dir, "MultiPageDocs"))

    #####################################################################################

    png_ids = []
    metadata_ipfs_ids = []
    errors_encountered=False
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
            try:
                transcribe_image(png_path, md_path)
            except:
                errors_encountered=True
                continue
        #ipfs_id = generate_id(png_path)
        transcript_id = generate_id(md_path)
        #category = categorize_text(content, gpt)

        metadata = {
            "ipfs_id": ipfs_id,
            "transcripts": [{
                "ipfs_id" : transcript_id,
                "transcriber" : "ChatGPT-4o-2024-08-06",
                "timestamp" : datetime.now(UTC).isoformat()
            }],
            "content": {

            },
            "source" : {
                "original_medium": original_medium,
                "digitisation_date": datetime.now(UTC).isoformat(),
                "digitiser": "anonymous"
            },
            "format": "png"
        }

        with open(json_path, 'w+') as f:
            json.dump(metadata, f, indent=4)

        metadata_ipfs_id = generate_id(json_path)
        metadata_ipfs_ids.append(metadata_ipfs_id)

    if errors_encountered:
        return
        
    multi_doc_ipfs_id = generate_id(output_dir_multi)
    doc_json_path = os.path.join(output_dir_multi, multi_doc_ipfs_id+".json")

    pdf_ipfs_id = generate_id(pdf_path)
    shutil.copy(pdf_path, os.path.join(output_dir_multi, multi_doc_ipfs_id+".pdf"))

    doc_metadata = {
        "ipfs_id": multi_doc_ipfs_id,
        "pages": metadata_ipfs_ids,
        "content": {

        },
        "source": {
            
        },
        "compilations":[
            {
            "ipfs_id":pdf_ipfs_id,
            "format":"pdf",
            "compilation_date":datetime.now(UTC).isoformat(),
            "compilation_method": "merged pages and transcripts into searchable PDF"
            }
        ]
    }


    with open(doc_json_path, 'w+') as f:
        json.dump(doc_metadata, f, indent=4)


    ### to dos
    ### - arbeiten mit unterordnern
    ### - GPT4all einbinden und content und source in einer extra function schreiben
    ### - make an Ordner.json to group pages together for the curation