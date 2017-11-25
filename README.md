# CourseBrowserImproved
Allows user to browse all UBC courses from the command line without internet connection. Course data matches that on the SSC and includes information about pre-requisites, co-requisites, and course codes/descriptions. Information is stored locally in a B-tree. To make this project, I created a domain specific language to handle user input, and wrote a tree-walk interpreter to execute the DSL. The DSL which allows SQL-like SELECT statements, and various imperative programming constructs as described below. CourseBrowserImproved can be used as course-planning tool adjunct to the SSC.
## Getting Started
### Prerequisites
Requires Python 2.7. Has small incompatibilities with Python 3 (i.e. `print` and `raw_input`).
### Setup
Download all files into same directory, keeping folder structure. Run `python setup.py`. 
This should take about 5 to 15 minutes to run, and requires an internet connection.
This setup should only be run once, when you first install everything.
## Usage
Run `python main.py` to access REPL,  or run `python main.py example.cbql` to run program `example.cbql`.
### Valid Commands: 
See `grammar.ebnf` for full description of forms that valid commands can take, and `sample.cbql` for some examples.
The following commands are useful for getting started:
* SELECT statements (based off SQL SELECT statements):
    - syntax: SELECT <fields> FROM <db> [WHERE <cond>]
    - e.g. `SELECT title FROM Courses WHERE "Calculus" < description`
* variables:
    - syntax: <var_name> := <val>
    - e.g. `best_dept := "MATH"`
* function definitions:
    - syntax: DEFUN <name> : <params> -> <body>
    - e.g. `DEFUN postreqs : n -> SELECT title FROM Courses WHERE n < prereqs`
* function calls:
    - syntax: f(arg1, arg2, ... , argN)
    - e.g. `get("MATH 443")`
* control flow:
    - ternary operator:
        - syntax: `<cond> ? <val1> : <val2>`
        - e.g. `DEFUN fact : n -> n = 0 ? 1 : fact(n-1)*n`
    - WHILE loops:
        - syntax: `WHILE <cond> : <expr>`
        - e.g. `DEFUN fact : n -> BEGIN x := 1; WHILE n <> 0 : BEGIN x *= n; n -= 1; END; x; END;`
* operators:
    - supports `+, -, *` for `INT`, `||, <, >` (`STR` concat and contains) for `STR`, `!, &, |` for `BOOL`, and `=, <>` (equality and inequality for all types).
* builtin functions (e.g. get, postreqs):
   - get(course_name): returns all info for course with given `course_name`.
   - postreqs(course_name): returns title of all courses with `course_name` as a prereq.
   - search(query): returns all courses with `query` in title or description.
