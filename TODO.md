# TODO

## Luke
- Make a wider pdf viewer
- Make it portable (webUI + desktopApp) - work on PyInstaller standalone app
- Compare hugging face to langchain - which is better?
- Write Readme and create a logo of lighthouse with AI
- Sell GPUs and set up the LLM dedicated machine
- Put documents on NAS
- Improve GUI and to clear the messages while changing model
- Look through ChatGPT if I left any usefull information there
- Input changes into github boards!
- LLM Agnostic!
- Clear the GPU memory after prompt!
- Work on generating text and making it LLM agnostic (seq2seq, causal) with RAG!
- Save documents to (Latex, markdown with custom alignment or plaintext with manual spacing)
- Set up RAG - vector database etc.
- Solve the issue with previewing large pdfs
- Convert to pdf from markdown (tesseract combination)
- Keep track of which documents have alredy been processed (if something goes wrong in the script)
- Do not save the original images, but only the compressed ones, or neither of them?
- Prompt adjustments: "Please extract and transcribe all visible text and formatting from the following image. The output should be in fully formatted markdown. Use appropriate markdown syntax to represent headings, tables, lists, and any other formatting present in the image. Do not include any introductory or explanatory text, just return the markdown content." - clarily that if it needs to correct something let hi mdo it?

### Priority
- Extract everything in between ```markdown
- Try to host an app in the network!
- Convert to one pdf the markdown files in data/transcripts/pdfs and also create transcripts/markdown
- Image to grayscale, compression - figure out the costs - use pngs and lossless compression? Why it raises size? COLOR_RGB2GRAY OR COLOR_BGR2GRAY

### Future
- Work on fine-tuning with GPU
- Work on instruction tuning - how to get over it? - selecting the context and taking it directly into the prompt

### Usefull info
- Figure out the cost of chatgpt different models: https://context.ai/compare/gpt-4o-2024-08-06/gpt-4o-mini
- gpt-4o-mini is the cheapest ca. 0.004$ per image but gpt-4o-2024-08-06 seems better and to be second the cheapest option - compare to chatgpt-4o-latest (probably the same models)
- Their accuracy: Comparison folder
