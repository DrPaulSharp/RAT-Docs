.. _project:

=================
The Project Class
=================
In the previous section, we saw an example of how we set up and run an analysis using RAT. 
Every call to the toolbox has two parts: the **Project** object, where we define the model, 
add the data and define our contrasts, and the **Controls** object where we tell the toolbox 
what type of analysis we would like to do. The reason for splitting things up in this way is that 
once our model is defined, we can interact with it in various ways without needing to modify the model. 
So we can try out different types of analysis and explore the landscape of solutions 
by simply modifying the **Controls** object, leaving the **Project** object alone.

In the following sections, we will look at how to build a standard layer slab model with the **Project** class. It is also
possible to define a custom model using a function; this is seen in the :ref:`customModels` tutorial. 

***********************************
The Components of the Project Class
***********************************

Project Defining Methods
========================

The first step is always to create an instance of the **Project** class to hold our model. 

This is always done by calling the project creation routine and assigning it to our variable name 
(we will mostly use ``problem`` in this manual), which always requires a name for our project as an input:

.. tab-set-code::
    .. code-block:: Matlab

        problem = createProject(name='My Problem');
    
    .. code-block:: Python
    
        problem = RAT.Project(name='My Problem')
    
This creates an instance of **Project**, assigns it to the variable ``problem``, and gives it the title 'My Problem'.

The first part of the created ``problem`` has two other fields: **Model Type** and **Geometry**.

* **Geometry**: This can be set to either ``"air/substrate"`` or ``"substrate/liquid"`` as below.

.. tab-set-code::
    .. code-block:: Matlab

        problem.geometry = 'air/substrate';
        problem.geometry = 'substrate/liquid';
    
    .. code-block:: Python

        problem.geometry = 'air/substrate'
        problem.geometry = 'substrate/liquid'

The effect of this parameter is in the numbering of roughness values in layer models. In any model for n-layers,
there are always n+1 associated interfaces, and hence n+1 roughness parameters required. In RAT, the bulk interface roughness
is a protected parameter called ``"Substrate Roughness"`` which always exists.
The **Geometry** field controls where this roughness is placed in the layer stack. So, for two layers defined with thickness,
SLD and roughness :math:`[d_1, \rho_1, \sigma_1]` and :math:`[d_2, \rho_2, \sigma_2]`, 
then for the ``"substrate/liquid"`` geometry the substrate roughness is placed as the first roughness the beam meets, 
and the layer roughness values refer to the interface after the particular layer.
But in the ``"air/substrate"`` case, the opposite is true, 
and the substrate roughness is the last roughness in the stack, with the layer roughness referring to the interface before each layer.

* **Model Type**: There are three ways of defining models in RAT:

    * **Standard Layers** - The model is defined in terms of parameters, which are distributed into layers, and subsequently grouped into contrasts. 
      No external functions are needed.
    * **Custom Layers** - Parameters are again defined and grouped into layers, but this time the layer definitions come from a user model script. 
      This then gives complete flexibility of how layers are defined, so allowing models to be written in terms of area per molecule or material density, 
      for example. This custom script controls translating these input parameters into a :math:`[d, \rho, \sigma]` (thickness, SLD, roughness) model. 
      This is probably the most useful operating mode for RasCAL. 
    * **Custom XY-Profile** - This modelling mode also relies on a custom model function, 
      but in this case does away with :math:`[d, \rho, \sigma]` layers completely. 
      Instead, the custom function uses the parameters to define a continuous SLD profile, which RAT then uses to calculate the reflectivity.

.. note:: 
   This tutorial just deals with standard layers. For information on the other model types, see :ref:`customLayers`.

The model type of the project can be changed as follows:

.. tab-set-code::
    .. code-block:: Matlab

        problem.modelType = 'standard layers';
        problem.modelType = 'custom layers';
        problem.modelType = 'custom XY';
    
    .. code-block:: Python

        problem.model = 'standard layers'
        problem.model = 'custom layers'
        problem.model = 'custom XY'

Custom modelling is described in more depth in a :ref:`later section<customModels>`.

The Parameters Block
====================

The parameters block outlines the material parameters of our model, such as thickness, SLD or roughness.
These parameters are specified by a name, a value, minimum and maximum ranges,
and a flag defining whether the parameter is fitted or fixed:


.. tab-set::
    :class: tab-label-hidden
    :sync-group: code

    .. tab-item:: Matlab
        :sync: Matlab

        .. output:: Matlab

            problem = createProject(name='My Problem');
            problem.parameters.displayTable()

    .. tab-item:: Python 
        :sync: Python
        
        .. output:: Python

            problem = RAT.Project(name='my project')
            print(problem.parameters)

The ``"Substrate Roughness"`` is a protected parameter in all cases (it defines the Fresnel roughness) and cannot be renamed or deleted.
Its value and ranges can however be set to any numerical values.

To add a parameter, you can just specify a name, in which case the parameter takes on default values, or specify the whole parameter at once:

.. tab-set-code::
    .. code-block:: Matlab

        problem.addParameter('My new param', 1, 2, 3);
        problem.addParameter('My other new param',10,20,30,false);

    .. code-block:: Python

        problem.parameters.append(name='My new param', min=1, value=2, max=3)
        problem.parameters.append(name='My other new param', min=10, value=20, max=30, fit=False)

To avoid having to make a whole load of statements for large projects with many parameters, you can define them at once in an array, and add them as a group: 

