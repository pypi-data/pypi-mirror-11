profile_eye - browser-based visualization frontend
==================================================

profile_eye is a broswer-based visualization frontend for 
`gprof2dot <https://github.com/jrfonseca/gprof2dot>`_
and 
`graphviz <http://www.graphviz.org/>`_. 

The former is a great tool for parsing profiler outputs and building relevant statstics, and the latter contains excellent graph-placement algorithms. Unfortunately, their outputs are static images. Modern Javascript libraries, e.g., 
`d3.js <http://d3js.org/>`_, do a superior job at dynamic information-rich visualizations. ProfileEye combines these three, with the former two serving as a backend, and the latter serving as a frontend.

The invocation is the same as that of gprof2dot, except, at the end, pipe the output through profile_eye and redirect the result to an html file which you can view via a browswer.

The full documentation is at `http://pythonhosted.org//ProfileEye/ <http://pythonhosted.org//ProfileEye/>`_.

Bug reports can be made at `https://bitbucket.org/atavory/profileeye/issues <https://bitbucket.org/atavory/profileeye/issues>`_.
