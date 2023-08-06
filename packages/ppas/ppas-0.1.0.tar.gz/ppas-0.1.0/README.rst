
ppas - PostProcess Answer Sets
==============================

This program accepts clingo 4.x and clasp 3.x log files and an ASP script to
postprocess the answer sets the log contains.
The result is a rewritten log file.

Each answer is assigned a sequence number starting from 1 and it's atoms are
wrapped in the special predicate _as(Term, SequenceNum). The answer sets are
replaced with atoms read from a special predicate _pp(Term, SequenceNum).

E.g. adding the atom "a." to the first answer set in the log could be done with
the following ASP script::

	% Add "a." to first answer set / model
	_pp(a, 1).
	% Pass everything else through
	_pp(Term, SeqNum) :- _as(Term, SeqNum).

Note that the sequence number does not necessarily correspond to <num> in the
"Answer: <num>" line in the input log file; for example when multiple solve
calls were used.

Installing
----------

Run::

	pip install --user ppas


Usage
-----
::

  ppas <script> <infile> <outfile> [--clingo-bin=<path>, --quiet]
  ppas -h | --help
  ppas --version

	Options:
  	--clingo-bin=<path>       Path to clingo binary.
  	--quiet                   Disable stdout messages.
  	-h --help                 Show this screen.
  	--version                 Show version.

Examples
--------

Examples are available in the examples/ directory.
E.g.::

  ppas.py examples/tsp/script.asp examples/tsp/log.txt tsp-processed.txt

License
-------

MIT. See LICENSE.txt