.. tab-set-code::
    .. code-block:: Matlab

        pGroup = {{'Layer thick', 10, 20, 30, true};
                  {'Layer SLD', 1e-6, 3e-6 5e-6, true};
                  {'Layer rough', 5, 7, 10, true}};
            
        problem.addParameterGroup(pGroup)
    
    .. code-block:: Python
        
        pGroup = [['Layer thick', 10, 20, 30, True,],
                  ['Layer SLD', 1e-6, 3e-6, 5e-6, True,],
                  ['Layer rough', 5, 7, 10, True]]

        for param in pGroup:
            problem.parameters.append(name=param[0], min=param[1], value=param[2], max=param[3], fit=param[4])

The resulting parameters block looks like this:

.. tab-set::
    :class: tab-label-hidden
    :sync-group: code

    .. tab-item:: Matlab
        :sync: Matlab

        .. output:: Matlab

            problem.addParameter('My new param', 1, 2, 3);
            problem.addParameter('My other new param',10,20,30,false);
            pGroup = {{'Layer thick', 10, 20, 30, true};
                    {'Layer SLD', 1e-6, 3e-6 5e-6, true};
                    {'Layer rough', 5, 7, 10, true}};
                
            problem.addParameterGroup(pGroup);
            problem.parameters.displayTable()

    .. tab-item:: Python 
        :sync: Python
        
        .. output:: Python

            problem.parameters.append(name='My new param', min=1, value=2, max=3)
            problem.parameters.append(name='My other new param', min=10, value=20, max=30, fit=False)
            pGroup = [RAT.models.Parameter(name='Layer thick', min=10, value=20, max=30, fit=True),
                      RAT.models.Parameter(name='Layer SLD', min=1e-6, value=3e-6, max=5e-6, fit=True),
                      RAT.models.Parameter(name='Layer rough', min=5, value=7, max=10, fit=True)] 
    
            problem.parameters.extend(pGroup)
            print(problem.parameters)

.. warning::
    Parameters can't have duplicate names. Attempting to duplicate a name will throw an error. This can cause problems when loading in RasCAL-1 projects
    where duplicate names are allowed.

To subsequently change the values of the parameters (including names), you can set the properties of a given parameter using name/value pairs, 
which parameter to set can be specified using the index number or name of the parameter:

.. tab-set-code::
    .. code-block:: Matlab

        problem.setParameter('My new param', 'name', 'My changed param');
        problem.setParameter(2, 'min', 0.96, 'max', 3.62);
        problem.setParameter(4, 'value', 20.22);
        problem.setParameter('Layer rough', 'fit', false);
    
    .. code-block:: Python

        problem.parameters['My new param'].name = 'My changed param'
        problem.parameters[1].min = 0.96
        problem.parameters[1].max = 3.62
        problem.parameters['Layer thick'].value = 20.22
        problem.parameters['Layer rough'].fit = False

.. tab-set::
    :class: tab-label-hidden
    :sync-group: code

    .. tab-item:: Matlab
        :sync: Matlab

        .. output:: Matlab

            problem.setParameter('My new param', 'name', 'My changed param');
            problem.setParameter(2, 'min', 0.96, 'max', 3.62);
            problem.setParameter(4, 'value', 20.22);
            problem.setParameter('Layer rough', 'fit', false);
            problem.parameters.displayTable()

    .. tab-item:: Python 
        :sync: Python
        
        .. output:: Python

            problem.parameters['My new param'].name = 'My changed param'
            problem.parameters[1].min = 0.96
            problem.parameters[1].max = 3.62
            problem.parameters['Layer thick'].value = 20.22
            problem.parameters['Layer rough'].fit = False
            print(problem.parameters)

Alternatively, you can set multiple properties of a given parameter at once using name/value pairs.

.. tab-set-code::
    .. code-block:: Matlab

        problem.setParameter('Layer thick', 'name', 'thick', 'min', 5, 'max', 33, 'fit', false)
    
    .. code-block:: Python

        problem.parameters.set_fields('Layer thick', name='thick', min=5, max=33, fit=False)

.. tab-set::
    :class: tab-label-hidden
    :sync-group: code

    .. tab-item:: Matlab
        :sync: Matlab

        .. output:: Matlab

            problem.setParameter(4, 'name', 'thick', 'min', 5, 'max', 33, 'fit', false);
            problem.parameters.displayTable()

    .. tab-item:: Python 
        :sync: Python
        
        .. output:: Python

            problem.parameters.set_fields(3, name='thick', min=5, max=33, fit=False)
            print(problem.parameters)

You can remove a parameter from the block using its index number or name. Note that if you remove a parameter from the middle of the block, 
subsequent parameter index numbers will change. 
Also, if you try to remove the substrate roughness you will get an error:

.. tab-set-code::
    .. code-block:: Matlab

        problem.removeParameter('Layer thick');
    
    .. code-block:: Python

        problem.parameters.remove('Layer thick')


.. tab-set::
    :class: tab-label-hidden
    :sync-group: code

    .. tab-item:: Matlab
        :sync: Matlab

        .. output:: Matlab

            problem.removeParameter(4);
            problem.parameters.displayTable()

    .. tab-item:: Python 
        :sync: Python
        
        .. output:: Python

            del problem.parameters[3]
            print(problem.parameters)

.. tab-set-code::
    .. code-block:: Matlab

        problem.removeParameter(1);
    
    .. code-block:: Python

        del problem.parameters[0]


.. tab-set::
    :class: tab-label-hidden
    :sync-group: code

    .. tab-item:: Matlab
        :sync: Matlab

        .. output:: Matlab

            try
                problem.removeParameter(1);
            catch ERROR
                disp(getReport(ERROR))
            end

    .. tab-item:: Python 
        :sync: Python
        
        .. output:: Python

            try:
                del problem.parameters[0]
            except Exception as err:
                print(err)

.. note::
   There are additional properties of Parameters used for Bayesian algorithms; see the :ref:`Bayes tutorial<bayesTutorial>`.


.. _standardLayers:

The Layers Block (Standard Layers models only)
==============================================

