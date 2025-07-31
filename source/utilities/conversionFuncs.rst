.. _conversionFuncs:

================================
Convert between RAT and RasCAL-1
================================

RAT is backwards-compatible with RasCAL-1; any RasCAL-1 project can be converted to a RAT project and analysed using RAT, and
it is also possible to convert RAT projects back into RasCAL-1 projects 
(although you will lose any data from features of RAT which are not in RasCAL-1!)


Convert R1 to RAT
.................

As an example, we can use the *'monolayer_8_contrasts'* demo example shipped with RasCAL-1:

.. image:: ../images/misc/rascal1.png
    :width: 800
    :alt: rascal-1


To convert this, simply navigate to the project directory, and run the following:

.. tab-set-code::
    .. code-block:: MATLAB

        problem = r1ToProjectClass('monolayer_8_contrasts.mat')

    .. code-block:: Python

        from ratapi.utils.convert import r1_to_project_class

        problem = r1_to_project_class('monolayer_8_contrasts.mat')

This produces a **Project** object containing the R1 project, which can then be analysed as normal:

.. tab-set-code:: 
    .. code-block:: MATLAB

        controls = controlsClass();
        controls.procedure = 'de';
        controls.parallel = 'contrasts';
        [problem,results] = RAT(problem, controls);
        plotRefSLD(problem, results);

    .. code-block:: Python
        
        import ratapi as RAT

        controls = RAT.Controls(procedure='de', parallel='contrasts')
        problem, results = RAT.run(problem, controls)
        RAT.plotting.plot_ref_sld(problem, results) 


.. tab-set::
    :class: tab-label-hidden
    :sync-group: code

    .. tab-item:: MATLAB
        :sync: MATLAB

        .. image:: ../images/misc/r1Converted.png
            :width: 800
            :alt: The MATLAB plot from running the converted RasCAL-1 example.

    .. tab-item:: Python
        :sync: Python

        .. image:: ../images/misc/r1python.png
            :width: 800
            :alt: The Python plot from running the converted RasCAL-1 example.


Convert RAT to a RasCAL-1 Project
.................................

It is also possible to do the opposite conversion, and convert any RAT **Project** back to an R1 project:

.. tab-set-code::
    .. code-block:: MATLAB

        projectClassToR1(problem,'saveproject',true,'dirName','testProject','fileName','myConvertedProject')

    .. code-block:: Python

        from ratapi.utils.convert import project_class_to_r1

        project_class_to_r1(problem, "./testProject/myConvertedProject") 

This will create the usual RasCAL-1 project structure in a directory called *testProject*, with a filename called *myConvertedProject.mat*
This can then be loaded into RasCAL-1 as normal.

