Colour - TODO
=============

TODO
----

- colour (18 items in 12 files)

    - algebra (1 item in 1 file)

        - interpolation.py

            - (236, 15) # TODO: Implements proper wrapper to ensure return values consistency and avoid having to cast to numeric in :meth:`SpectralPowerDistribution.interpolate` method.

    - appearance (8 items in 5 files)

        - ciecam02.py

            - (257, 7) # TODO: Compute hue composition.
            - (684, 7) # TODO: Check for negative values and their handling.

        - hunt.py

            - (406, 7) # TODO: Implement hue quadrature & composition computation.
            - (438, 7) # TODO: Implement whiteness-blackness :math:`Q_{wb}` computation.

        - llab.py

            - (303, 7) # TODO: Implement hue composition computation.

        - nayatani95.py

            - (267, 7) # TODO: Implement hue quadrature & composition computation.
            - (286, 7) # TODO: Investigate components usage.

        - rlab.py

            - (252, 7) # TODO: Implement hue composition computation.

    - colorimetry (1 item in 1 file)

        - spectrum.py

            - (1559, 11) # TODO: Provide support for fractional steps like 0.1, etc...

    - models (2 item in 2 file)

        - tests (1 item in 1 file)

            - tests_derivation.py

                - (123, 15) # TODO: Simplify that monster.

        - derivation.py

            - (153, 7) # TODO: Investigate if we return an ndarray here with primaries and whitepoint stacked together.

    - notation (5 items in 2 files)

        - tests (3 items in 1 file)

            - tests_munsell.py

                - (98, 3) # TODO: Investigate if tests can be simplified by using a common valid set of specifications.
                - (4162, 11) # TODO: This test is covered by the previous class, do we need a dedicated one?
                - (4208, 11) # TODO: This test is covered by the previous class, do we need a dedicated one?

        - munsell.py

            - (828, 11) # TODO: Consider refactoring implementation.
            - (1172, 11) # TODO: Should raise KeyError, need to check the tests.

    - volume (1 item in 1 file)
        
        -  rgb.py
            
            - (323, 11) # TODO: Investigate for generator yielding directly a ndarray.

About
-----

| **Colour** by Colour Developers - 2013 - 2015
| Copyright © 2013 - 2015 – Colour Developers – `colour-science@googlegroups.com <colour-science@googlegroups.com>`_
| This software is released under terms of New BSD License: http://opensource.org/licenses/BSD-3-Clause
| `http://github.com/colour-science/colour <http://github.com/colour-science/colour>`_
