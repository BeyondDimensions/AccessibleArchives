if True:  # stop code editors from rearranging imports
    import os
    import sys

    sys.path.append(os.path.abspath(os.path.join(
        __file__, "..", "..", "..", "src"
    )))

    from ocr.transcription import transcribe_image

transcribe_image(
    image_path="/mnt/Data/Programming/test3.jpg",
    md_filepath="/mnt/Data/Programming/test-output.md"
)
