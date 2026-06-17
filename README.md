# ARIA - Automated Research & Intelligence Agent

ARIA (Automated Research & Intelligence Agent) is a modern AI-powered research companion designed for the next generation of researchers, students, innovators, and knowledge workers.

Unlike traditional search engines that simply retrieve information, ARIA functions as an autonomous research collaborator capable of discovering recent scientific literature, analyzing academic papers, identifying research gaps, generating novel ideas, and producing publication-style research documents.

Built using LangGraph, LangChain, Google Gemini Flash, Streamlit, and LaTeX, ARIA bridges the gap between information discovery and knowledge creation by transforming research topics into complete academic papers.

---

## Why ARIA?

Modern research is no longer limited by access to information—it is limited by the ability to efficiently process, analyze, and synthesize that information.

ARIA addresses this challenge by combining:

- Agentic AI Workflows
- Academic Knowledge Retrieval
- Research Paper Analysis
- Scientific Reasoning
- Automated Paper Generation
- PDF Export Pipeline

The result is a unified research environment capable of supporting the complete research lifecycle—from literature discovery to final paper generation.

---

## Features

### Literature Discovery

- Searches arXiv for recent research papers
- Retrieves metadata and PDF links
- Identifies relevant publications
- Explores emerging research trends

### Research Analysis

- Downloads academic papers
- Extracts content from PDFs
- Summarizes key findings
- Identifies limitations and future work
- Synthesizes knowledge across multiple papers

### Research Ideation

- Generates novel research directions
- Suggests unexplored opportunities
- Assists with topic selection
- Produces original research concepts

### Academic Paper Generation

Generates complete research papers including:

- Title
- Abstract
- Introduction
- Literature Review
- Methodology
- Mathematical Formulations
- Results & Discussion
- Future Work
- References

### PDF Generation

- Generates LaTeX source code
- Compiles documents using Tectonic
- Produces publication-ready PDFs
- Supports direct download from the UI

### Interactive Research Workspace

- Modern Streamlit Interface
- Chat-based workflow
- Agent-driven research assistance
- Real-time paper generation
- Session memory using LangGraph

---

## Technology Stack

### Artificial Intelligence

- Google Gemini 2.5 Flash
- LangChain
- LangGraph

### Research Sources

- arXiv API

### Document Processing

- PyPDF2
- LaTeX
- Tectonic

### Frontend

- Streamlit

### Environment

- Python 3.11+
- UV Package Manager

---

## System Architecture

```text
User
 │
 ▼
ARIA Interface (Streamlit)
 │
 ▼
LangGraph Agent
 │
 ├── Gemini 2.5 Flash
 │
 ├── arXiv Search Tool
 │
 ├── PDF Analysis Tool
 │
 └── PDF Rendering Tool
 │
 ▼
Research Paper Generation
 │
 ▼
LaTeX Compilation
 │
 ▼
PDF Export
```

---

## Installation & Setup

### Prerequisites

Before running ARIA, ensure the following software is installed.

---

### Python

ARIA requires:

```bash
Python 3.11+
```

Verify installation:

```bash
python --version
```

---

### UV Package Manager

Install UV:

```bash
pip install uv
```

Verify installation:

```bash
uv --version
```

---

### Tectonic

ARIA uses Tectonic to compile LaTeX research papers into PDFs.

Download:

https://tectonic-typesetting.github.io

Verify installation:

```bash
tectonic --version
```

Alternatively, place `tectonic.exe` inside the project root directory.

---

## Clone Repository

```bash
git clone https://github.com/<your-username>/ARIA.git
cd ARIA
```

---

## Install Dependencies

Install all required dependencies:

```bash
uv sync
```

This installs:

- LangChain
- LangGraph
- Streamlit
- Google Gemini SDK
- PyPDF2
- Requests
- Python Dotenv
- Additional project dependencies

---

## Configure Environment Variables

Create a `.env` file:

```env
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
```

Obtain your Gemini API key from:

https://aistudio.google.com

---

## Running ARIA

Launch the application:

```bash
uv run streamlit run frontend.py
```

After startup:

```text
Local URL: http://localhost:8501
```

Open the URL in your browser.

---

## How ARIA Works

### Step 1 — Research Topic Selection

Enter a research topic.

Example:

```text
Write a research paper on Prompt Engineering.
```

---

### Step 2 — Literature Discovery

ARIA searches arXiv for recent publications related to the topic.

Example:

```text
Searching arXiv for papers about Prompt Engineering...
```

---

### Step 3 — Paper Exploration

Relevant papers and PDF links are presented to the user.

Example:

```text
Recent papers found:

1. Paper A
2. Paper B
3. Paper C
```

---

### Step 4 — Research Analysis

ARIA downloads and analyzes selected papers.

The system:

- Reads PDFs
- Extracts text
- Summarizes research
- Identifies future work
- Understands methodologies

---

### Step 5 — Research Ideation

Based on analyzed literature, ARIA proposes potential research directions.

Example:

```text
Potential Research Directions:

- Adaptive Prompt Optimization
- Multi-Agent Prompt Engineering
- Domain-Specific Prompt Learning
```

---

### Step 6 — Academic Paper Generation

ARIA generates a complete academic paper using discovered literature and selected research ideas.

Generated sections include:

- Abstract
- Introduction
- Literature Review
- Methodology
- Equations
- Results
- Future Work
- References

---

### Step 7 — LaTeX Generation

The research paper is converted into structured LaTeX code.

---

### Step 8 — PDF Compilation

ARIA uses Tectonic to compile the generated LaTeX document into PDF format.

Generated files are stored inside:

```text
output/
```

---

### Step 9 — PDF Export

The completed paper becomes available for download directly from the Streamlit interface.

---

## LangGraph Workflow

ARIA uses a cyclic agent architecture.

```text
START
  │
  ▼
Agent
  │
  ├── Tool Needed?
  │
  ├── Yes ──► Tool Node
  │              │
  │              ▼
  │            Agent
  │
  └── No ───► END
```

This enables iterative reasoning, tool usage, paper analysis, and research generation.

---

## Core Components

### frontend.py

Responsible for:

- Streamlit user interface
- Chat interaction
- Displaying research outputs
- PDF download support

---

### aria_researcher.py

Responsible for:

- LangGraph workflow creation
- Gemini integration
- Tool orchestration
- Conversation memory
- Agent reasoning loop

---

### arxiv.py

Responsible for:

- Searching arXiv
- Retrieving paper metadata
- Returning PDF links
- Discovering recent research

---

### analyze_pdf.py

Responsible for:

- Downloading PDFs
- Reading academic papers
- Extracting text
- Preparing content for analysis

---

### create_pdf.py

Responsible for:

- Receiving generated LaTeX
- Compiling via Tectonic
- Generating PDF documents
- Returning PDF file paths

---

## Future Enhancements

- Vector Database Integration
- Research Knowledge Graphs
- IEEE Formatting Support
- ACM Formatting Support
- Multi-Agent Collaboration

---

## Author

### ARIA — Automated Research & Intelligence Agent

Developed by:

**Siddhi Kale**

---

## Disclaimer

ARIA is intended for educational and research assistance purposes.

Generated research papers should always be reviewed, validated, and appropriately cited before academic submission, publication, or professional use.
