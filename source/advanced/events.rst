.. _events:

===================================
Handling Events During Calculations
===================================
Sometimes, it is useful to be able to monitor the progress or success of a fit in real time for long simulations. RAT can send out 'events', which contain different data about the 
calculation. By writing functions that 'listen' to these events, you can use this information to build various kinds of updates. 

***************************
Registering Event Listeners
***************************
When an event is triggered, the event data will be passed to any function that is registered for that specific event type. The event listener function (also called an event handler) should recieve a single argument which will be different depending on the event type.
The example below registers a function to listen for the ``Plot`` event:

.. tab-set-code::
    .. code-block:: Matlab

        eventManager.register(eventTypes.Plot, 'updatePlot');
    
    .. code-block:: Python

        import ratapi as RAT
        RAT.events.register(RAT.events.EventTypes.Plot, update_plot)      

The event listener function is also shown below, it uses one of the plot functions provided by RAT to display the event data. The plot event data contains the current state of the reflectivity and SLDs, along with a number of other items which is detailed below.

.. tab-set-code::
    .. code-block:: Matlab

        function updatePlot(eventData)

            h = figure(1000);             % Select / open the figure

            subplot(1,2,1); cla           % Reflectivity plot panel
            subplot(1,2,2); cla           % SLD plot panel
            plotRefSLDHelper(eventData);  % Use the standard RAT reflectivity plot
            drawnow limitrate             % Make sure it updates

        end

    .. code-block:: Python

        import matplotlib.pyplot as plt 
        
        def update_plot(event_data):
            figure = plt.figure(num=1) 
            
            # Use the standard RAT reflectivity plot
            RAT.plotting.plot_ref_sld_helper(event_data, figure)  

.. note::
    A utility function already exists to do live plotting, see :ref:`livePlot` for more information. This section is illustrative for users that want to write more advanced handlers for events.

***********
Event Types
***********
There are a few event types that are emitted by RAT and each type provides different data as its argument to the listener function. The following events are emitted by RAT:

1. :ref:`message_event`
2. :ref:`plot_event`
3. :ref:`progress_event`

Register a function as an event listener by providing the event type and the listener function to the ``register`` function, as shown below.

.. tab-set-code::
    .. code-block:: Matlab

        eventManager.register(eventTypes.Message, handleEvent);   % Message Event
        eventManager.register(eventTypes.Plot, handleEvent);      % Plot Event
        eventManager.register(eventTypes.Progress, handleEvent);  % Progress Event
    
    .. code-block:: Python

        import ratapi as RAT

        RAT.events.register(RAT.events.EventTypes.Message, handle_event)   # Message Event
        RAT.events.register(RAT.events.EventTypes.Plot, handle_event)      # Plot Event
        RAT.events.register(RAT.events.EventTypes.Progress, handle_event)  # Progress Event     

.. _message_event:

Message Event
=============
The message event contains text output from the calculation, which can inform the users about the current step or convergence of the calculation. This event is supported by all algorithms. The event data is a simple string. 

.. _plot_event:

Plot Event
==========
The plot event contains intermediate results from the calculation. As shown in the example above, a good use case for this data is live plotting while the simulation is running. The frequency of the plot events can be controlled from the controls class, see :ref:`frequencyLivePlot` from more information.
This event is supported by the Simplex and DE algorithms. The event data is a structure with the fields described below:

Fields in plot event
********************

.. list-table::
    :header-rows: 1
    
    * - Field
      - Type
      - Description
    * - reflectivity
      - array of double arrays
      - The calculated reflectivities
    * - shiftedData
      - array of double arrays
      - The data corrected with the scalefactor
    * - sldProfiles
      - array of double arrays
      - The calculated SLD profiles
    * - resampledLayers
      - array of double arrays
      - The resampled layers
    * - subRoughs
      - array of doubles
      - The substrate roughness
    * - dataPresent
      - array of boolean/logical values
      - flags indicating which contrast contains data
    * - resample
      - array of boolean/logical values
      - flags indicating which contrast was resampled  
    * - modelType
      - string
      - The model type used for the calculation
    * - contrastNames
      - array of strings
      - The name for each contrast which can be used to add a plot legend
    
.. _progress_event:

Progress Event
==============
The progress event gives the percentage completion for the calculation, and a title text for the event. This event is only supported by the DREAM algorithm. The event data is a structure with the fields described below:

Fields in progress event
************************

.. list-table::
    :header-rows: 1
    
    * - Field
      - Type
      - Description
    * - message
      - string
      - The title text for the event
    * - percent
      - float
      - The percentage of the calculation completed
