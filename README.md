# Question Bank API

A simple in-memory question bank service built with **FastAPI**.  
It supports creating, retrieving, updating, deleting, and fetching random
questions.

This project is also an experiment in AI-generated tests: we compare **bad
prompts → vague tests** vs. **good prompts → meaningful tests**.

---

## Run

### Prerequisites

- Python **>= 3.12**
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/) package
  manager

### Install Dependencies

```sh
$ uv sync
```

### Run Server

```sh
$ uv run uvicorn questions_bank.main:app --reload --port 8080
```

### Run Tests

This repo contains two sets of tests that highlight the difference between good
and bad prompts. Good Tests

#### Good Tests

```sh
$ uv run pytest tests/test_questions_good.py
```

#### Bad Tests

```sh
$ uv run pytest tests/test_questions_bad.py
```
