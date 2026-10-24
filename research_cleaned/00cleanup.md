# Research Directory Guide

This directory contains the exploratory work, computational analyses, mathematical investigations, supporting data, and results associated with this project. It is organized by **research topic**, with each topic containing its own code, figures, proofs, data, and notes as applicable.

The purpose of this structure is to make the research traversable, reproducible, and understandable without requiring every exploratory script or research note to be polished into a formal publication. The capstone paper serves as the polished presentation of the research; this directory preserves the supporting work behind it.

## Directory Structure

```text
research/
├── README.md
├── algorithm_comparison/
│   ├── README.md
│   ├── code/
│   ├── data/       # When applicable
│   ├── figures/
│   ├── proofs/     # When applicable
│   └── notes/      # When applicable
├── game_analysis/
│   ├── README.md
│   ├── code/
│   ├── data/
│   ├── figures/
│   ├── proofs/     # When applicable
│   └── notes/      # When applicable
├── mathematical_analysis/
│   ├── README.md
│   ├── code/
│   ├── data/       # When applicable
│   ├── figures/
│   ├── proofs/
│   └── notes/      # When applicable
├── asymptotic_analysis/
│   ├── README.md
│   ├── code/
│   ├── data/       # When applicable
│   ├── figures/
│   ├── proofs/     # When applicable
│   └── notes/      # When applicable
├── vector_analysis/
│   ├── README.md
│   ├── code/
│   ├── data/       # When applicable
│   ├── figures/
│   ├── proofs/     # When applicable
│   └── notes/      # When applicable
└── shared/
    ├── code/
    └── data/
    
```

This is a reference structure, not a requirement that every topic contain every subdirectory. Directories should be created when they have a meaningful purpose. Additional top-level research topics may be introduced as the project develops.

## Organizational Principles

### 1. Organize by research question

Each top-level topic represents a distinct area of investigation. Files should be grouped according to the question they help answer, rather than solely by file type.

For example, a Python script that generates a figure about game-state entropy belongs with the game analysis, alongside the resulting figure and relevant notes. It should not be separated into a global scripts directory simply because it is Python code.

When a file genuinely supports multiple topics, prefer placing shared functionality or data in `shared/` rather than duplicating it.

### 2. Keep topic-specific work together

Each research topic should contain the materials needed to understand and reproduce its analyses, as applicable.

- **`README.md`** — Describes the research question, major findings, directory organization, and instructions for reproducing important results.
- **`code/`** — Contains topic-specific scripts, notebooks, algorithms, and figure-generation code.
- **`data/`** — Contains datasets specific to the topic, including documented intermediate or derived data when necessary.
- **`figures/`** — Contains generated plots, diagrams, and other visual outputs associated with the topic.
- **`proofs/`** — Contains formal proofs, mathematical derivations, and supporting arguments relevant to the topic.
- **`notes/`** — Contains exploratory work, conjectures, brainstorming, research summaries, and other supporting documentation that does not fit naturally elsewhere.

These categories are intended to clarify the purpose of files, not to impose unnecessary uniformity. A topic may use additional subdirectories when its size or complexity justifies them.

### 3. Keep shared infrastructure separate

The `shared/` directory is reserved for resources used by multiple research topics. Examples include reusable analysis utilities, common plotting helpers, shared metric calculations, and other genuinely cross-topic code.

A resource should not be moved into `shared/` merely because it could theoretically be reused. If it serves only one topic, keep it there.

Shared code should have clear interfaces and documented dependencies where appropriate. Topic-specific scripts should not depend on undocumented assumptions about the working directory or on arbitrary modifications to Python's import path.

### 4. Distinguish source materials from generated outputs

Whenever practical, keep the code and inputs used to generate a result separate from the result itself.

- Source code belongs in `code/`.
- Input and intermediate datasets belong in `data/`.
- Generated visualizations belong in `figures/`.
- Mathematical arguments belong in `proofs/`.
- Exploratory reasoning and research records belong in `notes/`.

Generated files should not be treated as the authoritative source when they can be reproduced from maintained code and inputs. Conversely, important outputs that are expensive to regenerate or needed to verify a result may be retained, provided their purpose and provenance are documented.

Do not commit interpreter caches, temporary files, or other disposable build artifacts. Large datasets should be handled deliberately, with their source, reproducibility, and version-control implications considered before they are added.

## Naming Conventions

Use consistent, descriptive names so files can be understood from their paths alone.

- Use lowercase `snake_case` for directory and file names where practical.
- Prefer names that describe a research question, mathematical object, analysis, or output.
- Avoid spaces, inconsistent abbreviations, ambiguous names such as `final2`, and unexplained numerical suffixes.
- Use `.py` for Python scripts, `.ipynb` for notebooks, and descriptive extensions for documents and data files.
- Use meaningful names for generated figures that indicate the quantities, methods, or comparison being represented.
- Keep related outputs consistently named so they can be located and regenerated together.

Existing filenames need not be changed merely to satisfy stylistic preferences if doing so adds migration risk without improving clarity. During substantive reorganization, however, inconsistent or ambiguous names should be corrected when practical.

## Documentation Requirements

### Research-level README

This file serves as the entry point for the research directory. It describes the overall organization, links to the major research topics, and provides general guidance for navigating and reproducing the work.

### Topic-level README

Every top-level research topic should have its own `README.md`. At minimum, it should explain:

1. **Research question:** What is being investigated, and why?
2. **Current understanding:** What are the main findings, conclusions, or conjectures?
3. **Directory guide:** Where are the relevant code, data, figures, proofs, and notes?
4. **Important files:** Which scripts, documents, or outputs should a new reader examine first?
5. **Reproduction instructions:** How can the principal analyses or figures be regenerated?
6. **Limitations and open questions:** What remains incomplete, uncertain, or exploratory?

Not every section requires extensive prose. Concise explanations and links to the relevant files are preferable to duplicating material across multiple documents.

### File-level documentation

Individual files should be self-explanatory where possible. Scripts with non-obvious inputs, outputs, parameters, or execution requirements should include brief documentation. Data files should have their source, schema, and generation procedure documented when these details are not otherwise clear.

## Reproducibility

Research should be reproducible to the extent practical, without requiring every scratch experiment to become a fully maintained software package.

- Use the project's documented Python environment and dependency configuration.
- Document required inputs, parameters, and execution commands for important analyses.
- Make assumptions about paths and working directories explicit.
- Record the relationship between source code, data, and generated outputs.
- Preserve important results and supporting materials when regeneration is difficult or costly.
- Update documentation when changes to code, data, or directory structure affect reproducibility.

When a script is exploratory, incomplete, or dependent on undocumented assumptions, its status should be made clear rather than implying that it is a supported reproduction workflow.

## Adding or Modifying Research

When introducing a new analysis or expanding an existing one:

1. Identify the research topic to which it belongs.
2. Place topic-specific code, data, figures, proofs, and notes in their corresponding directories.
3. Reuse existing shared utilities when appropriate.
4. Give new files descriptive names.
5. Document important inputs, outputs, assumptions, and execution instructions.
6. Update the topic-level README if the new work changes the research workflow or contributes a significant result.
7. Update this README if the top-level organization changes.

New top-level topics should represent meaningful, distinct research areas rather than individual scripts or isolated experiments.

## Scope and Philosophy

This directory is a research workspace, not a substitute for the capstone paper or a publication-ready software release. It preserves exploratory work and supporting evidence while providing enough organization for another person to understand the project, locate important results, and reproduce key analyses.

The goal is not maximal abstraction or uniformity. The goal is **clear ownership, predictable organization, and transparent research workflows**.
