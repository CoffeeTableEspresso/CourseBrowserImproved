# CourseBrowserImproved
usage: run `setup.py` when first downloaded to setup database.
afterwards, run `main.py` to access REPL.

Note: you only need to run `setup.py` once, when you first start. It should take a few minutes to run.

valid commands: 

currently, the following commands are supported:

* SELECT statements (based off SQL SELECT statements):
    - syntax: SELECT <fields> FROM <db> [WHERE <cond>]
    - e.g. `SELECT title FROM Courses WHERE "Calculus" IN description`
* variables:
    - syntax: SET <var_name> = <val>
    - e.g. `SET best_dept = "MATH"`
* function definitions:
    - syntax: DEFUN <name> : <params> -> <body>
    - e.g. `DEFUN postreqs : n -> SELECT title FROM Courses WHERE n IN prereqs`
* function calls:
    - syntax: f(arg1, arg2, ... , argN)
    - e.g. `get("MATH 443")`
* builtin functions (e.g. get, postreqs):
   - get(course_name): returns all info for course with given course name.
   - postreqs(course_name): returns title of all courses with course_name as a prereq.
