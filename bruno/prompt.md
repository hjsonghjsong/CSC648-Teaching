Project Path: /home/varun/Code/School/SFSU/CSC648-Teaching/AITestExample/bruno

Source Tree:

```
bruno
├── environments
│   └── default.bru
├── Get Questions.bru
├── Get Question.bru
├── bruno.json
├── Delete Question.bru
├── Get Random Questions.bru
├── Modify Question.bru
└── Create Question.bru

```

`/home/varun/Code/School/SFSU/CSC648-Teaching/AITestExample/bruno/environments/default.bru`:

```````bru
vars {
  url: http://localhost:8080
  questionID: 1
}

```````

`/home/varun/Code/School/SFSU/CSC648-Teaching/AITestExample/bruno/Get Questions.bru`:

```````bru
meta {
  name: Get Questions
  type: http
  seq: 1
}

get {
  url: {{url}}/questions?tag=math&n=1
  body: none
  auth: inherit
}

params:query {
  tag: math
  n: 1
}

```````

`/home/varun/Code/School/SFSU/CSC648-Teaching/AITestExample/bruno/Get Question.bru`:

```````bru
meta {
  name: Get Question
  type: http
  seq: 2
}

get {
  url: {{url}}/questions/{{questionID}}
  body: none
  auth: inherit
}

```````

`/home/varun/Code/School/SFSU/CSC648-Teaching/AITestExample/bruno/Delete Question.bru`:

```````bru
meta {
  name: Delete Question
  type: http
  seq: 6
}

delete {
  url: {{url}}/questions/{{questionID}}
  body: none
  auth: inherit
}

```````

`/home/varun/Code/School/SFSU/CSC648-Teaching/AITestExample/bruno/Get Random Questions.bru`:

```````bru
meta {
  name: Get Random Questions
  type: http
  seq: 3
}

get {
  url: {{url}}/questions/random?n=1
  body: none
  auth: inherit
}

params:query {
  n: 1
}

```````

`/home/varun/Code/School/SFSU/CSC648-Teaching/AITestExample/bruno/Modify Question.bru`:

```````bru
meta {
  name: Modify Question
  type: http
  seq: 5
}

put {
  url: {{url}}/questions/{{questionID}}
  body: json
  auth: inherit
}

body:json {
  {
    "text": "What is 1 + 2?",
    "choices": ["1", "2", "3", "4"],
    "answer": "3",
    "tags": ["math", "school"]
  }
}

```````

`/home/varun/Code/School/SFSU/CSC648-Teaching/AITestExample/bruno/Create Question.bru`:

```````bru
meta {
  name: Create Question
  type: http
  seq: 4
}

post {
  url: {{url}}/questions
  body: json
  auth: inherit
}

body:json {
  {
    "text": "What is 1 + 2?",
    "choices": ["1", "2", "3", "4"],
    "answer": "3",
    "tags": ["math", "school"]
  }
}

```````