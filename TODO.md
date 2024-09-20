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
- Solve the issue with previewing large pdfs
- Convert to pdf from markdown (tesseract combination)
- Try to host an app in the network!

### Priority
- Fix the order, (``` content ```) extraction problem, test chatgpt latest also, detect why there is blank page, send corrected pdf/md files to Marvin
- Write a virt manager scirpt to setup the app to run
- LLM Agnostic!
- Clear the GPU memory after prompt!
- Work on generating text and making it LLM agnostic (seq2seq, causal) with RAG!
- Set up RAG - vector database etc.
- Cleanup roadmap
- Preview docs?
- https://platform.openai.com/docs/guides/batch/overview
- https://platform.openai.com/docs/guides/vision
- https://openai.com/api/pricing/
- Make logging with a FLAG to detect if there is a need to log to streamlit

### Future
- Add embedding model selection and fix init database wheel spinnig
- Let a compputer automatically decide which models are suitable for the computer
- Switch from Ollama to Hugging face to run a model in the backgorund
- Use different Database like (Milvus/Qdrant/Faiss)
- Work on fine-tuning with GPU
- Work on instruction tuning - how to get over it? - selecting the context and taking it directly into the prompt

### Usefull info
- Figure out the cost of chatgpt different models: https://context.ai/compare/gpt-4o-2024-08-06/gpt-4o-mini
- LLM arena: https://lmarena.ai/
- gpt-4o-mini is the cheapest ca. 0.004$ per image but gpt-4o-2024-08-06 seems better and to be second the cheapest option ca 0.005$ per image. Chatgpt-4o-latest is more expensive ca 0.009$ (probably the same models) and slightly slower.
- Their accuracy: Comparison folder
- 5 images processed comparision: gpt-4o-2024-08-06 (seems to be the fastest - 31s) vs chatgpt-4o-latest (34s)
- 1$ for first API call
- There is no difference in cost regarding conversion
- Embedding models leaderboard: https://huggingface.co/spaces/mteb/leaderboard
- Interesting model is: dunzhang/stella_en_1.5B_v5
- https://github.com/alejandro-ao/ask-multiple-pdfs - some inspiration from?