For standard layers models, model building is done by grouping the parameters into layers, and then into contrasts.
The layers block is not visible when either of the two custom models are selected. Layers are stored in the ``layers`` field of the **Project**. 
As an example here, we make a new project, add some parameters, and create some layers.

For each of the custom models cases, the model building is done using a script (discussed in :ref:`customModels`). 


For this example, we will make two layers representing a deuterated and hydrogenated version of the same layer. 
So, the layers will share all their parameters except for the SLD.

Start by making a new project, and adding the parameters we will need:

.. tab-set-code::
    .. code-block:: Matlab

        problem = createProject(name='Layers Example');
    
        params = {{'Layer Thickness', 10, 20, 30, false};
                  {'H SLD', -6e-6, -4e-6, -1e-6, false};
                  {'D SLD', 5e-6, 7e-6, 9e-6, true};
                  {'Layer rough', 3, 5, 7, true};
                  {'Layer hydr', 0, 10, 20, true}};
            
        problem.addParameterGroup(params);
    
    .. code-block:: Python

        problem = RAT.Project(name='Layers Example')
        
        params = [['Layer Thickness', 10, 20, 30, False],
                  ['H SLD', -6e-6, -4e-6, -1e-6, False],
                  ['D SLD', 5e-6, 7e-6, 9e-6, True],
                  ['Layer rough', 3, 5, 7, True],
                  ['Layer hydr', 0, 10, 20, True]]
 
        for param in params:
            problem.parameters.append(name=param[0], min=param[1], value=param[2], max=param[3], fit=param[4])


A layer is defined in terms of a name, thickness, SLD, roughness and (optional) hydration, along with details of which bulk phase is hydrating the layer.
The easiest way to define these is to group the parameters into cell arrays, and then add them to the project as a layers group:

.. tab-set-code::
    .. code-block:: Matlab

        problem.addLayer('H Layer','Layer Thickness','H SLD','Layer rough','Layer hydr','bulk out');
        problem.addLayer('D Layer','Layer Thickness','D SLD','Layer rough','Layer hydr','bulk out');
    
    .. code-block:: Python

        problem.layers.append(name='H Layer', thickness='Layer Thickness', SLD='H SLD',
                              roughness='Layer rough', hydration='Layer hydr', hydrate_with='bulk out')
        problem.layers.append(name='D Layer', thickness='Layer Thickness', SLD='D SLD',
                              roughness='Layer rough', hydration='Layer hydr', hydrate_with='bulk out')


Our two layers now appear in the ``layers`` block of the project:

.. tab-set::
    :class: tab-label-hidden
    :sync-group: code

    .. tab-item:: Matlab 
        :sync: Matlab

        .. output:: Matlab

            problem = createProject(name='Layers Example');
        
            params = {{'Layer Thickness', 10, 20, 30, false};
                    {'H SLD', -6e-6, -4e-6, -1e-6, false};
                    {'D SLD', 5e-6, 7e-6, 9e-6, true};
                    {'Layer rough', 3, 5, 7, true};
                    {'Layer hydr', 0, 10, 20, true}};
                
            problem.addParameterGroup(params);

            % Make the layers
            H_layer = {'H Layer','Layer Thickness','H SLD','Layer rough','Layer hydr','bulk out'};
            D_layer = {'D Layer','Layer Thickness','D SLD','Layer rough','Layer hydr','bulk out'};
            
            % Add them to the project - as a cell array{}
            problem.addLayerGroup({H_layer, D_layer});

            problem.layers.displayTable()

    .. tab-item:: Python 
        :sync: Python

        .. output:: Python

            problem = RAT.Project(name='Layers Example')
            params = [RAT.models.Parameter(name='Layer Thickness', min=10, value=20, max=30, fit=False),
                      RAT.models.Parameter(name='H SLD', min=-6e-6, value=-4e-6, max=-1e-6, fit=False),
                      RAT.models.Parameter(name='D SLD', min=5e-6, value=7e-6, max=9e-6, fit=True),
                      RAT.models.Parameter(name='Layer rough', min=3, value=5, max=7, fit=True),
                      RAT.models.Parameter(name='Layer hydr', min=0, value=10, max=20, fit=True)]
            problem.parameters.extend(params)

            problem.layers.append(name='H Layer', thickness='Layer Thickness', SLD='H SLD',
                                roughness='Layer rough', hydration='Layer hydr', hydrate_with='bulk out')
            problem.layers.append(name='D Layer', thickness='Layer Thickness', SLD='D SLD',
                                roughness='Layer rough', hydration='Layer hydr', hydrate_with='bulk out')

            print(problem.layers)

Note that in RAT, hydration is percent hydration between 0 and 100. It is not necessary to define a hydration at all, and we can also make layers without this parameter:

.. tab-set-code::
    .. code-block:: Matlab

        % Non hydrated layer
        problem.addLayer('Dry Layer', 'Layer Thickness', 'D SLD', 'Layer rough');
    
    .. code-block:: Python

        problem.layers.append(name='Dry Layer', thickness='Layer Thickness', SLD='D SLD', roughness='Layer rough')

.. tab-set::
    :class: tab-label-hidden
    :sync-group: code

    .. tab-item:: Matlab
        :sync: Matlab

        .. output:: Matlab

            problem.addLayer('Dry Layer', 'Layer Thickness', 'D SLD', 'Layer rough');
            problem.layers.displayTable()

    .. tab-item:: Python 
        :sync: Python

        .. output:: Python

            problem.layers.append(name='Dry Layer', thickness='Layer Thickness', SLD='D SLD', roughness='Layer rough')
            print(problem.layers)


The value of an existing layer can be changed by specifying the layer, layer parameter to be changed and the name of the new parameter.

