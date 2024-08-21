# Lighthouse

<p align="center">
  <img src="logo.png" alt="Lighthouse logo" />
</p>

## Overview

This project involves scanning documents related to the Red Army Faction (RAF), performing Optical Character Recognition (OCR) to extract text, and fine-tuning a Large Language Model (LLM) with the extracted data. The resulting model can engage in a chat about the RAF documents. The application leverages Hugging Face for model training and selection, and Streamlit for creating a graphical user interface (GUI) that allows document preview in PDF format.

## Features

- **Document Scanning and OCR**: Converts scanned RAF documents into searchable text.
- **LLM Fine-tuning**: Utilizes the extracted text to fine-tune various LLM models.
- **Model Selection**: Allows users to choose from multiple LLM models available on Hugging Face.
- **Interactive Chatbot**: Engage in conversations with the fine-tuned LLM about RAF documents.
- **Streamlit GUI**: User-friendly interface to upload, preview documents, and chat with the LLM.

## Installation

### Prerequisites

- Python 3.10+
- Pip (Python package installer)

### Clone the Repository

```bash
git clone https://github.com/BeyondDimensions/Lighthouse.git
cd Lighthouse
```

## Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application
```bash
streamlit run app.py
```

### Fine-tuning the Model
1. Choose an LLM model from the available options on Hugging Face.
2. Start the fine-tuning process with the extracted OCR data.
3. Once fine-tuned, you can interact with the chatbot.

## Project Structure
```bash
Lighthouse/
│
├── data/
│   ├── documents
│   ├── images
│       └── logo.png
│   └── fine_tuned/
├── ocr/
│   └── ocr.py
├── utils/
│   ├── fine_tuning.py
│   ├── model_utils.py
│   └── pdf_utils.py
├── app.py
├── config.py
├── requirements.txt
├── LICENSE
└── README.md
```

## Technologies Used
- Hugging Face: For accessing and fine-tuning various LLM models.
- Streamlit: For creating an interactive web-based GUI.
- Python: Primary programming language.

## Contribution
Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Contact
For any questions or suggestions, please open an issue in the repository or contact us.
