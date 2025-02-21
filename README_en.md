我将帮你创建一个英文版的README.md。建议将其保存为 README_EN.md，以便同时保留中文版本。

```markdown:h:\AI_WORK\ai_review33\README_EN.md
# Code Architecture Analysis System

An intelligent code architecture analysis system built on LangChain and LangGraph for automated codebase structure analysis and architecture review recommendations.

## Features

- Code Structure Analysis: AST-based code structure parsing and class relationship extraction
- Vector Storage: Code snippet vectorization using ChromaDB
- UML Generation: Automatic generation of Mermaid format UML class diagrams
- Multi-dimensional Analysis: Architecture analysis from modularity, extensibility, and other dimensions
- Intelligent Review: Architecture improvement suggestions based on LLM

## Tech Stack

- LangChain: LLM application framework
- LangGraph: Workflow orchestration
- ChromaDB: Vector database
- OpenAI/Gemini: Large language model interfaces
- Tree-sitter: Code parsing

## Core Modules

### Code Analyzer
<mcfile name="code_analyzer.py" path="h:\AI_WORK\ai_review33\agents\code_analyzer.py"></mcfile>
- Tree-sitter based code AST parsing
- Code snippet processing using LangChain text splitters
- Code quality analysis through LLM

### Mermaid Generator
<mcfile name="mermaid_generator.py" path="h:\AI_WORK\ai_review33\agents\mermaid_generator.py"></mcfile>
- UML class diagram generation from code structure
- Class relationship description using Mermaid syntax

### Framework Analyzer
<mcfile name="framework_analyzer.py" path="h:\AI_WORK\ai_review33\agents\framework_analyzer.py"></mcfile>
- Multi-dimensional architecture design analysis
- Improvement recommendations

### Vector Store
<mcfile name="vector_store.py" path="h:\AI_WORK\ai_review33\vector_store.py"></mcfile>
- Code vector storage using ChromaDB
- Similar code retrieval support

## Installation & Usage

1. Install Dependencies
```bash
pip install -r requirements.txt
```

2. Configure Environment Variables
- ARK_API_KEY: OpenAI API key
- ARK_API_URL: API base URL
- GEMINI_API_KEY: Gemini API key

3. Run Analysis
```bash
python main.py
```

## Output Examples

- UML Class Diagram: Saved in docs/uml_diagram.mmd
- Architecture Analysis Report: Saved in docs/framework_analyze.md
- Code Smell Analysis: Saved in docs/smell_analyze.md

## Project Structure

```
.
├── agents/          # Analysis agent modules
├── docs/           # Analysis result documents
├── extracts/       # Code extraction tools
├── test/          # Test cases
├── main.py        # Main entry
└── requirements.txt
```

## Dependencies

- langchain >= 0.3.18
- langgraph >= 0.2.72
- chromadb >= 0.6.3
- python-dotenv >= 1.0.0

## Notes

1. Proper API key configuration is required
2. Large codebases may require extended analysis time
3. Code analysis agents process files sequentially, time and token consumption scale with code volume
4. Implementation serves as reference, main components are functional

## License

Apache License 2.0

Copyright (c) 2024 [奥格](https://github.com/jewis123)

According to Apache License 2.0 requirements, when using this project:

1. Include the original copyright notice
2. Include a copy of the Apache License 2.0
3. State changes made to the original code (if any)
4. Retain author attribution information in derivative works

For the complete license text, see: [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0)
```