.. tab-set-code::
    .. code-block:: Matlab

        problem.setLayer('H Layer', 'thickness', 'H SLD');

    .. code-block:: Python

        problem.layers.set_fields('H Layer', thickness='H SLD') 

.. tab-set::
    :class: tab-label-hidden
    :sync-group: code

    .. tab-item:: Matlab
        :sync: Matlab

        .. output:: Matlab

            problem.setLayer('H Layer', 'thickness', 'H SLD');
            problem.layers.displayTable()

    .. tab-item:: Python 
        :sync: Python

        .. output:: Python

            problem.layers.set_fields(0, thickness='H SLD') 
            print(problem.layers)


The layers are then used to set up the contrasts as usual with a standard layers model.

Bulk Phases
===========

These are treated in the same way as parameters e.g.

.. tab-set-code::
    .. code-block:: Matlab

        problem.addBulkIn('Silicon', 2.0e-6, 2.07e-6, 2.1e-6, false);
        problem.addBulkOut('H2O', -0.6e-6, -0.56e-6, -0.5e-6, false);
    
    .. code-block:: Python
        
        problem.bulk_in.append(name='Silicon', min=2.0e-06, value=2.073e-06, max=2.1e-06, fit=False)
        problem.bulk_out.append(name='H2O', min=-0.6e-6, value=-0.56e-6, max=-0.5e-6, fit=False)

.. tab-set::
    :class: tab-label-hidden
    :sync-group: code

    .. tab-item:: Matlab
        :sync: Matlab

        .. output:: Matlab

            problem.addBulkIn('Silicon', 2.0e-6, 2.07e-6, 2.1e-6, false);
            problem.addBulkOut('H2O', -0.6e-6, -0.56e-6, -0.5e-6, false);
            problem.bulkIn.displayTable()
            problem.bulkOut.displayTable()

    .. tab-item:: Python 
        :sync: Python

        .. output:: Python

            problem.bulk_in.append(name='Silicon', min=2.0e-06, value=2.073e-06, max=2.1e-06, fit=False)
            problem.bulk_out.append(name='H2O', min=-0.6e-6, value=-0.56e-6, max=-0.5e-6, fit=False)
            print(problem.bulk_in)
            print(problem.bulk_out)

The values of **Bulk In** and **Bulk Out** can be modified as shown below:

