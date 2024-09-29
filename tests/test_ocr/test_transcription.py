import os
from ocr import transcribe_image


def test_transcribe_image(data_folder):
    image_path = os.path.join(data_folder, 'test.jpg')
    md_filepath = os.path.join(data_folder, 'test-output.md')

    result = transcribe_image(image_path=image_path, md_filepath=md_filepath)

    # Add assertions to verify the output
    assert result == md_filepath
