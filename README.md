# Kokoro — Chat Storage (Design Snapshot)

## Overview

Kokoro is a local AI ecosystem I have been building to explore modular, offline-first AI system design. The system is intentionally structured around **separation of concerns**, where individual components handle distinct responsibilities such as memory, prompting, inference, and storage.

This repository contains a single module from that ecosystem: **`chat_storage.py`**, which is responsible for persistent conversation storage.

---

## Purpose of This Repository

This repository is not a standalone application and is not intended to be installed or executed as a full system.

It exists as a **design snapshot and demonstration of one subsystem within Kokoro**, specifically the persistence layer for conversational memory.

Included artifacts:

- `chat_storage.py` → core database management logic
- demo SQLite database → example persistent conversation state
- example output (`.md`) → formatted conversation log output

---

## Architecture Role

Within Kokoro, the architecture is intentionally modular:

- Each subsystem is isolated into its own script/module
- Components communicate through defined interfaces rather than shared global logic
- This repository demonstrates that design principle through the separation of storage logic from other AI components

`chat_storage.py` represents the **persistent memory layer** of the system.

---

## Chat Storage System

The `ChatStorage` class is responsible for:

### 1. Database Initialization
- Creates and manages a SQLite database
- Ensures required schema exists on initialization
- Validates expected tables and columns

### 2. Schema Design
The database contains two primary tables:

- `conversations`
  - tracks conversation metadata
  - stores lifecycle information (creation, modification, deletion state)

- `messages`
  - stores individual chat messages
  - links to conversations via foreign key
  - supports optional metadata and raw model outputs

### 3. Data Integrity
- Validates schema consistency on startup
- Enforces expected table and column structure
- Uses foreign key constraints for relational integrity

---

## Standalone Demonstration

Although this module is designed to operate inside the larger Kokoro system, it includes a `__main__` block for demonstration purposes.

This standalone example:

- initializes a local SQLite database
- retrieves a sample conversation
- prints formatted chat history to the terminal

This is intended purely for demonstration and debugging purposes.

---

## Example Outputs

This repository includes:

- A **demo SQLite database**
- A **sample exported conversation in Markdown**

These are included to illustrate how persistent conversation data is stored and retrieved.

---

## Key Design Principles

This module reflects several core design decisions in Kokoro:

- **Separation of concerns** — storage logic is isolated from AI logic
- **Local-first design** — all persistence is handled locally via SQLite
- **Extensibility** — metadata fields allow future expansion (embeddings, tags, model traces)
- **Transparency** — schema validation ensures predictable structure

---

## Limitations

This module is not a complete system and should not be interpreted as one.

- No dependency management is included (by design)
- No runtime orchestration layer is present
- No inference or model logic exists in this repository

It is intentionally minimal and focused only on persistence behavior.

---

## Future Extensions (within Kokoro)

This storage layer is designed to support future enhancements such as:

- vector-based semantic memory retrieval
- message ranking and relevance scoring
- long-term memory compression
- embedding integration for contextual recall

---

## Summary

This repository demonstrates a single, well-defined subsystem of Kokoro: a persistent conversational memory layer built on SQLite, designed for modular integration within a larger local AI architecture.
