# Research

Research in this sense is a very broad term. Everything in this directory is related only by one thing, it was inspired by the game mechanic found in `backend/`. The way they are inspired is varied, as some are direct analysis of the game, some investigate componenets of the game, and some are a very tangential ideas. In this README you can see the basic outline of the directory, with a very brief abstract about each section. Within each section you will find more in depth README's, and documentation within each file.

## Conventions and Dependencies

To initialize this project, make sure you have uv installed, and that you are located in the  `research` directory. Then run `uv sync` and all packages will install according to the dependencies in this project. It is worth noting that `backend` has a separate set of dependencies and will create a separate virtual environment.

Each sub directory under `research` has the same general structure. In each are some common directory names.

- `code`: quick scripts, generation scripts, or any code in any language is here
- `notes`: quick notes, not necessarily with complete information. Mostly markdown
- `archive`: outdated or stale work.
- `data`: raw and generated data
- `figures`: generated images, mostly graphs
- `proofs`: only mathematical proofs that have been completed and are correct

Not all sections will have every sub directory, and some other sub directories may be present.

## Overview

### `research/algorithm_comparison/`

This section takes the multiple algorithms found in `backend/agent_algorithms`, then benchmarks and compares them. Includes many graphs, most of the code is generation of the graphs

### `research/asymptotic_analysis/`

This began as the study of what happens when certain game parameters are sent to infinity. Now, it is the most tangential part of the project, but also still interesting. Make sure to read `research/asymptotic_analysis/notes/discovery.md` to see the thought process behind it.

### `research/game_analysis/`

This is a fully computational analysis of the game, taking into account every possible game outcome. Many graphs are generated, to compare different metrics that arise from the game.

### `research/interactive_graph/`

This is the simplest place to start, because it is just little sandbox to see what happens within the game. Read `research/interactive_graph/how_to.md` to learn how to get it started (make sure you have the dependencies installed)

### `research/mathematical_analysis/`

This section is purely theoretical, and mostly boils down to set counting. It derives formulas for maximum payout, and the probabilities of the game

### `research/paper/`

Contains the final, overarching research paper.

### `research/shared/`

Not much in here, but maybe more will be added with future research

### `research/vector_analysis/`

This section was briefly started, but is unfinished currently

## A quick note on AI use

My goal was to make this research as handmade as possible. That does not mean I did not use AI, but I made it a point not to copy in large chunks of code or mathematical proofs. I did use free models of Claude, Gemini, and ChatGPT, mainly as brainstorming, learning, or boiler plate writing tools.
