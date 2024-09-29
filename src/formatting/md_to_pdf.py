import os
import tempfile
import subprocess
from utils import logger


# TODO Order of putting md into pdfs need to be fixed
def convert_markdown_to_pdf(markdown_folder, pdf_output_path):
    """Convert all Markdown files in a folder to a single PDF using Pandoc with each file on a separate page."""
    markdown_files = [os.path.join(markdown_folder, f) for f in sorted(
        os.listdir(markdown_folder)) if f.endswith('.md')]

    if not markdown_files:
        logger.warning("No Markdown files found to convert.")
        return

    try:
        # Create a temporary file to store the combined Markdown content
        with tempfile.NamedTemporaryFile(delete=False, suffix='.md') as temp_md_file:
            temp_md_path = temp_md_file.name

            with open(temp_md_path, 'w') as outfile:
                for md_file in markdown_files:
                    with open(md_file, 'r') as infile:
                        outfile.write(infile.read())
                        # Add a page break between files
                        outfile.write('\n\n\\newpage\n\n')

        # Build the Pandoc command with margin options
        pandoc_command = [
            'pandoc', '-s', '--pdf-engine=xelatex', '--variable', 'geometry:margin=1in',
            temp_md_path, '-o', pdf_output_path
        ]

        # Execute Pandoc command
        subprocess.run(pandoc_command, check=True)

        logger.success(f"PDF generated successfully: {pdf_output_path}")

    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to convert Markdown to PDF: {e}")

    finally:
        # Clean up the temporary file
        if temp_md_path and os.path.exists(temp_md_path):
            os.remove(temp_md_path)
