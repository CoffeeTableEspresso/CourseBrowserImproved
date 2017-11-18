# CourseBrowserImproved
A small terminal based program for browsing and filtering UBC courses.
## Getting Started
### Prerequisites
Requires Python 2.7. Has small incompatibilities with Python 3, i.e. print statements.
### Installing
Download all files into same directory. Run `python setup.py`. 
This should take about 5 to 15 minutes to run, and requires an internet connection.
This setup should only be run once, when you first install everything.

Afterwards, run `python main.py` to access REPL.
## Usage
Run `python main.py` to access REPL, then type any valid command and press enter.
### Valid Commands: 
See `grammar.ebnf` for full description of forms that valid commands can take, and `sample.cbql` for some sample statements.
The following commands are useful for getting started:
* SELECT statements (based off SQL SELECT statements):
    - syntax: SELECT <fields> FROM <db> [WHERE <cond>]
    - e.g. `SELECT title FROM Courses WHERE "Calculus" < description`
* variables:
    - syntax: <var_name> := <val>
    - e.g. `best_dept := "MATH"`
* control flow:
    - ternary operator:
        - syntax: `<cond> ? <val1> : <val2>`
        - e.g. `DEFUN fact : n -> n = 0 ? 1 : fact(n-1)*n`
* operators:
    - supports `+, -, *` for `INT`, `||, <, >` (`STR` concat and contains) for `STR`, `!, &, |` for `BOOL`.
* function definitions:
    - syntax: DEFUN <name> : <params> -> <body>
    - e.g. `DEFUN postreqs : n -> SELECT title FROM Courses WHERE n < prereqs`
* function calls:
    - syntax: f(arg1, arg2, ... , argN)
    - e.g. `get("MATH 443")`
* builtin functions (e.g. get, postreqs):
   - get(course_name): returns all info for course with given course name.
   - postreqs(course_name): returns title of all courses with course_name as a prereq.
   - search(string): returns all courses with string in title or description.
