.. _controls:

===================================
A Closer Look at the Controls Class
===================================

We have already seen in previous sections that once the problem has been defined in the project class, it is necessary to define a **Controls**
object which, as its name suggests, tells RAT what we want to do with the project.

Making an instance of the **Controls** class is quite simple:

.. tab-set-code::
    .. code-block:: Matlab
        
        controls = controlsClass();

    .. code-block:: Python
        
        controls = RAT.Controls()


This then creates an instance of the **Controls** class with a number of options defined:

.. tab-set::
    :class: tab-label-hidden
    :sync-group: code

    .. tab-item:: Matlab
        :sync: Matlab

        .. output:: Matlab

            controls = controlsClass();
            disp(controls)

    .. tab-item:: Python
        :sync: Python

        .. output:: Python

            controls = RAT.Controls()
            print(controls)

We will look at each of these in more detail below. Note that the options that are visible depend on
the ``procedure`` selected. So, at the moment the ``procedure`` is set to ``"calculate"``, which will simply calculate the reflectivity and 
SLD for any associated problem. If we select the ``"simplex"`` algorithm as the ``procedure``, a different set of options appears:

.. tab-set-code::
    .. code-block:: Matlab
        
        controls.procedure = 'simplex';

    .. code-block:: Python
        
        controls.procedure = 'simplex'


.. tab-set::
    :class: tab-label-hidden
    :sync-group: code

    .. tab-item:: Matlab
        :sync: Matlab

        .. output:: Matlab

            controls = controlsClass();
            controls.procedure = 'simplex';
            disp(controls)

    .. tab-item:: Python
        :sync: Python

        .. output:: Python

            controls = RAT.Controls(procedure='simplex')
            print(controls)

which allow the user to set things such as tolerance targets and so on. There are a different set of options for each algorithm.
We will now look at each of the available options in turn.

General parameters for the Controls Class
-----------------------------------------

These are the general parameters for the controls class. For algorithm-specific parameters see the page for each algorithm in the
:ref:`algorithms section<algorithms>`.

``procedure``
^^^^^^^^^^^^^
Which algorithm RAT should run. Currently the options are:

- ``"calculate"``: A simple `Abelès calculation <https://www.reflectometry.org/learn/3_reflectometry/slab_models/how_we_calculate_the_reflectivity_of_a_slab_model.html>`_
  of reflectivity for the model, with chi-squared fit calculated between the model and the data. 
- ``"simplex"``: Optimisation via the Nelder-Mead :ref:`simplex method<simplex>`.
- ``"de"``: Optimisation via :ref:`differential evolution<DE>`.
- ``"ns"``: Bayesian optimisation via :ref:`nested sampling<nestedSampling>`.
- ``"dream"``: Bayesian optimisation via the :ref:`DREAM algorithm<DREAM>`.

``parallel``
^^^^^^^^^^^^
How the calculation should be :ref:`parallelised<parallelisation>`. Currently the options are:

- ``"single"``: do not parallelise.
- ``"contrasts"``: each contrast gets its own calculation thread.
- ``"points"``: each contrast is split into a number of sections, and each section gets its own calculation thread.

Which option is more efficient will depend on the number of contrasts and the size of your data.

``calcSldDuringFit``
^^^^^^^^^^^^^^^^^^^^
A boolean (true or false) value which determines whether SLD will be calculated during the fit
(for :ref:`live plotting<livePlot>` etc.)

``display``
^^^^^^^^^^^
How much RAT should print to the terminal. The current options are:

- ``"off"``: No display.
- ``"iter"``: Give information after every iteration for iterative algorithms.
- ``"notify"``:
- ``"final"``: Just provide information when the calculation has finished.

Resampling parameters (``resampleMinAngle`` and ``resampleNPoints``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The two parameters ``resampleMinAngle`` and ``resampleNPoints`` decide how
adaptive resampling will be used on the SLD profiles. 
See the :ref:`resampling page<resampling>` for more details. In short:

- ``resampleMinAngle``: For each data point, the algorithm draws two lines from that data point to its neighbouring points on either side. 
  If the angle between those lines is smaller than ``resampleMinAngle``, then the algorithm will refine over that point. 

  In practice, this means that resampling happens for points which are significantly higher or lower than their neighbours
  (i.e. the gradient of the function has changed rapidly)
  and ``resampleMinAngle`` controls the sensitivity of this.
  
  ``resampleMinAngle`` is defined in the units of "radians divided by pi", i.e. ``resampleMinAngle = 0.9`` refines where the adjacent points form an angle smaller than :math:`0.9 \pi` radians.

- ``resampleNPoints``: The initial number of domain points (layers) sampled by the algorithm at the start.

``numSimulationPoints``
^^^^^^^^^^^^^^^^^^^^^^^
The number of points used for a reflectivity simulation where no data is present.
