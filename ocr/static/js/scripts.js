function toggleFileInput() {
    var uploadOption = document.getElementById('upload_option').value;
    var uploadSection = document.getElementById('upload_section');
    var chooseSection = document.getElementById('choose_section');

    if (uploadOption === 'upload') {
        uploadSection.classList.remove('hidden');
        chooseSection.classList.add('hidden');
    } else {
        uploadSection.classList.add('hidden');
        chooseSection.classList.remove('hidden');
        populateExistingFiles();
    }
}

function populateExistingFiles() {
    var existingFileSelect = document.getElementById('existing_file');

    fetch('/list_files')
        .then(response => response.json())
        .then(data => {
            existingFileSelect.innerHTML = '';
            data.files.forEach(file => {
                var option = document.createElement('option');
                option.value = file;
                option.text = file;
                existingFileSelect.appendChild(option);
            });
        });
}