.. tab-set-code::
    .. code-block:: Matlab

        problem.setBulkOut('H2O, 'value', 5.9e-6, 'fit', true);
        problem.setBulkIn('Silicon', 'value', 5.9e-6, 'fit', true);

    .. code-block:: Python

        problem.bulk_out.set_fields('H2O', value=5.9e-6, fit=True)
        problem.bulk_in.set_fields('Silicon', value=5.9e-6, fit=True)


Scalefactors
============
The ``scalefactors`` are also a parameters block like the bulk phases. You can add and modify ``scalefactors`` similarly to the previous blocks.

.. tab-set-code::
    .. code-block:: Matlab

        problem.addScalefactor('New Scalefactor',0.9,1.0,1.1,true);
        problem.setScalefactor('New Scalefactor','value',1.01);
    
    .. code-block:: Python

        problem.scalefactors.append(name='New Scalefactor', min=0.9, value=1.0, max=1.1, fit=True)
        problem.scalefactors.set_fields('New Scalefactor', value=1.01)

Backgrounds
===========
The ``backgrounds`` block is used to define the type of background applied to each contrast, and the parameters used to define the backgrounds themselves. The fittable parameters are in the
**Background Parameters** block, and the backgrounds themselves are in the ``backgrounds`` block:


.. tab-set::
    :class: tab-label-hidden
    :sync-group: code

    .. tab-item:: Matlab
        :sync: Matlab

        .. output:: Matlab

            problem.background.displayTable()

    .. tab-item:: Python 
        :sync: Python

        .. output:: Python
            
            print(problem.background_parameters)
            print(problem.backgrounds)

The **Background Parameters** is in fact another instance of the parameters class, and there are corresponding methods to fit, set limits and so on for these.

The backgrounds can be one of three types: ``"constant"``, ``"function"`` or ``"data"``. The three types are discussed in more detail below:

* ``"constant"`` - This is the normal background type from RasCAL-1. Each background requires one **and only one** Background Parameter associated with it, as follows:

.. tab-set-code::
    .. code-block:: Matlab

        problem.addBackgroundParam('My New BackPar', 1e-8, 1e-7, 1e-6, true);
        problem.addBackground('My New Background','constant','My New BackPar');

    .. code-block:: Python

        problem.background_parameters.append(name='My New BackPar', min=1e-8, value=1e-7, max=1e-6, fit=True)
        problem.background.append(name='My New Background', type='constant', source='My New BackPar')


With this code snippet we've made a new background, with the value taken from the (fittable) parameter called 'My New BackPar':

.. tab-set::
    :class: tab-label-hidden
    :sync-group: code

    .. tab-item:: Matlab
        :sync: Matlab

        .. output:: Matlab

            problem.addBackgroundParam('My New BackPar', 1e-8, 1e-7, 1e-6, true);
            problem.addBackground('My New Background','constant','My New BackPar');
            problem.background.displayTable()

    .. tab-item:: Python 
        :sync: Python

        .. output:: Python

            problem.background_parameters.append(name='My New BackPar', min=1e-8, value=1e-7, max=1e-6, fit=True)
            problem.backgrounds.append(name='My New Background', type='constant', source='My New BackPar')
            print(problem.background_parameters)
            print(problem.backgrounds)


This is then available to be used by any of our contrasts (see later).

* ``"data"`` - This option is used when a measured data background is available. Our measured data is given in a datafile loaded into the data block (see later).
  To define a data background from a datafile called 'My Background Data', we simply specify this datafile in our background specification:

.. tab-set-code::
    .. code-block:: Matlab

        problem.addBackground('Data Background 1', 'data', 'My Background Data')
    
    .. code-block:: Python

        problem.backgrounds.append(name='Data Background 1', type='data', source='My Background Data')

* ``"function"`` - This option defines the background using a function loaded into the custom file block (see later).
  To define a function background, we simply specify this custom file in our background specification, along with
  up to five background parameters (defined in the background parameters block) to use in the function.

  In the following code block we define a background based on the function ``"My Background Function"`` which takes two values given
  by ``"Background Parameter 1"`` and ``"Background Parameter 2"``

.. tab-set-code::
    .. code-block:: Matlab

        problem.addBackground('Data Background 1', 'function', 'My Background Function', 'Background Parameter 1', 'Background Parameter 2')
    
    .. code-block:: Python

        problem.backgrounds.append(name='Data Background 1', type='data', source='My Background Function' value_1='Background Parameter 1', value_2='Background Parameter 2')

This is then used in the reflectivity calculation for any contrast in which it is specified.

.. warning::
    Take care to make sure that the background and data with which it is intended to be used have **the same q values**, otherwise the code will raise an error.


Resolutions
===========
As is the case for the backgrounds, the resolutions block is also split into two parts: a **Resolution Parameters** block which defines the fittable parameters, 
and then the main ``resolutions`` block which groups these as required into actual resolutions.
The three types are:

*   ``"constant"``: The default type. A resolution parameter defines the width of a sliding Gaussian window convolution applied to the data.
*   ``"data"``: Convolution with a sliding Gaussian defined by a fourth column of a datafile.

To define a resolution parameter, we use the following methods:

.. tab-set-code::
    .. code-block:: Matlab

        problem.addResolutionParam('My Resolution Param', 0.02, 0.05, 0.08, true)

    .. code-block:: Python

        problem.resolution_parameters.append(name='My Resolution Param', min=0.02, value=0.05, max=0.08, fit=True)


.. tab-set::
    :class: tab-label-hidden
    :sync-group: code

    .. tab-item:: Matlab
        :sync: Matlab

        .. output:: Matlab

            problem.resolution.displayTable()

    .. tab-item:: Python 
        :sync: Python

        .. output:: Python

            print(problem.resolution_parameters)
            print(problem.resolutions)


Then, we make the actual resolution referring to whichever one of the resolution parameters:

.. tab-set-code::
    .. code-block:: Matlab

        problem.addResolution('My new resolution','constant','My Resolution Param')
        problem.addResolution('My Data Resolution','data')

    .. code-block:: Python
    
        problem.resolutions.append(name='My new resolution', type='constant', source='My Resolution Param')
        problem.resolutions.append(name='My Data Resolution', type='data')

.. tab-set::
    :class: tab-label-hidden
    :sync-group: code

    .. tab-item:: Matlab
        :sync: Matlab

        .. output:: Matlab

            problem.addResolutionParam('My Resolution Param', 0.02, 0.05, 0.08, true);
            problem.addResolution('My new resolution','constant','My Resolution Param');
            problem.addResolution('My Data Resolution','data');
            problem.resolution.displayTable()

    .. tab-item:: Python 
        :sync: Python

        .. output:: Python

            problem.resolution_parameters.append(name='My Resolution Param', min=0.02, value=0.05, max=0.08, fit=True)
            problem.resolutions.append(name='My new resolution', type='constant', source='My Resolution Param')
            problem.resolutions.append(name='My Data Resolution', type='data')
            print(problem.resolutions)

.. warning::
   There are no parameters for a ``"data"`` resolution. Instead this tells RAT to expect a fourth column in the datafile for the contrast. 
   If no fourth column exists in the data to which this is applied, RAT will throw an error at runtime.


Data
====
The data block contains the data which defines at which points in q the reflectivity is calculated at each contrast. 
By default, it initialises with a single ``"Simulation"`` entry:

.. tab-set::
    :class: tab-label-hidden
    :sync-group: code

    .. tab-item:: Matlab
        :sync: Matlab

        .. output:: Matlab

            problem.data.displayTable()

    .. tab-item:: Python 
        :sync: Python

        .. output:: Python

            print(problem.data)


For each entry in the table there are four fields:

* **Name**: The name you choose to give the datafile (for reference in the contrasts block)
* **Data**: An array containing the data itself (empty for 'Simulation').
* **Data Range**: The min / max range of the data you wish to include in the fit. 
  You do not have to include all the data in the calculation of chi-squared. 
  This range must lie **within** the range of the dataset.
* **Simulation Range**: The total range of the simulation to be calculated. 
  This must be equal to or larger than the range of any data added to the **Data** column.

To add data, we first load it into Matlab/Python, then create a new data entry containing it:

.. tab-set-code::
    .. code-block:: Matlab

        root = getappdata(0, 'root');
        myData = readmatrix(fullfile(root, '/examples/normalReflectivity/customXY/c_PLP0016596.dat'));
        problem.addData('My new datafile', myData)
    
    .. code-block:: Python

        import numpy as np
        myData = np.loadtxt('c_PLP0016596.dat', delimiter=",")
        problem.data.append(name='My new datafile', data=myData)

and our new dataset appears in the table:

.. tab-set::
    :class: tab-label-hidden
    :sync-group: code

    .. tab-item:: Matlab
        :sync: Matlab

        .. output:: Matlab

            root = getappdata(0, 'root');
            myData = readmatrix(fullfile(root, '/examples/normalReflectivity/customXY/c_PLP0016596.dat'));
            problem.addData('My new datafile', myData);
            problem.data.displayTable()

    .. tab-item:: Python 
        :sync: Python

        .. output:: Python

            from importlib.resources import files
            import numpy as np
            data_path =  files("ratapi.examples.data")
            myData = np.loadtxt(data_path / 'c_PLP0016596.dat', delimiter=',')
            problem.data.append(name='My new datafile', data=myData)
            print(problem.data)


Note that we did not specify data or simulation ranges, and so these default to the min / max values of the data added. We can change these as follows:

.. tab-set-code::
    .. code-block:: Matlab

        problem.setData('My new datafile', dataRange=[0.1, 0.3])
    
    .. code-block:: Python

        problem.data.set_fields('My new datafile', data_range=[0.1, 0.3])


.. tab-set::
    :class: tab-label-hidden
    :sync-group: code

    .. tab-item:: Matlab
        :sync: Matlab

        .. output:: Matlab

            problem.setData('My new datafile', dataRange=[0.1, 0.3])
            problem.data.displayTable()

    .. tab-item:: Python 
        :sync: Python

        .. output:: Python

            problem.data.set_fields(1, data_range=[0.1, 0.3])
            print(problem.data)


Putting it all together – defining contrasts
============================================

Once we have defined the various aspects of our project, i.e. backgrounds, data and so on, we group these together into contrasts to make our fitting project. 
A contrast defines one 'experimental setup', for example in our hydration/deuteration model we need two contrasts, one for hydration and one for deuteration.
We can add a contrast using just its name, and edit it later, or we can specify which parts of our project we want to add to the contrast using name value pairs:

.. tab-set-code::
    .. code-block:: Matlab

        problem.addContrast('name', 'D-tail/H-Head/D2O',...
                            'background', 'Background D2O',...
                            'resolution', 'Resolution 1',...
                            'scalefactor', 'Scalefactor 1',...
                            'BulkIn', 'SLD Air',...
                            'BulkOut', 'SLD D2O',...
                            'data', 'D-tail / H-head / D2O');
        
    .. code-block:: Python

        problem.contrasts.append(name='D-tail/H-Head/D2O',
                                 background='Background D2O',
                                 resolution='Resolution 1', 
                                 scalefactor='Scalefactor 1',
                                 bulk_in='SLD Air',
                                 bulk_out='SLD D2O',
                                 data='D-tail / H-head / D2O')

The values which we add must refer to names within the other blocks of the project. If the name doesn't exist in the relevant block, an error will be raised. 

Once we have added the contrasts, then we need to set the model, either by adding layers for a ``"standard layers"`` project, 
or a custom model file (we discuss these in :ref:`customModels`). 
In the case of layers, we give a list of layer names, in order from bulk in to bulk out. 
So for a monolayer for example, we would specify tails and then heads as shown below:

.. tab-set-code::
    .. code-block:: Matlab

        problem.setContrast('D-tail/H-Head/D2O', 'model', {'Deuterated Tails', 'Hydrogenated heads'});
    
    .. code-block:: Python

        problem.contrasts.set_fields('D-tail/H-Head/D2O', model=['Deuterated Tails', 'Hydrogenated heads'])

We can also define the layers array beforehand and include it when defining the contrast. Once we have defined our contrasts they appear in the ``contrasts`` block at the end of the project when it is displayed.


*****************************
The Monolayer Example In Full
*****************************
In the previous sections, we showed an example of a pre-loaded problem definition class, which we used to analyse data from two contrasts of a lipid monolayer. Now, rather than loading in a pre-defined version of this problem we can use our class methods to build this from scratch, and do the same analysis as we did there, but this time from a script.

To start, we first make an instance of the **Project** class:

.. tab-set-code::
    .. code-block:: Matlab

        problem = createProject(name='DSPC monolayers');
    
    .. code-block:: Python

        import ratapi as RAT
        problem = RAT.Project(name='DSPC monolayers')

Then we need to define the parameters we need. We'll do this by making a parameters block, and adding these to the project:

.. tab-set-code::
    .. code-block:: Matlab

        % Define the parameters:
        Parameters = {
            %       Name                min     val     max      fit? 
            {'Tails Thickness',         10,     20,      30,     true};
            {'Heads Thickness',          3,     11,      16,     true};
            {'Tails Roughness',          2,     5,       9,      true};
            {'Heads Roughness',          2,     5,       9,      true};
            {'Deuterated Tails SLD',    4e-6,   6e-6,    2e-5,   true};
            {'Hydrogenated Tails SLD', -0.6e-6, -0.4e-6, 0,      true};
            {'Deuterated Heads SLD',    1e-6,   3e-6,    8e-6,   true};
            {'Hydrogenated Heads SLD',  0.1e-6, 1.4e-6,  3e-6,   true};
            {'Heads Hydration',         0,      0.3,     0.5,    true};
            };

        problem.addParameterGroup(Parameters);

    .. code-block:: Python
        
        parameters = [
            ['Tails Thickness', 10, 20, 30, True],
            ['Heads Thickness', 3, 11, 16, True],
            ['Tails Roughness', 2, 5, 9, True],
            ['Heads Roughness', 2, 5, 9, True],
            ['Deuterated Tails SLD', 4e-6, 6e-6, 2e-5, True],
            ['Hydrogenated Tails SLD', -0.6e-6, -0.4e-6, 0, True],
            ['Deuterated Heads SLD', 1e-6, 3e-6, 8e-6, True],
            ['Hydrogenated Heads SLD', 0.1e-6, 1.4e-6, 3e-6, True],
            ['Heads Hydration', 0, 0.3, 0.5, True]
            ]
 
        for param in params:
            problem.parameters.append(name=param[0], min=param[1], value=param[2], max=param[3], fit=param[4])


Next we need to group the parameters into our layers. We need four layers in all, representing deuterated and hydrogenated versions of the heads and tails:

.. tab-set-code::
    .. code-block:: Matlab

        H_Heads = {'Hydrogenated Heads', 'Heads Thickness',...
                   'Hydrogenated Heads SLD', 'Heads Roughness',...
                   'Heads Hydration', 'bulk out' };
                    
        D_Heads = {'Deuterated Heads', 'Heads Thickness',...
                   'Deuterated Heads SLD', 'Heads Roughness',...
                   'Heads Hydration', 'bulk out' };
                    
        D_Tails = {'Deuterated Tails', 'Tails Thickness',...
                   'Deuterated Tails SLD', 'Tails Roughness'};

        H_Tails = {'Hydrogenated Tails', 'Tails Thickness',...
                   'Hydrogenated Tails SLD', 'Tails Roughness'};
    
    .. code-block:: Python
        
        H_Heads = RAT.models.Layer(name='Hydrogenated Heads', thickness='Heads Thickness', 
                                   SLD='Hydrogenated Heads SLD', roughness='Heads Roughness', 
                                   hydration='Heads Hydration', hydrate_with='bulk out')
                    
        D_Heads = RAT.models.Layer(name='Deuterated Heads', thickness='Heads Thickness', 
                                   SLD='Deuterated Heads SLD', roughness='Heads Roughness',
                                   hydration='Heads Hydration', hydrate_with='bulk out')
                    
        D_Tails = RAT.models.Layer(name='Deuterated Tails', thickness='Tails Thickness',
                                   SLD='Deuterated Tails SLD', roughness='Tails Roughness')

        H_Tails = RAT.models.Layer(name='Hydrogenated Tails', thickness='Tails Thickness',
                                   SLD='Hydrogenated Tails SLD', roughness='Tails Roughness')
.. note:: 
    The headgroups are hydrated and so share a hydration parameter, whereas the tails are not. 

We now add our layers to the project:

.. tab-set-code::
    .. code-block:: Matlab

        problem.addLayerGroup({H_Heads; D_Heads; H_Tails; D_Tails});
    
    .. code-block:: Python

        problem.layers.extend([H_Heads, D_Heads, H_Tails, D_Tails])

We are using two different sub-phases: D2O and ACMW. We need a different constant background for each, so we need two background parameters. There is already one background parameter in the project as a default, so we rename this and add a second one:

.. tab-set-code::
    .. code-block:: Matlab

        problem.setBackgroundParamName(1, 'Backs Value ACMW');
        problem.setBackgroundParamValue(1, 5.5e-6);
        problem.addBackgroundParam('Backs Value D2O', 1e-8, 2.8e-6, 1e-5);
    
    .. code-block:: Python
        
        problem.background_parameters.set_fields(0, name='Backs Value ACMW', value=5.5e-6)
        problem.background_parameters.append(name='Backs Value D2O', min=1e-8, value=2.8e-6, max=1e-5)
       
Use these parameters to define two constant backgrounds, again using the existing default for one of them:

.. tab-set-code::
    .. code-block:: Matlab

        problem.addBackground('Background D2O', 'constant', 'Backs Value D2O');
        problem.setBackground(1, 'name', 'Background ACMW', 'value1', 'Backs Value ACMW');
    
    .. code-block:: Python

        problem.backgrounds.append(name='Background D2O', type='constant', source='Backs Value D2O')
        problem.backgrounds.set_fields(0, name='Background ACMW', source='Backs Value ACMW')

We need two sub-phases for our project. D2O is already in the project as a default, so we only need to add the bulk out for ACMW

.. tab-set-code::
    .. code-block:: Matlab

        problem.addBulkOut('SLD ACMW', -0.6e-6, -0.56e-6, -0.3e-6, true);

    .. code-block:: Python

        problem.bulk_out.append(name='SLD ACMW', min=-0.6e-6, value=-0.56e-6, max=-0.3e-6, fit=True)

Now we need to add the data. We read in the two files, and put the data into the ``data`` block with appropriate names:

.. tab-set-code::
    .. code-block:: Matlab

        root = getappdata(0, 'root');
        dataPath = '/examples/miscellaneous/convertRasCAL1Project/';
        d13ACM = readmatrix(fullfile(root, dataPath, 'd13acmw20.dat'));
        d70d2O = readmatrix(fullfile(root, dataPath, 'd70d2o20.dat'));
        problem.addData('H-tail / D-head / ACMW', d13ACM);
        problem.addData('D-tail / H-head / D2O', d70d2O);
    
    .. code-block:: Python

        import numpy as np
        d13ACM = np.loadtxt('d13acmw20.dat', delimiter=",")
        d70d2O = np.loadtxt('d70d2o20.dat', delimiter=",")
        problem.data.append(name='H-tail / D-head / ACMW', data=d13ACM)
        problem.data.append(name='D-tail / H-head / D2O', data=d70d2O)

We have everything we need to now build our contrasts. We have two contrasts in all, and we build them using name / value pairs for all the different parts of the contrasts (i.e. selecting which background and bulk phases etc we need using the names we have given them).
To define the models for each contrast, we list the names of the relevant layers as appropriate.

.. tab-set-code::
    .. code-block:: Matlab

        problem.addContrast('name', 'D-tail/H-Head/D2O',...
                            'background', 'Background D2O',...
                            'resolution', 'Resolution 1',...
                            'scalefactor', 'Scalefactor 1',...
                            'BulkOut', 'SLD D2O',...
                            'BulkIn', 'SLD Air',...
                            'data', 'D-tail / H-head / D2O',...
                            'model', {'Deuterated Tails','Hydrogenated heads'}); 

        problem.addContrast('name', 'H-tail/D-Head/ACMW',...
                            'background', 'Background ACMW',...
                            'resolution', 'Resolution 1',...
                            'scalefactor', 'Scalefactor 1',...
                            'BulkOut', 'SLD ACMW',...
                            'BulkIn', 'SLD Air',...
                            'data', 'H-tail / D-head / ACMW',...
                            'model', {'Hydrogenated Tails','Deuterated Heads'});

    .. code-block:: Python

        problem.contrasts.append(name='D-tail/H-Head/D2O',
                                 background='Background D2O',
                                 resolution='Resolution 1', 
                                 scalefactor='Scalefactor 1',
                                 bulk_out='SLD D2O',
                                 bulk_in='SLD Air',
                                 data='D-tail / H-head / D2O',
                                 model=['Deuterated Tails', 'Hydrogenated Heads'])

        problem.contrasts.append(name='H-tail/D-Head/ACMW',
                                 background='Background ACMW',
                                 resolution='Resolution 1',
                                 scalefactor='Scalefactor 1',
                                 bulk_out='SLD ACMW',
                                 bulk_in='SLD Air',
                                 data='D-tail / H-head / D2O',
                                 model=['Hydrogenated Tails', 'Deuterated Heads'])
    
We need to make sure that we are fitting the relevant backgrounds, scalefactors and bulk phase values:

.. tab-set-code::
    .. code-block:: Matlab

        problem.setBackgroundParam('Backs Value ACMW', 'fit', true);
        problem.setBackgroundParam('Backs Value D2O', 'fit', true);
        problem.setScalefactor('Scalefactor 1', 'fit', true);
        problem.setBulkOut('SLD D2O', 'fit', true);

    .. code-block:: Python

        problem.background_parameters.set_fields('Backs Value ACMW', fit=True)
        problem.background_parameters.set_fields('Backs Value D2O', fit=True)
        problem.scalefactors.set_fields('Scalefactor 1', fit=True)
        problem.bulk_out.set_fields('SLD D2O', fit=True)

Now have a look at our project, to make sure it all looks reasonable:

.. tab-set-code::
    .. code-block:: Matlab

        disp(problem)

    .. code-block:: Python

        print(problem)

.. tab-set::
    :class: tab-label-hidden
    :sync-group: code

    .. tab-item:: Matlab
        :sync: Matlab

        .. output:: Matlab

            problem = load('source/tutorial/data/twoContrastExample.mat');
            problem = problem.problem;
            disp(problem)

    .. tab-item:: Python 
        :sync: Python

        .. output:: Python

            problem = RAT.Project.load("source/tutorial/data/two_contrast_example.json")
            print(problem)

Now we'll calculate this to check the agreement with the data. We need an instance of the controls class, with the procedure attribute set to ``"calculate"`` (the default):

.. tab-set-code::
    .. code-block:: Matlab

        controls = controlsClass();
        disp(controls)
    
    .. code-block:: Python

        controls = RAT.Controls()
        print(controls)

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

We then send all of this to RAT, and plot the output:

.. tab-set-code::
    .. code-block:: Matlab

        [problem, results] = RAT(problem,controls);
    
    .. code-block:: Python

        problem, results = RAT.run(problem, controls)

.. tab-set::
    :class: tab-label-hidden
    :sync-group: code

    .. tab-item:: Matlab
        :sync: Matlab

        .. output:: Matlab

            [problem, results] = RAT(problem,controls);

    .. tab-item:: Python 
        :sync: Python

        .. output:: Python

            problem, results = RAT.run(problem, controls)


.. tab-set-code::
    .. code-block:: Matlab

        figure(1); clf;
        plotRefSLD(problem, results)
    
    .. code-block:: Python

        RAT.plotting.plot_ref_sld(problem, results)
        

.. image:: ../images/tutorial/plotBeforeOptimization.png
    :alt: Displays reflectivity and SLD plot

To do a fit, we change the ``procedure`` attribute of the controls class to ``"simplex"``. We will also change the ``parallel`` option to ``"contrasts"``, so that each contrast gets its own calculation thread, 
and modify the output to only display the final result (rather than each iteration) by setting the ``display`` option to ``"final"`` and then run our fit and plot the results:

.. tab-set-code::
    .. code-block:: Matlab

        controls = controlsClass();
        controls.procedure = 'simplex';
        controls.parallel = 'contrasts';
        controls.display = 'final';
        [problem, results] = RAT(problem, controls);
    
    .. code-block:: Python

        controls = RAT.Controls(procedure='simplex', parallel='contrasts', display='final')
        problem, results = RAT.run(problem, controls)

.. tab-set::
    :class: tab-label-hidden
    :sync-group: code

    .. tab-item:: Matlab
        :sync: Matlab

        .. output:: Matlab

            controls = controlsClass();
            controls.procedure = 'simplex';
            controls.parallel = 'contrasts';
            controls.display = 'final';
            [problem,results] = RAT(problem,controls);

    .. tab-item:: Python 
        :sync: Python

        .. output:: Python

            controls = RAT.Controls(procedure='simplex', parallel='contrasts', display='final')
            problem, results = RAT.run(problem, controls)

.. tab-set-code::
    .. code-block:: Matlab

        disp(results)

    .. code-block:: Python

        print(results)

.. tab-set::
    :class: tab-label-hidden
    :sync-group: code

    .. tab-item:: Matlab
        :sync: Matlab

        .. output:: Matlab

            disp(results)

    .. tab-item:: Python 
        :sync: Python

        .. output:: Python

            print(results)

We can now plot the results of our fit:

.. tab-set-code::
    .. code-block:: Matlab

        figure; clf;
        plotRefSLD(out,results)
    
    .. code-block:: Python

        RAT.plotting.plot_ref_sld(problem, results)

.. image:: ../images/tutorial/plotAfterOptimization.png
    :alt: Displays reflectivity and SLD plot
