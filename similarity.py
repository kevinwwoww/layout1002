from html_similarity import similarity, style_similarity, structural_similarity

html_1 = '''
<!DOCTYPE html>
<!--[if IE 8]><html class="no-js lt-ie9" lang="en" > <![endif]--><!--[if gt IE 8]><!--><html class="no-js" lang="en"><!--<![endif]--><head>
  <meta charset="utf-8"/>
  <meta content="Training and documentation on Luceda Photonics' IPKISS software and photonic IC design automation." name="description"/>
<meta content="Luceda Academy, Photonics Design, Python, AWG, directional coupler, ring resonator, silicon photonics, IPKISS, Caphe, MMI, photonic waveguide, PIC, integrated circuit, Photonics PDK, CAMFR, SiEPICfab, SiEPIC, CORNERSTONE, SOI, SiN, silicon nitride, Ligentec, AMF, wavelength division multiplexing, WDM, mask merging" name="keywords"/>

  <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
  
  <title>Welcome to Luceda Academy — Luceda Academy  documentation</title>
  

  
  
    <link href="_static/academy_hat.png" rel="shortcut icon"/>
  
  
  

  
  <script src="_static/js/modernizr.min.js" type="text/javascript"></script>
  
    
      <script data-url_root="./" id="documentation_options" src="_static/documentation_options.js" type="text/javascript"></script>
        <script data-url_root="./" id="documentation_options" src="_static/documentation_options.js"></script>
        <script src="_static/jquery.js"></script>
        <script src="_static/underscore.js"></script>
        <script src="_static/_sphinx_javascript_frameworks_compat.js"></script>
        <script src="_static/doctools.js"></script>
        <script src="_static/sphinx_highlight.js"></script>
    
    <script src="_static/js/theme.js" type="text/javascript"></script>

    

  
  <link href="_static/css/luceda_theme.css" rel="stylesheet" type="text/css"/>
  <link href="_static/pygments.css" rel="stylesheet" type="text/css"/>
  <link href="_static/pygments.css" rel="stylesheet" type="text/css"/>
  <link href="_static/css/luceda_theme.css" rel="stylesheet" type="text/css"/>
    <link href="genindex.html" rel="index" title="Index"/>
    <link href="search.html" rel="search" title="Search"/>
    <link href="installation.html" rel="next" title="Installation"/> 
</head>

<body class="wy-body-for-nav">

   
  <div class="wy-grid-for-nav">
    
    <nav class="wy-nav-side" data-toggle="wy-nav-shift">
      <div class="wy-side-scroll">
        <div class="wy-side-nav-search">
          

          
            <a href="#">
          

          
            
            <img alt="Logo" class="logo" src="_static/luceda_academy_darkbg_transparent.png"/>
          
          </a>

          
            
            
          

          
<html><head></head><body><p style="text-align: center; font-size:70%; font-family:'Segoe UI';">
      <a class="button button1 buttonsmall" href="/download_samples.html">DOWNLOAD SAMPLES</a>
      <a class="button button3 buttonsmall" href="https://www.lucedaphotonics.com/ipkiss-photonics-design-platform" target="_blank">DISCOVER IPKISS</a>
  </p></body></html><div role="search">
  <form action="search.html" class="wy-form" id="rtd-search-form" method="get">
    <input name="q" placeholder="Search docs" type="text"/>
    <input name="check_keywords" type="hidden" value="yes"/>
    <input name="area" type="hidden" value="default"/>
  </form>
</div>

          
        </div>

        <div aria-label="main navigation" class="wy-menu wy-menu-vertical" data-spy="affix" role="navigation">
          
            
            
              
            
            
              <ul>
<li class="toctree-l1"><a class="reference internal" href="installation.html">Installation</a></li>
<li class="toctree-l1"><a class="reference internal" href="ipkiss_and_luceda_photonics.html">About IPKISS and Luceda Photonics</a></li>
</ul>
<p class="caption" role="heading"><span class="caption-text">Getting started</span></p>
<ul>
<li class="toctree-l1"><a class="reference internal" href="training/getting_started/introduction/index.html">Introduction</a><ul>
<li class="toctree-l2"><a class="reference internal" href="training/getting_started/introduction/index.html#about-this-tutorial">About this tutorial</a></li>
<li class="toctree-l2"><a class="reference internal" href="training/getting_started/introduction/index.html#new-to-python">New to Python?</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="training/getting_started/pcells_views_properties/index.html">PCells, Views and Properties</a><ul>
<li class="toctree-l2"><a class="reference internal" href="training/getting_started/pcells_views_properties/index.html#importing-ipkiss-and-the-technology">Importing IPKISS and the technology</a></li>
<li class="toctree-l2"><a class="reference internal" href="training/getting_started/pcells_views_properties/index.html#a-first-pcell-with-properties">A first PCell with properties</a></li>
<li class="toctree-l2"><a class="reference internal" href="training/getting_started/pcells_views_properties/index.html#properties-with-default-values">Properties with default values</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="training/getting_started/component_mmi/index.html">Design a component: MMI</a><ul>
<li class="toctree-l2"><a class="reference internal" href="training/getting_started/component_mmi/index.html#layout">Layout</a><ul>
<li class="toctree-l3"><a class="reference internal" href="training/getting_started/component_mmi/index.html#visualize-the-layout">Visualize the layout</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/getting_started/component_mmi/index.html#virtual-fabrication-and-cross-section">Virtual fabrication and cross section</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/getting_started/component_mmi/index.html#test-your-knowledge">Test your knowledge</a></li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="training/getting_started/component_mmi/index.html#circuit-model">Circuit Model</a><ul>
<li class="toctree-l3"><a class="reference internal" href="training/getting_started/component_mmi/index.html#netlist-view">Netlist View</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/getting_started/component_mmi/index.html#circuit-model-view">Circuit Model View</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/getting_started/component_mmi/index.html#defining-the-s-matrix">Defining the S-matrix</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/getting_started/component_mmi/index.html#implementing-the-compact-model">Implementing the compact model</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/getting_started/component_mmi/index.html#adding-the-circuit-model-to-the-pcell">Adding the circuit model to the PCell</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="training/getting_started/component_mmi/index.html#simulate-the-mmi">Simulate the MMI</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="training/getting_started/waveguides_connectors/index.html">Waveguides and waveguide connectors</a><ul>
<li class="toctree-l2"><a class="reference internal" href="training/getting_started/waveguides_connectors/index.html#draw-a-waveguide-from-a-trace-template">Draw a waveguide from a trace template</a></li>
<li class="toctree-l2"><a class="reference internal" href="training/getting_started/waveguides_connectors/index.html#routing-functions">Routing functions</a></li>
<li class="toctree-l2"><a class="reference internal" href="training/getting_started/waveguides_connectors/index.html#waveguide-connectors">Waveguide connectors</a></li>
<li class="toctree-l2"><a class="reference internal" href="training/getting_started/waveguides_connectors/index.html#define-a-custom-waveguide-template">Define a custom waveguide template</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="training/getting_started/circuit_splitter_tree/index.html">Design a circuit: splitter tree</a><ul>
<li class="toctree-l2"><a class="reference internal" href="training/getting_started/circuit_splitter_tree/1_splitter_tree_2levels.html">1. Splitter tree with two levels</a><ul>
<li class="toctree-l3"><a class="reference internal" href="training/getting_started/circuit_splitter_tree/1_splitter_tree_2levels.html#ports">1.1. Ports</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/getting_started/circuit_splitter_tree/1_splitter_tree_2levels.html#building-a-circuit-with-i3-circuit">1.2. Building a circuit with i3.Circuit</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/getting_started/circuit_splitter_tree/1_splitter_tree_2levels.html#performing-a-circuit-simulation">1.3. Performing a circuit simulation</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/getting_started/circuit_splitter_tree/1_splitter_tree_2levels.html#test-your-knowledge">1.4. Test your knowledge</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/getting_started/circuit_splitter_tree/1_splitter_tree_2levels.html#adding-a-crossing">1.4.1. Adding a crossing</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="training/getting_started/circuit_splitter_tree/2_adding_fgc.html">2. Adding fiber grating couplers</a><ul>
<li class="toctree-l3"><a class="reference internal" href="training/getting_started/circuit_splitter_tree/2_adding_fgc.html#building-the-circuit">2.1. Building the circuit</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/getting_started/circuit_splitter_tree/2_adding_fgc.html#layout-and-simulation">2.2. Layout and simulation</a></li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="training/getting_started/circuit_splitter_tree/3_splitter_tree_parametric.html">3. Parametric splitter tree</a><ul>
<li class="toctree-l3"><a class="reference internal" href="training/getting_started/circuit_splitter_tree/3_splitter_tree_parametric.html#class-splittertree">3.1. Class SplitterTree</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/getting_started/circuit_splitter_tree/3_splitter_tree_parametric.html#instantiating-and-simulating-the-parametric-splitter">3.2. Instantiating and simulating the parametric splitter</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/getting_started/circuit_splitter_tree/3_splitter_tree_parametric.html#adding-fiber-grating-couplers">3.3. Adding fiber grating couplers</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="training/getting_started/project_setup/index.html">Create a new IPKISS design project</a></li>
</ul>
<p class="caption" role="heading"><span class="caption-text">Tutorials</span></p>
<ul>
<li class="toctree-l1"><a class="reference internal" href="training/topical_training/passive_component_design.html">Passive component design</a><ul>
<li class="toctree-l2"><a class="reference internal" href="training/topical_training/device_optimization_mmi/index.html">1. Multi-mode interferometer (MMI)</a><ul>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/device_optimization_mmi/1_design_structure.html">1.1. Design folder structure</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/device_optimization_mmi/2_mmi_layout.html">1.2. PCell: Layout</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/device_optimization_mmi/2_mmi_layout.html#define-the-pcell">1.2.1. Define the PCell</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/device_optimization_mmi/2_mmi_layout.html#visualize-the-layout">1.2.2. Visualize the layout</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/device_optimization_mmi/2_mmi_layout.html#virtual-fabrication-and-cross-section">1.2.3. Virtual fabrication and cross section</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/device_optimization_mmi/3_mmi_circuit_model.html">1.3. PCell: Circuit Model</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/device_optimization_mmi/3_mmi_circuit_model.html#netlist-view">1.3.1. Netlist View</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/device_optimization_mmi/3_mmi_circuit_model.html#circuit-model-view">1.3.2. Circuit Model View</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/device_optimization_mmi/3_mmi_circuit_model.html#instantiate-the-pcell">1.3.3. Instantiate the PCell</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/device_optimization_mmi/4_mmi_camfr_optimization.html">1.4. MMI simulation and optimization</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/device_optimization_mmi/4_mmi_camfr_optimization.html#simulation-with-camfr">1.4.1. Simulation with CAMFR</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/device_optimization_mmi/4_mmi_camfr_optimization.html#optimization">1.4.2. Optimization</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/device_optimization_mmi/4_mmi_camfr_optimization.html#pcell-of-the-optimized-mmi">1.4.3. PCell of the optimized MMI</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="training/topical_training/mmi_mode_simulation_eme/index.html">2. IPKISS libraries: Enriching foundry components with simulated models</a><ul>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/mmi_mode_simulation_eme/index.html#introduction">2.1. Introduction</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/mmi_mode_simulation_eme/index.html#defining-and-using-a-simulation-recipe-for-the-mmi">2.2. Defining and using a simulation recipe for the MMI</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/mmi_mode_simulation_eme/index.html#test-your-knowledge">2.3. Test your knowledge</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/mmi_mode_simulation_eme/index.html#defining-a-circuit-model-for-a-fixed-mmi">2.4. Defining a circuit model for a (fixed) MMI</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/mmi_mode_simulation_eme/index.html#step-1-implementing-a-compact-model">2.4.1. Step 1: Implementing a compact model</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/mmi_mode_simulation_eme/index.html#step-2-define-a-fixed-pcell">2.4.2. Step 2: Define a fixed PCell</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/mmi_mode_simulation_eme/index.html#step-3-the-regeneration-script">2.4.3. Step 3: The regeneration script</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/mmi_mode_simulation_eme/index.html#try-it-out">2.5. Try it out</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="training/topical_training/routing.html">Routing</a><ul>
<li class="toctree-l2"><a class="reference internal" href="training/topical_training/waveguide_bundle/waveguide_bundle.html">1. Waveguide bundle routing</a><ul>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/waveguide_bundle/waveguide_bundle.html#introduction">1.1. Introduction</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/waveguide_bundle/waveguide_bundle.html#simple-bundle-routing">1.2. Simple bundle routing</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/waveguide_bundle/waveguide_bundle.html#bundle-routing-with-obstacles-avoidance">1.3. Bundle routing with obstacles avoidance</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/waveguide_bundle/waveguide_bundle.html#fanouts">1.3.1. Fanouts</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/waveguide_bundle/waveguide_bundle.html#waveguide-array">1.3.2. Waveguide Array</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="training/topical_training/routing_chip_edge/routing_chip_edge.html">2. Advanced Routing: Routing to the chip edge</a><ul>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/routing_chip_edge/routing_chip_edge.html#introduction">2.1. Introduction</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/routing_chip_edge/routing_chip_edge.html#warm-up">2.2. Warm-up</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/routing_chip_edge/routing_chip_edge.html#routing-to-the-chip-edge">2.3. Routing to the chip edge</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/routing_chip_edge/routing_chip_edge.html#chaining-connectors">2.4. Chaining Connectors</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/routing_chip_edge/routing_chip_edge.html#bundles">2.5. Bundles</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/routing_chip_edge/routing_chip_edge.html#example-1-splitter-tree-north">2.6. Example 1: Splitter Tree North</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/routing_chip_edge/routing_chip_edge.html#step-1-definition-of-the-instances">2.6.1. Step 1: Definition of the instances</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/routing_chip_edge/routing_chip_edge.html#step-2-definition-of-the-placement-and-routing-specifications">2.6.2. Step 2: Definition of the placement and routing specifications</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/routing_chip_edge/routing_chip_edge.html#level">2.6.3. 1 level</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/routing_chip_edge/routing_chip_edge.html#levels">2.6.4. 3 levels</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/routing_chip_edge/routing_chip_edge.html#id1">2.6.5. 6 levels</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/routing_chip_edge/routing_chip_edge.html#example-2-splitter-tree-west">2.7. Example 2: Splitter Tree West</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/routing_chip_edge/routing_chip_edge.html#id2">2.7.1. 1 level</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/routing_chip_edge/routing_chip_edge.html#id3">2.7.2. 3 levels</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/routing_chip_edge/routing_chip_edge.html#id4">2.7.3. 6 levels</a></li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="training/topical_training/working_as_a_team.html">Working as a team</a><ul>
<li class="toctree-l2"><a class="reference internal" href="training/topical_training/working_as_a_team/design_project_management.html">1. Several contributions to one tape-out run</a><ul>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/working_as_a_team/design_project_management.html#introduction">1.1. Introduction</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/working_as_a_team/design_project_management.html#a-design-project-example">1.2. A Design Project Example</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/working_as_a_team/design_project_management.html#the-regenerate-script">1.2.1. The regenerate script</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/working_as_a_team/design_project_management.html#the-merge-script">1.2.2. The merge script</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/working_as_a_team/design_project_management.html#running-the-merging-script">1.2.3. Running the merging script</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/working_as_a_team/design_project_management.html#test-your-knowledge">1.3. Test your knowledge</a></li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="training/topical_training/working_as_a_team/build_library_on_pdk.html">2. Develop and distribute your component library</a><ul>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/working_as_a_team/build_library_on_pdk.html#introduction">2.1. Introduction</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/working_as_a_team/build_library_on_pdk.html#folder-structure-of-the-library">2.2. Folder structure of the library</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/working_as_a_team/build_library_on_pdk.html#version-control">2.3. Version control</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/working_as_a_team/build_library_on_pdk.html#configuration-in-pycharm">2.3.1. Configuration in Pycharm</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/working_as_a_team/build_library_on_pdk.html#saving-your-work">2.3.2. Saving your work</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/working_as_a_team/build_library_on_pdk.html#undoing-changes">2.3.3. Undoing changes</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/working_as_a_team/build_library_on_pdk.html#next-steps">2.3.4. Next steps</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/working_as_a_team/build_library_on_pdk.html#using-the-library-in-multiple-designs">2.4. Using the library in multiple designs</a></li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="training/topical_training/working_as_a_team/library_regression_test.html">3. Test and validate your component library</a><ul>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/working_as_a_team/library_regression_test.html#configuring-the-library-for-testing">3.1. Configuring the library for testing</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/working_as_a_team/library_regression_test.html#adding-component-reference-tests-to-the-library">3.2. Adding component reference tests to the library</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/working_as_a_team/library_regression_test.html#generating-and-checking-the-known-good-reference-files">3.3. Generating and checking the known-good reference files</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/working_as_a_team/library_regression_test.html#running-the-tests">3.4. Running the tests</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/working_as_a_team/library_regression_test.html#updating-tests-after-a-desired-change">3.5. Updating tests after a desired change</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/working_as_a_team/library_regression_test.html#where-to-go-from-here">3.6. Where to go from here</a></li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="training/topical_training/working_as_a_team/library_in_ledit.html">4. Deploying IPKISS libraries and PDKs in L-Edit</a><ul>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/working_as_a_team/library_in_ledit.html#introduction">4.1. Introduction</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/working_as_a_team/library_in_ledit.html#building-the-openaccess-library">4.2. Building the OpenAccess library</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/working_as_a_team/library_in_ledit.html#creating-a-new-design-in-l-edit">4.3. Creating a new design in L-Edit</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/working_as_a_team/library_in_ledit.html#test-your-knowledge">4.4. Test your knowledge</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="training/topical_training/designing_with_a_pdk.html">Designing with an IPKISS PDK</a><ul>
<li class="toctree-l2"><a class="reference internal" href="training/topical_training/siepic_mzi_ybranch/index.html">1. SiEPIC: Mach-Zehnder interferometer with Y-branches</a><ul>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/siepic_mzi_ybranch/1_ybranch.html">1.1. Y-Branch</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/siepic_mzi_ybranch/1_ybranch.html#layout">1.1.1. Layout</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/siepic_mzi_ybranch/1_ybranch.html#circuit-simulation">1.1.2. Circuit simulation</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/siepic_mzi_ybranch/2_mzi.html">1.2. Mach-Zehnder interferometer</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/siepic_mzi_ybranch/2_mzi.html#import-statements">1.2.1. Import statements</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/siepic_mzi_ybranch/2_mzi.html#instantiating-the-components">1.2.2. Instantiating the components</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/siepic_mzi_ybranch/2_mzi.html#optional-the-get-angle-function">1.2.3. (optional) The get_angle function</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/siepic_mzi_ybranch/2_mzi.html#building-the-circuit-with-i3-circuit">1.2.4. Building the circuit with i3.Circuit</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/siepic_mzi_ybranch/2_mzi.html#circuit-layout-and-simulation">1.2.5. Circuit layout and simulation</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/siepic_mzi_ybranch/2_mzi.html#test-your-knowledge">1.2.6. Test your knowledge</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/siepic_mzi_ybranch/3_adding_fgc.html">1.3. Adding fiber grating couplers</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/siepic_mzi_ybranch/3_adding_fgc.html#layout-and-circuit-simulation">1.3.1. Layout and circuit simulation</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="training/topical_training/siepic_mzi_dc_sweep/index.html">2. SiEPIC: Mach-Zehnder interferometer sweep</a><ul>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/siepic_mzi_dc_sweep/1_mzi.html">2.1. Mach-Zehnder interferometer</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/siepic_mzi_dc_sweep/1_mzi.html#pcell-properties">2.1.1. PCell Properties</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/siepic_mzi_dc_sweep/1_mzi.html#cells-placement-and-connections">2.1.2. Cells, placement and connections</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/siepic_mzi_dc_sweep/1_mzi.html#exposed-ports">2.1.3. Exposed ports</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/siepic_mzi_dc_sweep/1_mzi.html#run-the-code">2.1.4. Run the code</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/siepic_mzi_dc_sweep/1_mzi.html#test-your-knowledge">2.1.5. Test your knowledge</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/siepic_mzi_dc_sweep/2_design_variations.html">2.2. Design variations and hierarchical layout</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/siepic_mzi_dc_sweep/2_design_variations.html#parameters-for-the-mzi-sweep">2.2.1. Parameters for the MZI sweep</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/siepic_mzi_dc_sweep/2_design_variations.html#floorplan">2.2.2. Floorplan</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/siepic_mzi_dc_sweep/2_design_variations.html#mzi-sweep">2.2.3. MZI sweep</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/siepic_mzi_dc_sweep/2_design_variations.html#final-design">2.2.4. Final design</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/siepic_mzi_dc_sweep/2_design_variations.html#layout-and-circuit-simulation">2.2.5. Layout and circuit simulation</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/siepic_mzi_dc_sweep/2_design_variations.html#test-your-knowledge">2.2.6. Test your knowledge</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/siepic_mzi_dc_sweep/3_controlling_wg_lengths.html">2.3. Controlling the waveguides length</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/siepic_mzi_dc_sweep/3_controlling_wg_lengths.html#function-to-control-the-delay-length">2.3.1. Function to control the delay length</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/siepic_mzi_dc_sweep/3_controlling_wg_lengths.html#design-variations-controlling-the-delay-length">2.3.2. Design variations controlling the delay length</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/siepic_mzi_dc_sweep/3_controlling_wg_lengths.html#layout-and-circuit-simulation">2.3.3. Layout and circuit simulation</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/siepic_mzi_dc_sweep/3_controlling_wg_lengths.html#test-your-knowledge">2.3.4. Test your knowledge</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="training/topical_training/cornerstone_mzi_sweep/index.html">3. CORNERSTONE SiN: Mach-Zehnder interferometer sweep</a><ul>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/cornerstone_mzi_sweep/1_mzi.html">3.1. Mach-Zehnder interferometer</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cornerstone_mzi_sweep/1_mzi.html#pcell-properties">3.1.1. PCell Properties</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cornerstone_mzi_sweep/1_mzi.html#cells-placement-and-connections">3.1.2. Cells, placement and connections</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cornerstone_mzi_sweep/1_mzi.html#exposed-ports">3.1.3. Exposed ports</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cornerstone_mzi_sweep/1_mzi.html#run-the-code">3.1.4. Run the code</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cornerstone_mzi_sweep/1_mzi.html#test-your-knowledge">3.1.5. Test your knowledge</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/cornerstone_mzi_sweep/2_design_variations.html">3.2. Design variations and hierarchical layout</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cornerstone_mzi_sweep/2_design_variations.html#parameters-for-the-mzi-sweep">3.2.1. Parameters for the MZI sweep</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cornerstone_mzi_sweep/2_design_variations.html#design-frame">3.2.2. Design frame</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cornerstone_mzi_sweep/2_design_variations.html#mzi-sweep">3.2.3. MZI sweep</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cornerstone_mzi_sweep/2_design_variations.html#circuit-design">3.2.4. Circuit design</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cornerstone_mzi_sweep/2_design_variations.html#layout-and-circuit-simulation">3.2.5. Layout and circuit simulation</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cornerstone_mzi_sweep/2_design_variations.html#test-your-knowledge">3.2.6. Test your knowledge</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/cornerstone_mzi_sweep/3_controlling_wg_lengths.html">3.3. Controlling the waveguides length</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cornerstone_mzi_sweep/3_controlling_wg_lengths.html#function-to-control-the-delay-length">3.3.1. Function to control the delay length</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cornerstone_mzi_sweep/3_controlling_wg_lengths.html#design-variations-controlling-the-delay-length">3.3.2. Design variations controlling the delay length</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cornerstone_mzi_sweep/3_controlling_wg_lengths.html#layout-and-circuit-simulation">3.3.3. Layout and circuit simulation</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cornerstone_mzi_sweep/3_controlling_wg_lengths.html#test-your-knowledge">3.3.4. Test your knowledge</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="designs/cwdm_awg_amf/cwdm_awg_amf.html">4. AMF: AWG demultiplexer</a><ul>
<li class="toctree-l3"><a class="reference internal" href="designs/cwdm_awg_amf/cwdm_awg_amf.html#designing-the-awg">4.1. Designing the AWG</a></li>
<li class="toctree-l3"><a class="reference internal" href="designs/cwdm_awg_amf/cwdm_awg_amf.html#preparing-to-tape-out">4.2. Preparing to tape-out</a></li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="designs/opa_shuksan/opa_shuksan.html">5. SiEPIC Shuksan: Optical phased array (OPA)</a><ul>
<li class="toctree-l3"><a class="reference internal" href="designs/opa_shuksan/opa_shuksan.html#laser-source">5.1. Laser source</a></li>
<li class="toctree-l3"><a class="reference internal" href="designs/opa_shuksan/opa_shuksan.html#splitter-tree">5.2. Splitter tree</a></li>
<li class="toctree-l3"><a class="reference internal" href="designs/opa_shuksan/opa_shuksan.html#heated-spirals-matrix">5.3. Heated spirals matrix</a></li>
<li class="toctree-l3"><a class="reference internal" href="designs/opa_shuksan/opa_shuksan.html#grating-couplers-matrix">5.4. Grating couplers matrix</a></li>
<li class="toctree-l3"><a class="reference internal" href="designs/opa_shuksan/opa_shuksan.html#opa1-layout">5.5. OPA1 Layout</a></li>
<li class="toctree-l3"><a class="reference internal" href="designs/opa_shuksan/opa_shuksan.html#opa1-simulation">5.6. OPA1 Simulation</a></li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="designs/four_lane_mzm/four_lane_mzm.html">6. Tyndall ADK: Four-lanes Mach-Zehnder Modulator (MZM)</a><ul>
<li class="toctree-l3"><a class="reference internal" href="designs/four_lane_mzm/four_lane_mzm.html#fully-assembled-design">6.1. Fully assembled design</a></li>
<li class="toctree-l3"><a class="reference internal" href="designs/four_lane_mzm/four_lane_mzm.html#step-1-importing-the-dependencies">6.2. Step 1: Importing the dependencies</a></li>
<li class="toctree-l3"><a class="reference internal" href="designs/four_lane_mzm/four_lane_mzm.html#step-2-instantiating-the-phase-shifter-and-the-splitter">6.3. Step 2: Instantiating the phase shifter and the splitter</a></li>
<li class="toctree-l3"><a class="reference internal" href="designs/four_lane_mzm/four_lane_mzm.html#step-3-instantiating-the-mzm">6.4. Step 3: Instantiating the MZM</a></li>
<li class="toctree-l3"><a class="reference internal" href="designs/four_lane_mzm/four_lane_mzm.html#step-4-instantiating-the-four-lane-mzm">6.5. Step 4: Instantiating the four-lane MZM</a></li>
<li class="toctree-l3"><a class="reference internal" href="designs/four_lane_mzm/four_lane_mzm.html#step-5-instantiating-the-tyndall-adk-packaging-frame">6.6. Step 5: Instantiating the Tyndall ADK packaging frame</a></li>
<li class="toctree-l3"><a class="reference internal" href="designs/four_lane_mzm/four_lane_mzm.html#step-6-routing-to-the-packaging-frame-and-exporting-the-design">6.7. Step 6: Routing to the packaging frame and exporting the design</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l1"><a class="reference external" href="http://docs.lucedaphotonics.com/tutorials/index.html">More tutorials</a></li>
</ul>
<p class="caption" role="heading"><span class="caption-text">Application Examples</span></p>
<ul>
<li class="toctree-l1"><a class="reference internal" href="training/topical_training/filters.html">Filters</a><ul>
<li class="toctree-l2"><a class="reference internal" href="training/topical_training/wdm_transmitter_mzi/wdm_transmitter.html">1. CWDM transmitter using cascaded MZI lattice filters</a><ul>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/wdm_transmitter_mzi/mzi_lattice_filter.html">1.1. MZI lattice filter</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/wdm_transmitter_mzi/mzi_lattice_filter.html#directional-coupler">1.1.1. Directional coupler</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/wdm_transmitter_mzi/mzi_lattice_filter.html#id2">1.1.2. MZI lattice filter</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/wdm_transmitter_mzi/mux2.html">1.2. CWDM based on cascaded MZI lattice filters</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/wdm_transmitter_mzi/mux2.html#designing-our-first-lattice-filter">1.2.1. Designing our first lattice filter</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/wdm_transmitter_mzi/mux2.html#implementing-the-lattice-filter-as-a-class">1.2.2. Implementing the lattice filter as a class</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/wdm_transmitter_mzi/muxn.html">1.3. Four-way WDM</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/wdm_transmitter_mzi/muxn.html#eight-way-wdm">1.4. Eight-way WDM</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/wdm_transmitter_mzi/muxn.html#parametric-wdm">1.5. Parametric WDM</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/wdm_transmitter_mzi/filter_coefficients.html">1.6. Calculating coupler coefficients</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/wdm_transmitter_mzi/filter_coefficients.html#transforming-the-filter">1.6.1. Transforming the filter</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/wdm_transmitter_mzi/test_your_knowledge.html">1.7. Test your knowledge</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/wdm_transmitter_mzi/test_your_knowledge.html#task-1-compact-four-way-demultiplexer">1.7.1. Task 1: Compact Four-Way demultiplexer</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/wdm_transmitter_mzi/test_your_knowledge.html#task-2-maximize-the-extinction-and-insertion-loss-ratio-of-mux2">1.7.2. Task 2: Maximize the extinction (and insertion loss) ratio of Mux2</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="training/topical_training/wbg_temp_sensor/section00_waveguide_grating_temperature_sensor.html">2. Temperature sensing with SOI waveguide Bragg gratings</a><ul>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/wbg_temp_sensor/section01_wbg_basics.html">2.1. WBGs: why and how?</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/wbg_temp_sensor/section01_wbg_basics.html#rationale-for-optical-temperature-sensing-and-wbgs">2.1.1. Rationale for optical temperature sensing and WBGs</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/wbg_temp_sensor/section01_wbg_basics.html#a-successful-wbg-design-what-is-needed-in-ipkiss">2.1.2. A successful WBG design: what is needed in IPKISS?</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/wbg_temp_sensor/section02_unit_cell.html">2.2. Designing a unit cell with IPKISS</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/wbg_temp_sensor/section02_unit_cell.html#importing-a-foundry-pdk">2.2.1. Importing a foundry PDK</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/wbg_temp_sensor/section02_unit_cell.html#define-the-layout-of-the-unit-cell-create-a-new-building-block">2.2.2. Define the layout of the unit cell (+ create a new building block)</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/wbg_temp_sensor/section02_unit_cell.html#calculating-the-s-parameters-of-the-unit-cell-with-camfr">2.2.3. Calculating the S-parameters of the unit cell with CAMFR</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/wbg_temp_sensor/section02_unit_cell.html#fit-and-save-the-s-matrix-coefficients-to-a-txt-file">2.2.4. Fit and save the S-matrix coefficients to a .txt file</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/wbg_temp_sensor/section02_unit_cell.html#define-the-circuit-model-of-the-unit-cell">2.2.5. Define the circuit model of the unit cell</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/wbg_temp_sensor/section03_optimize_temperature_sensitivity.html">2.3. Optimizing the temperature sensitivity</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/wbg_temp_sensor/section03_optimize_temperature_sensitivity.html#configurations-at-lambda-c">2.3.1. Configurations at <span class="math notranslate nohighlight">\(\lambda_c\)</span></a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/wbg_temp_sensor/section03_optimize_temperature_sensitivity.html#find-the-configuration-yielding-the-most-sensitive-temperature-sensor">2.3.2. Find the configuration yielding the most sensitive temperature sensor</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/wbg_temp_sensor/section03_optimize_temperature_sensitivity.html#simulate-the-temperature-sensing-of-the-device">2.3.3. Simulate the temperature sensing of the device</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/wbg_temp_sensor/section04_full_wbg.html">2.4. Creating the WBG layout and circuit model</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/wbg_temp_sensor/section04_full_wbg.html#creating-the-wbg-layout">2.4.1. Creating the WBG layout</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/wbg_temp_sensor/section04_full_wbg.html#creating-the-wbg-circuit-model">2.4.2. Creating the WBG circuit model</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/wbg_temp_sensor/section04_full_wbg.html#test-your-knowledge">2.4.3. Test your knowledge</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/wbg_temp_sensor/section05_full_circuit.html">2.5. Adding fiber couplers: the final working circuit</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/wbg_temp_sensor/section05_full_circuit.html#creating-the-circuit-layout">2.5.1. Creating the circuit layout</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/wbg_temp_sensor/section05_full_circuit.html#simulating-the-final-circuit">2.5.2. Simulating the final circuit</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/wbg_temp_sensor/section05_full_circuit.html#exporting-the-final-layout-to-a-gds-file">2.5.3. Exporting the final layout to a gds file</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="training/topical_training/cwdm_awg/cwdm_awg.html">3. Arrayed waveguide grating (AWG) demultiplexer</a><ul>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/cwdm_awg/1_introduction.html">3.1. Introduction</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cwdm_awg/1_introduction.html#arrayed-waveguide-grating">3.1.1. Arrayed waveguide grating</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cwdm_awg/1_introduction.html#specification-driven-workflow">3.1.2. Specification-driven workflow</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cwdm_awg/1_introduction.html#application-400g-ethernet">3.1.3. Application: 400G Ethernet</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cwdm_awg/1_introduction.html#design-project-structure">3.1.4. Design project structure</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cwdm_awg/1_introduction.html#conclusion">3.1.5. Conclusion</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cwdm_awg/1_introduction.html#test-your-knowledge">3.1.6. Test your knowledge</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/cwdm_awg/2_generation_subcomponents.html">3.2. AWG generation: Subcomponents</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cwdm_awg/2_generation_subcomponents.html#materials">3.2.1. Materials</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cwdm_awg/2_generation_subcomponents.html#slab-template">3.2.2. Slab template</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cwdm_awg/2_generation_subcomponents.html#waveguide-aperture">3.2.3. Waveguide aperture</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cwdm_awg/2_generation_subcomponents.html#multimode-interference-aperture">3.2.4. Multimode interference aperture</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cwdm_awg/2_generation_subcomponents.html#waveguides">3.2.5. Waveguides</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cwdm_awg/2_generation_subcomponents.html#conclusion">3.2.6. Conclusion</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/cwdm_awg/3_generation_synthesis.html">3.3. AWG generation: Synthesis</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cwdm_awg/3_generation_synthesis.html#functional-specifications">3.3.1. Functional specifications</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cwdm_awg/3_generation_synthesis.html#physical-specifications">3.3.2. Physical specifications</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cwdm_awg/3_generation_synthesis.html#subcomponents">3.3.3. Subcomponents</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cwdm_awg/3_generation_synthesis.html#automated-synthesis">3.3.4. Automated Synthesis</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cwdm_awg/3_generation_synthesis.html#parameters-review">3.3.5. Parameters review</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cwdm_awg/3_generation_synthesis.html#storing-the-result">3.3.6. Storing the result</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cwdm_awg/3_generation_synthesis.html#conclusion">3.3.7. Conclusion</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/cwdm_awg/4_generation_assembly.html">3.4. AWG generation: Assembly</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cwdm_awg/4_generation_assembly.html#defining-the-star-couplers">3.4.1. Defining the star couplers</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cwdm_awg/4_generation_assembly.html#routing-the-waveguide-array">3.4.2. Routing the waveguide array</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cwdm_awg/4_generation_assembly.html#awg-assembly">3.4.3. AWG assembly</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/cwdm_awg/5_simulation_and_analysis.html">3.5. AWG simulation and analysis</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cwdm_awg/5_simulation_and_analysis.html#simulation">3.5.1. Simulation</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cwdm_awg/5_simulation_and_analysis.html#analysis">3.5.2. Analysis</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/cwdm_awg/6_finalization.html">3.6. AWG finalization</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cwdm_awg/6_finalization.html#preparing-for-tape-out">3.6.1. Preparing for tape-out</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cwdm_awg/6_finalization.html#using-the-awg-in-a-chip">3.6.2. Using the AWG in a chip</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cwdm_awg/6_finalization.html#conclusion">3.6.3. Conclusion</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/cwdm_awg/6_finalization.html#test-your-knowledge">3.6.4. Test your knowledge</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="training/topical_training/oct_awg/oct_awg.html">4. Arrayed waveguide grating (AWG) for integrated optical coherence tomography</a><ul>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/oct_awg/oct_awg.html#introduction">4.1. Introduction</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/oct_awg/oct_awg.html#generation">4.2. Generation</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/oct_awg/oct_awg.html#subcomponents">4.2.1. Subcomponents</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/oct_awg/oct_awg.html#synthesis">4.2.2. Synthesis</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/oct_awg/oct_awg.html#assembly">4.2.3. Assembly</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/oct_awg/oct_awg.html#simulation-and-analysis">4.3. Simulation and analysis</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/oct_awg/oct_awg.html#finalization">4.4. Finalization</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/oct_awg/oct_awg.html#test-your-knowledge">4.5. Test your knowledge</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="training/topical_training/active_devices.html">Active devices</a><ul>
<li class="toctree-l2"><a class="reference internal" href="training/topical_training/mzm/index.html">1. Mach-Zehnder modulator</a><ul>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/mzm/introduction.html">1.1. Introduction</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/mzm/introduction.html#performance-of-the-modulator">1.1.1. Performance of the modulator</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/mzm/introduction.html#modulator-design-choices">1.1.2. Modulator design choices</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/mzm/phaseshifter.html">1.2. Electro-optic phase modulator</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/mzm/phaseshifter.html#layout">1.2.1. Layout</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/mzm/phaseshifter.html#model">1.2.2. Model</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/mzm/phaseshifter.html#test-your-knowledge">1.2.3. Test your knowledge</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/mzm/heater.html">1.3. Thermo-optic phase shifter (Heater)</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/mzm/heater.html#layout">1.3.1. Layout</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/mzm/heater.html#model">1.3.2. Model</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/mzm/heater.html#test-your-knowledge">1.3.3. Test your knowledge</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/mzm/mzm.html">1.4. Mach-Zehnder modulator (MZM)</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/mzm/mzm.html#layout">1.4.1. Layout</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/mzm/mzm.html#model-and-simulation-recipes">1.4.2. Model and simulation recipes</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/mzm/mzm.html#test-your-knowledge">1.4.3. Test your knowledge</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="training/topical_training/opa/opa.html">2. Optical phased array (OPA)</a><ul>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/opa/opa.html#introduction">2.1. Introduction</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/opa/opa.html#unrouted-opa-visualization-and-simulation">2.2. Unrouted OPA: visualization and simulation</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/opa/opa.html#instantiating-the-parametric-components-of-the-opa">2.2.1. Instantiating the parametric components of the OPA</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/opa/opa.html#instantiating-the-unrouted-opa">2.2.2. Instantiating the unrouted OPA</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/opa/opa.html#unrouted-opa-parametric-cell">2.3. Unrouted OPA: parametric cell</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/opa/opa.html#simulation-recipe">2.4. Simulation recipe</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/opa/opa.html#routed-opa-parametric-cell">2.5. Routed OPA: parametric cell</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/opa/opa.html#routed-opa-visualization-and-simulation">2.6. Routed OPA: visualization and simulation</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/opa/opa.html#conclusion">2.7. Conclusion</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/opa/opa.html#extended-example-electrical-routing-to-two-sides">2.8. Extended example: Electrical routing to two sides</a></li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="training/topical_training/quantum_key_distribution/index.html">3. Quantum key distribution</a><ul>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/quantum_key_distribution/introduction.html">3.1. Introduction</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/quantum_key_distribution/qkd_receiver.html">3.2. The QKD Receiver</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/quantum_key_distribution/qkd_receiver.html#how-the-circuit-works">3.2.1. How the circuit works</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/quantum_key_distribution/qkd_receiver.html#implementation-of-the-circuit-in-ipkiss">3.2.2. Implementation of the circuit in IPKISS</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/quantum_key_distribution/qkd_receiver.html#testbench-and-time-domain-simulations">3.2.3. Testbench and time-domain simulations</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/quantum_key_distribution/qkd_receiver.html#test-your-knowledge">3.2.4. Test your knowledge</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="training/topical_training/ppc/index.html">4. Programmable Photonic Circuit</a><ul>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/ppc/introduction.html">4.1. Introduction</a></li>
<li class="toctree-l3"><a class="reference internal" href="training/topical_training/ppc/ppc_design_simulation.html">4.2. Rectangular PPC</a><ul>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/ppc/ppc_design_simulation.html#mzi-unit-cell">4.2.1. MZI Unit Cell</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/ppc/ppc_design_simulation.html#rectangular-ppc-layout">4.2.2. Rectangular PPC Layout</a></li>
<li class="toctree-l4"><a class="reference internal" href="training/topical_training/ppc/ppc_design_simulation.html#reconfiguring-the-ppc">4.2.3. Reconfiguring the PPC</a></li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
</ul>
<p class="caption" role="heading"><span class="caption-text">Design Kits Doc</span></p>
<ul>
<li class="toctree-l1"><a class="reference internal" href="pdks_sources/si_fab/docs/index.html">SiFab</a><ul>
<li class="toctree-l2"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/index.html">Components</a><ul>
<li class="toctree-l3"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/metal/bondpad/doc/index.html">Bondpad</a><ul>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/metal/bondpad/doc/index.html#id1">BondPad</a></li>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/metal/bondpad/doc/index.html#bondpad-5050">BONDPAD_5050</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/dir_coupler/doc/index.html">Directional coupler</a><ul>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/dir_coupler/doc/index.html#directionalcoupler">DirectionalCoupler</a></li>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/dir_coupler/doc/index.html#sidirectionalcoupleru">SiDirectionalCouplerU</a></li>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/dir_coupler/doc/index.html#sidirectionalcouplers">SiDirectionalCouplerS</a></li>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/dir_coupler/doc/index.html#sindirectionalcouplers">SiNDirectionalCouplerS</a></li>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/dir_coupler/doc/index.html#sidirectionalcouplerupower">SiDirectionalCouplerUPower</a></li>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/dir_coupler/doc/index.html#sidirectionalcouplerspower">SiDirectionalCouplerSPower</a></li>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/dir_coupler/doc/index.html#sindirectionalcouplerspower">SiNDirectionalCouplerSPower</a></li>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/dir_coupler/doc/index.html#simulation-and-regeneration-of-the-data-files">Simulation and regeneration of the data files</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/metal/wire/doc/index.html">Electrical Trace Templates</a><ul>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/metal/wire/doc/index.html#m1wiretemplate">M1WireTemplate</a></li>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/metal/wire/doc/index.html#m1m2viawiretracetemplate">M1M2ViaWireTraceTemplate</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/grating_coupler/doc/index.html">Grating coupler</a><ul>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/grating_coupler/doc/index.html#gratingcoupler">GratingCoupler</a></li>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/grating_coupler/doc/index.html#fc-te-1550">FC_TE_1550</a></li>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/grating_coupler/doc/index.html#fc-te-1300">FC_TE_1300</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/edge_coupler/doc/index.html">Edge coupler</a><ul>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/edge_coupler/doc/index.html#sininvertedtaper">SiNInvertedTaper</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/heater/doc/index.html">Heaters</a><ul>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/heater/doc/index.html#heatedwaveguide">HeatedWaveguide</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/modulator/mzm/doc/index.html">Mach-Zehnder modulator</a><ul>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/modulator/mzm/doc/index.html#mzmodulator">MZModulator</a></li>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/modulator/mzm/doc/index.html#model-and-simulation-recipes">Model and simulation recipes</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/mmi/doc/index.html">Multimode interferometer</a><ul>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/mmi/doc/index.html#mmi1x2">MMI1x2</a></li>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/mmi/doc/index.html#mmi1x2optimized1550">MMI1x2Optimized1550</a></li>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/mmi/doc/index.html#mmi1x2optimized1310">MMI1x2Optimized1310</a></li>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/mmi/doc/index.html#simulation-and-regeneration-of-the-data-files">Simulation and regeneration of the data files</a></li>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/mmi/doc/index.html#creating-a-new-optimized-mmi">Creating a new optimized MMI</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/phase_shifter/doc/index.html">Phase shifters</a><ul>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/phase_shifter/doc/index.html#phaseshifterwaveguide">PhaseShifterWaveguide</a></li>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/phase_shifter/doc/index.html#model-and-simulation-recipes">Model and simulation recipes</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/resistor/doc/index.html">Resistor</a><ul>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/resistor/doc/index.html#id1">Resistor</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/metal/rf/doc/index.html">RF pads</a><ul>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/metal/rf/doc/index.html#probepad">ProbePad</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/spiral/doc/index.html">Spiral waveguide</a><ul>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/spiral/doc/index.html#fixedportwithlengthspiral">FixedPortWithLengthSpiral</a></li>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/spiral/doc/index.html#doublespiralfixedbend">DoubleSpiralFixedBend</a></li>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/spiral/doc/index.html#doublespiralwithincouplingfixedbend">DoubleSpiralWithInCouplingFixedBend</a></li>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/spiral/doc/index.html#fixedlengthspiralfixedbend">FixedLengthSpiralFixedBend</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/metal/via/doc/index.html">Via</a><ul>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/metal/via/doc/index.html#via-m1-m2">VIA_M1_M2</a></li>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/metal/via/doc/index.html#contact">Contact</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/crossing/doc/index.html">Waveguide crossing</a><ul>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/crossing/doc/index.html#crossing">Crossing</a></li>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/crossing/doc/index.html#crossingoptimized">CrossingOptimized</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/waveguides/doc/index.html">Waveguides</a><ul>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/waveguides/doc/index.html#wire-waveguide-templates">Wire waveguide templates</a></li>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/waveguides/doc/index.html#rib-waveguide-templates">Rib waveguide templates</a></li>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/waveguides/doc/index.html#sin-wire-waveguide-templates">SiN wire waveguide templates</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/y_branch/doc/index.html">Y-branch</a><ul>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/y_branch/doc/index.html#ybranch">YBranch</a></li>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/y_branch/doc/index.html#ybranchoptimized">YBranchOptimized</a></li>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/y_branch/doc/index.html#simulation-and-regeneration-of-the-data-files">Simulation and regeneration of the data files</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/fixed_bend/doc/index.html">Waveguide bends</a><ul>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/fixed_bend/doc/index.html#waveguidebend">WaveguideBend</a></li>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/components/fixed_bend/doc/index.html#eulerfixedbend">EulerFixedBend</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/technology/doc/index.html">Technology</a><ul>
<li class="toctree-l3"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/technology/doc/material_models.html">Material models</a><ul>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/technology/doc/material_models.html#model-functions">Model functions</a></li>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab/technology/doc/material_models.html#data-and-fitting">Data and fitting</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab_awg/doc/index.html">AWG components</a><ul>
<li class="toctree-l3"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab_awg/doc/index.html#sislabtemplate">SiSlabTemplate</a><ul>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab_awg/doc/api/si_fab_awg.all.SiSlabTemplate.html">si_fab_awg.all.SiSlabTemplate</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab_awg/doc/index.html#siribaperture">SiRibAperture</a><ul>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab_awg/doc/api/si_fab_awg.all.SiRibAperture.html">si_fab_awg.all.SiRibAperture</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab_awg/doc/index.html#siribmmiaperture">SiRibMMIAperture</a><ul>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/si_fab/si_fab/ipkiss/si_fab_awg/doc/api/si_fab_awg.all.SiRibMMIAperture.html">si_fab_awg.all.SiRibMMIAperture</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="pdks_sources/si_fab/docs/tests.html">Test coverage</a><ul>
<li class="toctree-l3"><a class="reference internal" href="pdks_sources/si_fab/docs/tests.html#file-structure">File structure</a></li>
<li class="toctree-l3"><a class="reference internal" href="pdks_sources/si_fab/docs/tests.html#configuration-files">Configuration files</a></li>
<li class="toctree-l3"><a class="reference internal" href="pdks_sources/si_fab/docs/tests.html#layer-tests">Layer tests</a></li>
<li class="toctree-l3"><a class="reference internal" href="pdks_sources/si_fab/docs/tests.html#component-tests">Component tests</a></li>
<li class="toctree-l3"><a class="reference internal" href="pdks_sources/si_fab/docs/tests.html#awg-designer-tests">AWG Designer tests</a></li>
<li class="toctree-l3"><a class="reference internal" href="pdks_sources/si_fab/docs/tests.html#generating-reference-files">Generating reference files</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="pdks/siepic/siepic.html">IPKISS PDK for SiEPIC</a></li>
<li class="toctree-l1"><a class="reference internal" href="pdks/siepic_shuksan/siepic_shuksan.html">IPKISS PDK for SiEPIC Shuksan</a></li>
<li class="toctree-l1"><a class="reference internal" href="pdks/cornerstone_sin/cornerstone_sin.html">IPKISS PDK for CORNERSTONE SiN</a></li>
<li class="toctree-l1"><a class="reference internal" href="pdks/cornerstone/cornerstone.html">IPKISS PDK for CORNERSTONE SOI</a></li>
<li class="toctree-l1"><a class="reference internal" href="pdks_sources/tyndall_packaging/doc/index.html">IPKISS ADK for Tyndall</a><ul>
<li class="toctree-l2"><a class="reference internal" href="pdks_sources/tyndall_packaging/doc/index.html#usage">Usage</a></li>
<li class="toctree-l2"><a class="reference internal" href="pdks_sources/tyndall_packaging/doc/index.html#reference">Reference</a><ul>
<li class="toctree-l3"><a class="reference internal" href="pdks_sources/tyndall_packaging/doc/index.html#packagingarray">PackagingArray</a><ul>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/tyndall_packaging/doc/api/tyndall_packaging.all.PackagingArray.html">tyndall_packaging.all.PackagingArray</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="pdks_sources/tyndall_packaging/doc/index.html#uniformpackagingarray">UniformPackagingArray</a><ul>
<li class="toctree-l4"><a class="reference internal" href="pdks_sources/tyndall_packaging/doc/api/tyndall_packaging.all.UniformPackagingArray.html">tyndall_packaging.all.UniformPackagingArray</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="pdks_sources/tyndall_packaging/doc/index.html#examples">Examples</a></li>
</ul>
</li>
</ul>
<p class="caption" role="heading"><span class="caption-text">Software Doc</span></p>
<ul>
<li class="toctree-l1"><a class="reference external" href="https://docs.lucedaphotonics.com/">IPKISS documentation</a></li>
</ul>

            
          
        </div>
      </div>
    </nav>

    <section class="wy-nav-content-wrap" data-toggle="wy-nav-shift">

      
      <nav aria-label="top navigation" class="wy-nav-top">
        
          <i class="fa fa-bars" data-toggle="wy-nav-top"></i>
          <a href="#">Luceda Academy</a>
        
      </nav>


      <div class="wy-nav-content">
        
        <div class="rst-content">
        
          















<div aria-label="breadcrumbs navigation" role="navigation">

  <ul class="wy-breadcrumbs">
    
      <li><a href="#">Docs</a> »</li>
        
      <li>Welcome to Luceda Academy</li>
    
    
      <li class="wy-breadcrumbs-aside">
        
            
        
      </li>
    
  </ul>

  
  <hr/>
</div>
          <div class="document" itemscope="itemscope" itemtype="http://schema.org/Article" role="main">
           <div itemprop="articleBody">
            
  <div class="figure align-center">
<a class="reference internal image-reference" href="_images/academy_hat_blue.png"><img alt="Luceda Academy" src="_images/academy_hat_blue.png" style="width: 25%;"/></a>
</div>
<div class="section" id="welcome-to-luceda-academy">
<h1>Welcome to Luceda Academy<a class="headerlink" href="#welcome-to-luceda-academy" title="Permalink to this heading">¶</a></h1>
<h2 style="text-align:center; font-variant:small-caps; font-size:150%; line-height:0px;">Improve your photonic design skills</h2>
<br/><p>Luceda Academy is an online hub where you can find the necessary resources to improve your design skills using all the tools in the Luceda ecosystem.
Whether it is your first time using IPKISS or you are an experienced IPKISS user, this is the right place for you.
Here you will find:</p>
<ul class="simple">
<li><p><strong>Getting started tutorials</strong>, for your first discovery journey through what IPKISS offers.</p></li>
<li><p><strong>Tutorials</strong>, for step-by-step guides to discovering many of the important aspects for designing photonic circuits using IPKISS.
Learn about automating your waveguide routing and building your own internal libraries.</p></li>
<li><p><strong>Application examples</strong>, for an in-depth dive into specific topics and use cases.
Learn about new and exciting applications, such as designing temperature sensors, AWG filters and modulators.</p></li>
</ul>
<p>Request an account to download the Luceda Academy examples and run them directly on your PC.</p>
<p style="text-align: center; font-size:90%; font-family:'Segoe UI';">
  <a class="button button2" href="https://www.lucedaphotonics.com/contactus" target="_blank">REQUEST LUCEDA ACCOUNT</a>
</p>

<h2>Highlights</h2><table class="docutils align-default">
<colgroup>
<col style="width: 50%"/>
<col style="width: 50%"/>
</colgroup>
<tbody>
<tr class="row-odd"><td><p><a class="reference external" href="./training/topical_training/ppc/index.html"><img alt="logo1" src="_images/website_programmable_photonic_circuit.png" style="width: 100%;"/></a></p></td>
<td><p><a class="reference external" href="./training/topical_training/quantum_key_distribution/index.html"><img alt="logo2" src="_images/website_quantum_key_distribution.png" style="width: 100%;"/></a></p></td>
</tr>
</tbody>
</table>
<h2>Luceda Academy PDKs</h2><p>Luceda Academy is built using <strong>SiFab</strong>, a standalone demonstration PDK that looks very much like a foundry PDK.
In the <a class="reference internal" href="pdks_sources/si_fab/docs/index.html#si-fab-documentation"><span class="std std-ref">SiFab</span></a>, you can find</p>
<ul class="simple">
<li><p>a list of all the components with usage examples,</p></li>
<li><p>an overview of the material models used in the PDK technology,</p></li>
<li><p>a list of AWG components enabled for use with the <a href="https://www.lucedaphotonics.com/ipkiss-awg-designer" target="_blank">IPKISS AWG Designer</a> module,</p></li>
<li><p>a documentation of the regression tests implemented to perform continuous quality testing using the <a href="https://www.lucedaphotonics.com/ipkiss-ip-manager" target="_blank">IPKISS IP Manager</a> module.</p></li>
</ul>
<p>In addition, Luceda Academy also contains tutorials based on the following foundry PDKs and Assembly Design Kits (ADKs):</p>
<ul class="simple">
<li><p>IPKISS PDK for CORNERSTONE SOI and SiN</p></li>
<li><p>IPKISS PDK for SiEPIC and SiEPIC Shuksan</p></li>
<li><p>IPKISS PDK for Ligentec AN150</p></li>
<li><p>IPKISS ADK for Tyndall</p></li>
</ul>
<div class="toctree-wrapper compound">
</div>
<div class="toctree-wrapper compound">
</div>
<div class="toctree-wrapper compound">
</div>
<div class="toctree-wrapper compound">
</div>
<div class="toctree-wrapper compound">
</div>
<div class="toctree-wrapper compound">
</div>
</div>


           </div>
           
          </div>
          <footer>
  
    <div aria-label="footer navigation" class="rst-footer-buttons" role="navigation">
      
        <a accesskey="n" class="btn btn-neutral float-right" href="installation.html" rel="next" title="Installation">Next <span class="fa fa-arrow-circle-right"></span></a>
      
      
    </div>
  

  <hr/>

  <div role="contentinfo">
    <p>
        © Copyright 2020, Luceda Photonics - Build date: 2023-01-12 - Luceda Academy version: 3.9-1.1.0

    </p>
  </div>
  Built with <a href="http://sphinx-doc.org/">Sphinx</a> using a <a href="https://github.com/rtfd/sphinx_rtd_theme">theme</a> provided by <a href="https://readthedocs.org">Read the Docs</a>. 

</footer>

        </div>
      </div>

    </section>

  </div>
  


  <script type="text/javascript">
      jQuery(function () {
          SphinxRtdTheme.Navigation.enable(true);
      });
  </script>

  
  
    
    <!-- Theme Analytics -->
    <script>
    (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
      (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
      m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
    })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

    ga('create', 'UA-43898285-6', 'auto');
    ga('send', 'pageview');
    </script>

    
   


</body></html>
'''

html_2 = '''
<!DOCTYPE html>
<html class="writer-html5" lang="en" >
<head>
  <meta charset="utf-8" /><meta name="generator" content="Docutils 0.18.1: http://docutils.sourceforge.net/" />

  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>PhotoCAD User Manual &mdash; PhotoCAD 1.5 documentation</title>
      <link rel="stylesheet" href="_static/pygments.css" type="text/css" />
      <link rel="stylesheet" href="_static/css/theme.css" type="text/css" />
    <link rel="canonical" href="https://photocad-docs.readthedocs.io/en/latest/index.html" />
  <!--[if lt IE 9]>
    <script src="_static/js/html5shiv.min.js"></script>
  <![endif]-->
  
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
        <script data-url_root="./" id="documentation_options" src="_static/documentation_options.js"></script>
        <script src="_static/doctools.js"></script>
        <script src="_static/sphinx_highlight.js"></script>
        <script async="async" src="/_/static/javascript/readthedocs-doc-embed.js"></script>
    <script src="_static/js/theme.js"></script>
    <link rel="index" title="Index" href="genindex.html" />
    <link rel="search" title="Search" href="search.html" />
    <link rel="next" title="Introduction" href="Introduction/index.html" /> 

<!-- RTD Extra Head -->

<link rel="stylesheet" href="/_/static/css/readthedocs-doc-embed.css" type="text/css" />

<script type="application/json" id="READTHEDOCS_DATA">{"ad_free": false, "api_host": "https://readthedocs.org", "build_date": "2023-02-27T06:35:56Z", "builder": "sphinx", "canonical_url": null, "commit": "0e86a32e", "docroot": "/docs/", "features": {"docsearch_disabled": false}, "global_analytics_code": "UA-17997319-1", "language": "en", "page": "index", "programming_language": "words", "project": "photocad-docs", "proxied_api_host": "/_", "source_suffix": ".rst", "subprojects": {"photocad-docszh": "https://photocad-docs.readthedocs.io/zh/latest/"}, "theme": "sphinx_rtd_theme", "user_analytics_code": "", "version": "latest"}</script>

<!--
Using this variable directly instead of using `JSON.parse` is deprecated.
The READTHEDOCS_DATA global variable will be removed in the future.
-->
<script type="text/javascript">
READTHEDOCS_DATA = JSON.parse(document.getElementById('READTHEDOCS_DATA').innerHTML);
</script>

<script type="text/javascript" src="/_/static/javascript/readthedocs-analytics.js" async="async"></script>

<!-- end RTD <extrahead> -->
</head>

<body class="wy-body-for-nav"> 
  <div class="wy-grid-for-nav">
    <nav data-toggle="wy-nav-shift" class="wy-nav-side">
      <div class="wy-side-scroll">
        <div class="wy-side-nav-search" >

          
          
          <a href="#" class="icon icon-home">
            PhotoCAD
          </a>
              <div class="version">
                latest
              </div>
<div role="search">
  <form id="rtd-search-form" class="wy-form" action="search.html" method="get">
    <input type="text" name="q" placeholder="Search docs" aria-label="Search docs" />
    <input type="hidden" name="check_keywords" value="yes" />
    <input type="hidden" name="area" value="default" />
  </form>
</div>
        </div><div class="wy-menu wy-menu-vertical" data-spy="affix" role="navigation" aria-label="Navigation menu">
              <ul>
<li class="toctree-l1"><a class="reference internal" href="Introduction/index.html">Introduction</a><ul>
<li class="toctree-l2"><a class="reference internal" href="Introduction/introduction.html">PhotoCAD Introduction</a><ul>
<li class="toctree-l3"><a class="reference internal" href="Introduction/introduction.html#fnpcell">fnpcell</a></li>
<li class="toctree-l3"><a class="reference internal" href="Introduction/introduction.html#link">link</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="Installation/index.html">Installation</a><ul>
<li class="toctree-l2"><a class="reference internal" href="Installation/installation.html">Installing PhotoCAD</a><ul>
<li class="toctree-l3"><a class="reference internal" href="Installation/installation.html#system-requirement">System Requirement</a></li>
<li class="toctree-l3"><a class="reference internal" href="Installation/installation.html#install-python-ide-and-python-package">Install Python IDE and Python package</a></li>
<li class="toctree-l3"><a class="reference internal" href="Installation/installation.html#install-photocad">Install PhotoCAD</a></li>
<li class="toctree-l3"><a class="reference internal" href="Installation/installation.html#photocad-file-structure">PhotoCAD file structure</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="QuickStart/quickstart.html">QuickStart to PhotoCAD</a></li>
<li class="toctree-l1"><a class="reference internal" href="gpdk_manual/index.html">gpdk</a><ul>
<li class="toctree-l2"><a class="reference internal" href="gpdk_manual/components.html"><strong>Components</strong>: Provided by gpdk</a><ul>
<li class="toctree-l3"><a class="reference internal" href="gpdk_manual/components.html#passive-components">Passive components</a></li>
<li class="toctree-l3"><a class="reference internal" href="gpdk_manual/components.html#active-components">Active components</a></li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="gpdk_manual/examples.html"><strong>Examples</strong>: gpdk-based component building</a></li>
<li class="toctree-l2"><a class="reference internal" href="gpdk_manual/routing.html"><strong>Link</strong>: gpdk-based circuit-level design</a></li>
<li class="toctree-l2"><a class="reference internal" href="gpdk_manual/technology.html"><strong>Technology</strong>: Process related settings in gpdk</a><ul>
<li class="toctree-l3"><a class="reference internal" href="gpdk_manual/technology.html#default-process">Default process</a></li>
<li class="toctree-l3"><a class="reference internal" href="gpdk_manual/technology.html#customized-process">Customized process</a></li>
<li class="toctree-l3"><a class="reference internal" href="gpdk_manual/technology.html#waveguide-information">Waveguide information</a></li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="gpdk_manual/layout01.html"><strong>layout01</strong>: Project Development</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="fnpcell_manual/index.html">fnpcell</a><ul>
<li class="toctree-l2"><a class="reference internal" href="fnpcell_manual/fnpcell_class_definition.html">Definition of each component class in <strong>fnpcell</strong></a><ul>
<li class="toctree-l3"><a class="reference internal" href="fnpcell_manual/fnpcell_class_definition.html#full-script">Full script</a></li>
<li class="toctree-l3"><a class="reference internal" href="fnpcell_manual/fnpcell_class_definition.html#section-script-description">Section Script Description</a></li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="fnpcell_manual/fnpcell_class_generate.html">The use of classes in <strong>fnpcell</strong> (generating components)</a><ul>
<li class="toctree-l3"><a class="reference internal" href="fnpcell_manual/fnpcell_class_generate.html#section-script-description">Section Script Description</a></li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="fnpcell_manual/fnpcell_example.html">Example of using fnpcell to build class</a><ul>
<li class="toctree-l3"><a class="reference internal" href="fnpcell_manual/fnpcell_example.html#example1-bend-bezier-py">Example1: <code class="docutils literal notranslate"><span class="pre">bend_bezier.py</span></code></a><ul>
<li class="toctree-l4"><a class="reference internal" href="fnpcell_manual/fnpcell_example.html#full-script">Full script</a></li>
<li class="toctree-l4"><a class="reference internal" href="fnpcell_manual/fnpcell_example.html#section-script-definition">Section Script Definition</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="fnpcell_manual/fnpcell_example.html#example2-bend-circular-py">Example2: bend_circular.py</a><ul>
<li class="toctree-l4"><a class="reference internal" href="fnpcell_manual/fnpcell_example.html#id1">Full script</a></li>
<li class="toctree-l4"><a class="reference internal" href="fnpcell_manual/fnpcell_example.html#id2">Section Script Definition</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="fnpcell_manual/fnpcell_DRC.html">Design Rule Check(DRC)</a><ul>
<li class="toctree-l3"><a class="reference internal" href="fnpcell_manual/fnpcell_DRC.html#generate-svrftm-template">Generate SVRF<sup>TM</sup> template</a></li>
<li class="toctree-l3"><a class="reference internal" href="fnpcell_manual/fnpcell_DRC.html#generate-drc-template-files-using-svrftm-templates">Generate DRC template files using SVRF<sup>TM</sup> templates</a><ul>
<li class="toctree-l4"><a class="reference internal" href="fnpcell_manual/fnpcell_DRC.html#full-script">Full script</a></li>
<li class="toctree-l4"><a class="reference internal" href="fnpcell_manual/fnpcell_DRC.html#section-script-definition">Section Script Definition</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="fnpcell_manual/fnpcell_DRC.html#using-drc-template-files">Using DRC template files</a></li>
<li class="toctree-l3"><a class="reference internal" href="fnpcell_manual/fnpcell_DRC.html#format-instructions">Format instructions</a></li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="fnpcell_manual/fnpcell_write_pcell.html">Writing a user-defined PCell in PhotoCAD</a><ul>
<li class="toctree-l3"><a class="reference internal" href="fnpcell_manual/fnpcell_write_pcell.html#import-module">Import module</a></li>
<li class="toctree-l3"><a class="reference internal" href="fnpcell_manual/fnpcell_write_pcell.html#define-ringresonator">Define <code class="docutils literal notranslate"><span class="pre">RingResonator</span></code></a></li>
<li class="toctree-l3"><a class="reference internal" href="fnpcell_manual/fnpcell_write_pcell.html#define-ringresonator2">Define <code class="docutils literal notranslate"><span class="pre">RingResonator2</span></code></a></li>
<li class="toctree-l3"><a class="reference internal" href="fnpcell_manual/fnpcell_write_pcell.html#create-examples-layout-units-using-classes-ringresonator-and-ringresonator2">Create examples(layout units) using classes <code class="docutils literal notranslate"><span class="pre">RingResonator</span></code> and <code class="docutils literal notranslate"><span class="pre">RingResonator2</span></code></a></li>
<li class="toctree-l3"><a class="reference internal" href="fnpcell_manual/fnpcell_write_pcell.html#gds-layout">GDS Layout</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="gpdk/QuickCreatePDK.html">Create a customized PDK</a><ul>
<li class="toctree-l2"><a class="reference internal" href="gpdk/components.html">components</a><ul>
<li class="toctree-l3"><a class="reference internal" href="gpdk/straight.html">Straight</a></li>
<li class="toctree-l3"><a class="reference internal" href="gpdk/bend_euler.html">bend_euler</a></li>
<li class="toctree-l3"><a class="reference internal" href="gpdk/grating_coupler.html">grating_coupler</a></li>
<li class="toctree-l3"><a class="reference internal" href="gpdk/mmi.html">MMI</a></li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="gpdk/routing.html">routing</a><ul>
<li class="toctree-l3"><a class="reference internal" href="gpdk/auto_transitioned.html">auto_transitioned</a></li>
<li class="toctree-l3"><a class="reference internal" href="gpdk/comp_scan.html">comp_scan</a></li>
<li class="toctree-l3"><a class="reference internal" href="gpdk/extended.html">extended</a></li>
<li class="toctree-l3"><a class="reference internal" href="gpdk/fanout.html">fanout</a></li>
<li class="toctree-l3"><a class="reference internal" href="gpdk/horizontalized.html">horizontalized</a></li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="gpdk/technology.html">technology</a><ul>
<li class="toctree-l3"><a class="reference internal" href="gpdk/layers_csv.html">layers.csv</a></li>
<li class="toctree-l3"><a class="reference internal" href="gpdk/generate_layers_and_display_from_csv_py.html">generate layers and display from csv file</a></li>
<li class="toctree-l3"><a class="reference internal" href="gpdk/waveguide_factory_py.html">waveguide_factory.py</a><ul>
<li class="toctree-l4"><a class="reference internal" href="gpdk/waveguide_factory_py.html#straight">Straight</a></li>
<li class="toctree-l4"><a class="reference internal" href="gpdk/waveguide_factory_py.html#circularbend">CircularBend</a></li>
<li class="toctree-l4"><a class="reference internal" href="gpdk/waveguide_factory_py.html#eulerbend">EulerBend</a></li>
<li class="toctree-l4"><a class="reference internal" href="gpdk/waveguide_factory_py.html#examples">Examples</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="gpdk/wg_py.html">wg.py</a><ul>
<li class="toctree-l4"><a class="reference internal" href="gpdk/wg_py.html#waveguide-configuration">waveguide configuration</a></li>
<li class="toctree-l4"><a class="reference internal" href="gpdk/wg_py.html#generate-waveguide-class-i">Generate waveguide class I</a></li>
<li class="toctree-l4"><a class="reference internal" href="gpdk/wg_py.html#generate-waveguide-class-ii">Generate waveguide class II</a></li>
<li class="toctree-l4"><a class="reference internal" href="gpdk/wg_py.html#generate-wg-information-to-csv-file">Generate wg information to csv file</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="gpdk/auto_link_py.html">auto_link.py</a><ul>
<li class="toctree-l4"><a class="reference internal" href="gpdk/auto_link_py.html#less-trans"><code class="docutils literal notranslate"><span class="pre">LESS_TRANS</span></code></a></li>
<li class="toctree-l4"><a class="reference internal" href="gpdk/auto_link_py.html#max-swg"><code class="docutils literal notranslate"><span class="pre">MAX_SWG</span></code></a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="gpdk/auto_transition_py.html">auto_transition.py</a></li>
</ul>
</li>
</ul>
</li>
</ul>
<p class="caption" role="heading"><span class="caption-text">Tutorials</span></p>
<ul>
<li class="toctree-l1"><a class="reference internal" href="CreatePcell/index.html">Create Parametrized Cell(PCell)</a><ul>
<li class="toctree-l2"><a class="reference internal" href="CreatePcell/bendeuler.html">BendEuler</a><ul>
<li class="toctree-l3"><a class="reference internal" href="CreatePcell/bendeuler.html#full-script">Full script</a></li>
<li class="toctree-l3"><a class="reference internal" href="CreatePcell/bendeuler.html#section-script-description">Section Script Description</a></li>
<li class="toctree-l3"><a class="reference internal" href="CreatePcell/bendeuler.html#extend-pcells-from-bendeuler">Extend PCells from <code class="docutils literal notranslate"><span class="pre">BendEuler</span></code></a></li>
<li class="toctree-l3"><a class="reference internal" href="CreatePcell/bendeuler.html#export-gds-layout">Export GDS Layout</a></li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="CreatePcell/splitter.html">Splitter</a><ul>
<li class="toctree-l3"><a class="reference internal" href="CreatePcell/splitter.html#full-script">Full Script</a></li>
<li class="toctree-l3"><a class="reference internal" href="CreatePcell/splitter.html#section-script-description">Section Script Description</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="WaveguideRouting/Summary.html">Waveguide Routing</a><ul>
<li class="toctree-l2"><a class="reference internal" href="WaveguideRouting/singleport_to_singleport.html">Single-port to Single-port</a><ul>
<li class="toctree-l3"><a class="reference internal" href="WaveguideRouting/singleport_to_singleport.html#examples">Examples</a></li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="WaveguideRouting/multiport_to_multiport.html">Multi-port to Multi-port</a><ul>
<li class="toctree-l3"><a class="reference internal" href="WaveguideRouting/multiport_to_multiport.html#fp-linked-example-recommendation"><code class="docutils literal notranslate"><span class="pre">fp.Linked</span></code> example ( Recommendation★★★ )</a></li>
<li class="toctree-l3"><a class="reference internal" href="WaveguideRouting/multiport_to_multiport.html#fp-create-links-example-recommendation"><code class="docutils literal notranslate"><span class="pre">fp.create_links</span></code> example ( Recommendation★★★★★ )</a></li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="WaveguideRouting/routing_way.html">Routing Path Selection</a><ul>
<li class="toctree-l3"><a class="reference internal" href="WaveguideRouting/routing_way.html#waylines"><code class="docutils literal notranslate"><span class="pre">waylines</span></code></a><ul>
<li class="toctree-l4"><a class="reference internal" href="WaveguideRouting/routing_way.html#example-1">example 1</a></li>
<li class="toctree-l4"><a class="reference internal" href="WaveguideRouting/routing_way.html#example-2">example 2</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="WaveguideRouting/routing_way.html#waypoints"><code class="docutils literal notranslate"><span class="pre">waypoints</span></code></a></li>
<li class="toctree-l3"><a class="reference internal" href="WaveguideRouting/routing_way.html#target-length"><code class="docutils literal notranslate"><span class="pre">Target_length</span></code></a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="example_manual/routing_list.html">Advanced Routing</a><ul>
<li class="toctree-l2"><a class="reference internal" href="example_manual/routing_automation.html">Routing automation between components ports</a><ul>
<li class="toctree-l3"><a class="reference internal" href="example_manual/example_linked.py.html">Linked</a><ul>
<li class="toctree-l4"><a class="reference internal" href="example_manual/example_linked.py.html#full-script">Full Script</a></li>
<li class="toctree-l4"><a class="reference internal" href="example_manual/example_linked.py.html#section-script-description">Section Script Description</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="example_manual/example_linked_elec.py.html">Linked Electrical Pad</a><ul>
<li class="toctree-l4"><a class="reference internal" href="example_manual/example_linked_elec.py.html#full-script">Full script</a></li>
<li class="toctree-l4"><a class="reference internal" href="example_manual/example_linked_elec.py.html#parameters-and-testing-descriptions">Parameters and testing descriptions</a></li>
<li class="toctree-l4"><a class="reference internal" href="example_manual/example_linked_elec.py.html#connections">Connections</a><ul>
<li class="toctree-l5"><a class="reference internal" href="example_manual/example_linked_elec.py.html#top-connection">Top connection</a></li>
<li class="toctree-l5"><a class="reference internal" href="example_manual/example_linked_elec.py.html#middle-connection">Middle connection</a></li>
<li class="toctree-l5"><a class="reference internal" href="example_manual/example_linked_elec.py.html#bottom-connection">Bottom connection</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="example_manual/auto_transitioned.py.html">AutoTransitioned</a></li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="example_manual/batch_form_routing.html">Routing in batch form</a><ul>
<li class="toctree-l3"><a class="reference internal" href="example_manual/comp_scan.py.html">Components Scan</a><ul>
<li class="toctree-l4"><a class="reference internal" href="example_manual/comp_scan.py.html#full-script">Full script</a></li>
<li class="toctree-l4"><a class="reference internal" href="example_manual/comp_scan.py.html#section-script-definition">Section Script Definition</a><ul>
<li class="toctree-l5"><a class="reference internal" href="example_manual/comp_scan.py.html#importing-python-libraries-and-functional-modules-of-photocad">Importing python libraries and functional modules of PhotoCAD</a></li>
<li class="toctree-l5"><a class="reference internal" href="example_manual/comp_scan.py.html#define-device-adaptation-fiber-coupling-constant-fiber-coupler-and-several-other-classes">Define device adaptation, fiber coupling, constant fiber coupler and several other classes</a></li>
<li class="toctree-l5"><a class="reference internal" href="example_manual/comp_scan.py.html#define-the-batch-class-block">Define the batch class <code class="docutils literal notranslate"><span class="pre">Block</span></code></a></li>
<li class="toctree-l5"><a class="reference internal" href="example_manual/comp_scan.py.html#define-alignment">Define <code class="docutils literal notranslate"><span class="pre">Alignment</span></code></a></li>
<li class="toctree-l5"><a class="reference internal" href="example_manual/comp_scan.py.html#define-title">Define <code class="docutils literal notranslate"><span class="pre">Title</span></code></a></li>
<li class="toctree-l5"><a class="reference internal" href="example_manual/comp_scan.py.html#define-blank">Define <code class="docutils literal notranslate"><span class="pre">Blank</span></code></a></li>
<li class="toctree-l5"><a class="reference internal" href="example_manual/comp_scan.py.html#define-method-to-get-the-port-center">Define method to get the port center</a></li>
<li class="toctree-l5"><a class="reference internal" href="example_manual/comp_scan.py.html#define-methods-for-obtaining-module-content">Define methods for obtaining module content</a></li>
<li class="toctree-l5"><a class="reference internal" href="example_manual/comp_scan.py.html#define-compscan">Define <code class="docutils literal notranslate"><span class="pre">CompScan</span></code></a></li>
<li class="toctree-l5"><a class="reference internal" href="example_manual/comp_scan.py.html#define-compscanbuilder">Define <code class="docutils literal notranslate"><span class="pre">CompScanBuilder</span></code></a></li>
<li class="toctree-l5"><a class="reference internal" href="example_manual/comp_scan.py.html#create-the-component-and-export-the-layout">Create the component and export the layout</a></li>
</ul>
</li>
<li class="toctree-l4"><a class="reference internal" href="example_manual/comp_scan.py.html#script-description">Script Description</a></li>
<li class="toctree-l4"><a class="reference internal" href="example_manual/comp_scan.py.html#gds-layout">GDS Layout</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="example_manual/expand_footprint.html">Expand the footprint for downstream devices</a><ul>
<li class="toctree-l3"><a class="reference internal" href="example_manual/h_fanout.py.html">Hfanout</a><ul>
<li class="toctree-l4"><a class="reference internal" href="example_manual/h_fanout.py.html#full-script">Full script</a></li>
<li class="toctree-l4"><a class="reference internal" href="example_manual/h_fanout.py.html#section-script-definition">Section Script Definition</a><ul>
<li class="toctree-l5"><a class="reference internal" href="example_manual/h_fanout.py.html#importing-libraries-and-modules">Importing libraries and modules</a></li>
<li class="toctree-l5"><a class="reference internal" href="example_manual/h_fanout.py.html#define-hfanout">Define <code class="docutils literal notranslate"><span class="pre">HFanout</span></code></a></li>
<li class="toctree-l5"><a class="reference internal" href="example_manual/h_fanout.py.html#create-components-and-export-layouts">Create components and export layouts</a></li>
</ul>
</li>
<li class="toctree-l4"><a class="reference internal" href="example_manual/h_fanout.py.html#gds-layout">GDS Layout</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="example_manual/horizontalization.html">Horizontalization of device ports</a><ul>
<li class="toctree-l3"><a class="reference internal" href="example_manual/horizontalized.py.html">Horizontalization</a><ul>
<li class="toctree-l4"><a class="reference internal" href="example_manual/horizontalized.py.html#full-script">Full script</a></li>
<li class="toctree-l4"><a class="reference internal" href="example_manual/horizontalized.py.html#section-script-definition">Section Script Definition</a><ul>
<li class="toctree-l5"><a class="reference internal" href="example_manual/horizontalized.py.html#create-horizontalized-components-ports-and-export-layouts">Create horizontalized components ports and export layouts</a></li>
</ul>
</li>
<li class="toctree-l4"><a class="reference internal" href="example_manual/horizontalized.py.html#gds-layout">GDS Layout</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="example_manual/extend.html">Extension of the ports</a><ul>
<li class="toctree-l3"><a class="reference internal" href="example_manual/extended.py.html">Extended</a><ul>
<li class="toctree-l4"><a class="reference internal" href="example_manual/extended.py.html#full-script">Full script</a></li>
<li class="toctree-l4"><a class="reference internal" href="example_manual/extended.py.html#section-script-definition">Section Script Definition</a><ul>
<li class="toctree-l5"><a class="reference internal" href="example_manual/extended.py.html#create-extended-ports-and-export-layout">Create extended ports and export layout</a></li>
</ul>
</li>
<li class="toctree-l4"><a class="reference internal" href="example_manual/extended.py.html#gds-layout">GDS Layout</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="example_manual/advanced_routing_example.html">More routing examples</a><ul>
<li class="toctree-l3"><a class="reference internal" href="example_manual/example_link_between.py.html">LinkBetween</a><ul>
<li class="toctree-l4"><a class="reference internal" href="example_manual/example_link_between.py.html#import-function-module">Import function module</a></li>
<li class="toctree-l4"><a class="reference internal" href="example_manual/example_link_between.py.html#main-function">Main function</a></li>
<li class="toctree-l4"><a class="reference internal" href="example_manual/example_link_between.py.html#define-function">Define function</a></li>
<li class="toctree-l4"><a class="reference internal" href="example_manual/example_link_between.py.html#test-for-waypoints-in-linkbetween">Test for <code class="docutils literal notranslate"><span class="pre">waypoints</span></code> in <code class="docutils literal notranslate"><span class="pre">LinkBetween</span></code></a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="example_manual/example_link_smooth.py.html">LinkSmooth</a><ul>
<li class="toctree-l4"><a class="reference internal" href="example_manual/example_link_smooth.py.html#full-script">Full script</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="example_manual/example_linked_splitter.py.html">LinkedSplitter</a><ul>
<li class="toctree-l4"><a class="reference internal" href="example_manual/example_linked_splitter.py.html#full-script">Full script</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="example_manual/example_linked_elec2.py.html">Linked Electrical wire</a><ul>
<li class="toctree-l4"><a class="reference internal" href="example_manual/example_linked_elec2.py.html#full-script">Full script</a></li>
<li class="toctree-l4"><a class="reference internal" href="example_manual/example_linked_elec2.py.html#parameters-and-testing-description">Parameters and testing description</a><ul>
<li class="toctree-l5"><a class="reference internal" href="example_manual/example_linked_elec2.py.html#components-positioning">Components positioning</a></li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="example_manual/component_list.html">Component</a><ul>
<li class="toctree-l2"><a class="reference internal" href="example_manual/example_phase_shifter.py.html">Phase Shifter</a><ul>
<li class="toctree-l3"><a class="reference internal" href="example_manual/example_phase_shifter.py.html#full-script">Full script</a></li>
<li class="toctree-l3"><a class="reference internal" href="example_manual/example_phase_shifter.py.html#segment-description">Segment Description</a><ul>
<li class="toctree-l4"><a class="reference internal" href="example_manual/example_phase_shifter.py.html#import-function-module">1. Import function module</a></li>
<li class="toctree-l4"><a class="reference internal" href="example_manual/example_phase_shifter.py.html#main-function">2. Main function</a></li>
<li class="toctree-l4"><a class="reference internal" href="example_manual/example_phase_shifter.py.html#define-function">3. Define function</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="example_manual/example_sampler_periodic.py.html">Sampler Periodic</a><ul>
<li class="toctree-l3"><a class="reference internal" href="example_manual/example_sampler_periodic.py.html#full-script">Full script</a></li>
<li class="toctree-l3"><a class="reference internal" href="example_manual/example_sampler_periodic.py.html#left-graph">Left graph</a></li>
<li class="toctree-l3"><a class="reference internal" href="example_manual/example_sampler_periodic.py.html#right-graph">Right graph</a></li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="example_manual/directional_coupler_bend.py.html">Directional Coupler Bend</a><ul>
<li class="toctree-l3"><a class="reference internal" href="example_manual/directional_coupler_bend.py.html#full-script">Full script</a></li>
<li class="toctree-l3"><a class="reference internal" href="example_manual/directional_coupler_bend.py.html#parameter-description">Parameter description</a></li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="example_manual/example_elliptical_rings.py.html">Elliptical Rings</a><ul>
<li class="toctree-l3"><a class="reference internal" href="example_manual/example_elliptical_rings.py.html#full-script">Full script</a></li>
<li class="toctree-l3"><a class="reference internal" href="example_manual/example_elliptical_rings.py.html#fp-el-ring-description">fp.el.Ring Description</a></li>
<li class="toctree-l3"><a class="reference internal" href="example_manual/example_elliptical_rings.py.html#fp-el-ellipticalring-description">fp.el.EllipticalRing Description</a></li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="example_manual/ring_filter.html">Ring filter</a><ul>
<li class="toctree-l3"><a class="reference internal" href="example_manual/ring_filter.html#full-script">Full script</a></li>
<li class="toctree-l3"><a class="reference internal" href="example_manual/ring_filter.html#parameters-and-testing-descriptions">Parameters and testing descriptions</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="Tutorials/Quickstart.html">Quick Start: Create a Circuit</a><ul>
<li class="toctree-l2"><a class="reference internal" href="Tutorials/Step1.html">Step 1: Build basic building blocks</a><ul>
<li class="toctree-l3"><a class="reference internal" href="Tutorials/Step1.html#bend">Bend</a></li>
<li class="toctree-l3"><a class="reference internal" href="Tutorials/Step1.html#straight">Straight</a></li>
<li class="toctree-l3"><a class="reference internal" href="Tutorials/Step1.html#taper">Taper</a></li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="Tutorials/Step2.html">Step 2: Build basic circuits with basic building blocks</a><ul>
<li class="toctree-l3"><a class="reference internal" href="Tutorials/Step2.html#directionalcoupler">DirectionalCoupler</a></li>
<li class="toctree-l3"><a class="reference internal" href="Tutorials/Step2.html#mmi">MMI</a></li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="Tutorials/Step3.html">Step 3: Build complex circuits using basic building blocks</a><ul>
<li class="toctree-l3"><a class="reference internal" href="Tutorials/Step3.html#target-length">target_length</a></li>
<li class="toctree-l3"><a class="reference internal" href="Tutorials/Step3.html#waypoints">waypoints</a></li>
<li class="toctree-l3"><a class="reference internal" href="Tutorials/Step3.html#waylines">waylines</a></li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="Tutorials/Step4.html">Step 4: Drawing of common shapes and layout design by Boolean operations</a><ul>
<li class="toctree-l3"><a class="reference internal" href="Tutorials/Step4.html#commonly-used-shape">Commonly_used_shape</a><ul>
<li class="toctree-l4"><a class="reference internal" href="Tutorials/Step4.html#rectangle">Rectangle</a></li>
<li class="toctree-l4"><a class="reference internal" href="Tutorials/Step4.html#circle">Circle</a></li>
<li class="toctree-l4"><a class="reference internal" href="Tutorials/Step4.html#polygon">Polygon</a></li>
<li class="toctree-l4"><a class="reference internal" href="Tutorials/Step4.html#ring">Ring</a></li>
<li class="toctree-l4"><a class="reference internal" href="Tutorials/Step4.html#regular-polygon">Regular_Polygon</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="Tutorials/Step4.html#boolean-operation">Boolean_operation</a><ul>
<li class="toctree-l4"><a class="reference internal" href="Tutorials/Step4.html#or">OR</a></li>
<li class="toctree-l4"><a class="reference internal" href="Tutorials/Step4.html#and">AND</a></li>
<li class="toctree-l4"><a class="reference internal" href="Tutorials/Step4.html#not">NOT</a></li>
<li class="toctree-l4"><a class="reference internal" href="Tutorials/Step4.html#xor">XOR</a></li>
<li class="toctree-l4"><a class="reference internal" href="Tutorials/Step4.html#examples">Examples</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="Tutorials/Step5.html">Step 5: Example(MMI Tree)</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="export_netlist_manual/index.html">Export Netlist</a><ul>
<li class="toctree-l2"><a class="reference internal" href="export_netlist_manual/implementation.html">Export netlist implementation</a></li>
<li class="toctree-l2"><a class="reference internal" href="export_netlist_manual/description.html">Descriptions of the contents in the netlist</a><ul>
<li class="toctree-l3"><a class="reference internal" href="export_netlist_manual/description.html#create-components-and-export-layouts">Create components and export layouts</a></li>
<li class="toctree-l3"><a class="reference internal" href="export_netlist_manual/description.html#submodules">Submodules</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="jupyter_notebook/index.html">Visualize in Jupyter Notebook</a><ul>
<li class="toctree-l2"><a class="reference internal" href="jupyter_notebook/mzi_post_sim_example.html">MZI circuit layout generation and simulation in Jupyter notebook</a><ul>
<li class="toctree-l3"><a class="reference internal" href="jupyter_notebook/mzi_post_sim_example.html#create-a-jupyter-notebook">Create a Jupyter Notebook</a></li>
<li class="toctree-l3"><a class="reference internal" href="jupyter_notebook/mzi_post_sim_example.html#code-cell-markdown-cell">Code cell &amp; Markdown cell</a></li>
<li class="toctree-l3"><a class="reference internal" href="jupyter_notebook/mzi_post_sim_example.html#generate-mzi-layout">Generate MZI layout</a></li>
<li class="toctree-l3"><a class="reference internal" href="jupyter_notebook/mzi_post_sim_example.html#mzi-post-layout-simulation">MZI Post-layout simulation</a></li>
</ul>
</li>
</ul>
</li>
</ul>
<p class="caption" role="heading"><span class="caption-text">Examples</span></p>
<ul>
<li class="toctree-l1"><a class="reference internal" href="PICircuits/PICircuits.html">Programmable Photonic Integrated Circuit</a><ul>
<li class="toctree-l2"><a class="reference internal" href="PICircuits/PICircuits.html#part-i-building-a-rectangular-network">Part I. Building a Rectangular Network</a></li>
<li class="toctree-l2"><a class="reference internal" href="PICircuits/PICircuits.html#part-ii-parameter-description">Part II. Parameter Description</a></li>
<li class="toctree-l2"><a class="reference internal" href="PICircuits/PICircuits.html#part-iii-test-description">Part III. Test Description</a></li>
<li class="toctree-l2"><a class="reference internal" href="PICircuits/PICircuits.html#part-iv-summary">Part IV. Summary</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="example_manual/triangle_mzi.py.html">Triangle MZI mesh</a><ul>
<li class="toctree-l2"><a class="reference internal" href="example_manual/triangle_mzi.py.html#part-i-build-mzi-units">Part I. Build MZI units</a></li>
<li class="toctree-l2"><a class="reference internal" href="example_manual/triangle_mzi.py.html#part-ii-build-programmable-triangular-mzi-mesh">Part II. Build programmable triangular MZI mesh</a><ul>
<li class="toctree-l3"><a class="reference internal" href="example_manual/triangle_mzi.py.html#mzi-mesh-with-8-external-optical-ports-mzi-triangle-mesh">MZI Mesh with 8 external optical ports (MZI_triangle_mesh)</a></li>
<li class="toctree-l3"><a class="reference internal" href="example_manual/triangle_mzi.py.html#mzi-mesh-with-8-grating-couplers-mzi-triangle-mesh-with-gc">MZI Mesh with 8 Grating Couplers (MZI_triangle_mesh_with_GC)</a></li>
<li class="toctree-l3"><a class="reference internal" href="example_manual/triangle_mzi.py.html#triangle-mzi-array-mzi-triangle-array">Triangle MZI array (MZI_triangle_array)</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="example_manual/example_demultiplexer2.py.html">Demultiplexer</a><ul>
<li class="toctree-l2"><a class="reference internal" href="example_manual/example_demultiplexer2.py.html#full-script">Full script</a></li>
<li class="toctree-l2"><a class="reference internal" href="example_manual/example_demultiplexer2.py.html#view-gds-layout-file">View GDS layout file</a></li>
<li class="toctree-l2"><a class="reference internal" href="example_manual/example_demultiplexer2.py.html#instantiation-of-components">Instantiation of components</a></li>
<li class="toctree-l2"><a class="reference internal" href="example_manual/example_demultiplexer2.py.html#testing-and-analysis">Testing and Analysis</a></li>
<li class="toctree-l2"><a class="reference internal" href="example_manual/example_demultiplexer2.py.html#summary">Summary</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="post_simulation/index.html">Post Layout Simulation</a><ul>
<li class="toctree-l2"><a class="reference internal" href="post_simulation/sim_model.html">Types of simulation model commonly used in <strong>PhotoCAD</strong></a><ul>
<li class="toctree-l3"><a class="reference internal" href="post_simulation/sim_model.html#smatrixwavelengthmodel"><code class="docutils literal notranslate"><span class="pre">SMatrixWavelengthModel</span></code></a></li>
<li class="toctree-l3"><a class="reference internal" href="post_simulation/sim_model.html#externalfilemodel"><code class="docutils literal notranslate"><span class="pre">ExternalFileModel</span></code></a></li>
<li class="toctree-l3"><a class="reference internal" href="post_simulation/sim_model.html#specific-component-simulation-model">Specific component simulation model</a></li>
<li class="toctree-l3"><a class="reference internal" href="post_simulation/sim_model.html#summary">Summary</a></li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="post_simulation/theoretical_parameters.html"><code class="docutils literal notranslate"><span class="pre">wg.py</span></code> configuration</a></li>
<li class="toctree-l2"><a class="reference internal" href="post_simulation/example_mzi.html">MZI simulation</a><ul>
<li class="toctree-l3"><a class="reference internal" href="post_simulation/example_mzi.html#full-script">Full script</a></li>
<li class="toctree-l3"><a class="reference internal" href="post_simulation/example_mzi.html#build-class-circuitmzi">Build Class <code class="docutils literal notranslate"><span class="pre">CircuitMzi</span></code></a></li>
<li class="toctree-l3"><a class="reference internal" href="post_simulation/example_mzi.html#post-layout-simulation">Post-layout simulation</a></li>
</ul>
</li>
</ul>
</li>
</ul>
<p class="caption" role="heading"><span class="caption-text">Support and Changelog</span></p>
<ul>
<li class="toctree-l1"><a class="reference internal" href="Release_notes/index.html">Release notes</a><ul>
<li class="toctree-l2"><a class="reference internal" href="Release_notes/Release_notes_PhotoCAD_V150.html">PhotoCAD V1.5.0</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="Frequent_question/index.html">Frequently Asked Questions</a><ul>
<li class="toctree-l2"><a class="reference internal" href="Frequent_question/data_compression.html">Data Compression</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="AboutUS.html">About Us</a></li>
</ul>

        </div>
      </div>
    </nav>

    <section data-toggle="wy-nav-shift" class="wy-nav-content-wrap"><nav class="wy-nav-top" aria-label="Mobile navigation menu" >
          <i data-toggle="wy-nav-top" class="fa fa-bars"></i>
          <a href="#">PhotoCAD</a>
      </nav>

      <div class="wy-nav-content">
        <div class="rst-content">
          <div role="navigation" aria-label="Page navigation">
  <ul class="wy-breadcrumbs">
      <li><a href="#" class="icon icon-home" aria-label="Home"></a></li>
      <li class="breadcrumb-item active">PhotoCAD User Manual</li>
      <li class="wy-breadcrumbs-aside">
              <a href="https://github.com/Latitudeda/PhotoCAD_Docs/blob/main/docs/index.rst" class="fa fa-github"> Edit on GitHub</a>
      </li>
  </ul>
  <hr/>
</div>
          <div role="main" class="document" itemscope="itemscope" itemtype="http://schema.org/Article">
           <div itemprop="articleBody">
             
  <section id="photocad-user-manual">
<h1>PhotoCAD User Manual<a class="headerlink" href="#photocad-user-manual" title="Permalink to this heading"></a></h1>
<p><strong>PhotoCAD</strong> is written in Python, a language widely used in the photonics industry, and the algorithms used to generate the layout are carefully optimized and researched by the developers, giving it a unique advantage over similar tools at home and abroad, such as no distortion or tearing of the layout at any angle. <strong>fnpcell</strong> and <strong>link</strong> are the two main tools of <strong>PhotoCAD</strong>, which correspond to the parametric cell layout and circuit-level layout in photonics chip layout design.</p>
<p>For beginners who wants to create a PIC by themselves by using <strong>PhotoCAD</strong>, we recommend to look through the <code class="docutils literal notranslate"><span class="pre">TUTORIALS</span></code> section, and you can get a quick glimpse from creating PCells to building your own circuits.</p>
<p>There are also several applications created by <strong>Latitudeda</strong> in the <code class="docutils literal notranslate"><span class="pre">EXAMPLES</span></code> section, users could also browse the examples to get an imagination how can <strong>PhotoCAD</strong> realize your ideas.</p>
<div class="toctree-wrapper compound">
</div>
<div class="toctree-wrapper compound">
</div>
<div class="toctree-wrapper compound">
</div>
<div class="toctree-wrapper compound">
</div>
</section>


           </div>
          </div>
          <footer><div class="rst-footer-buttons" role="navigation" aria-label="Footer">
        <a href="Introduction/index.html" class="btn btn-neutral float-right" title="Introduction" accesskey="n" rel="next">Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span></a>
    </div>

  <hr/>

  <div role="contentinfo">
    <p>&#169; Copyright 2022, Latitudeda.com.
      <span class="commit">Revision <code>0e86a32e</code>.
      </span></p>
  </div>

  Built with <a href="https://www.sphinx-doc.org/">Sphinx</a> using a
    <a href="https://github.com/readthedocs/sphinx_rtd_theme">theme</a>
    provided by <a href="https://readthedocs.org">Read the Docs</a>.
   

</footer>
        </div>
      </div>
    </section>
  </div>
  

  <div class="rst-versions" data-toggle="rst-versions" role="note" aria-label="Versions">
    <span class="rst-current-version" data-toggle="rst-current-version">
      <span class="fa fa-book"> Read the Docs</span>
      v: latest
      <span class="fa fa-caret-down"></span>
    </span>
    <div class="rst-other-versions">
      <dl>
        <dt>Versions</dt>
        
          <dd><a href="/en/latest/">latest</a></dd>
        
          <dd><a href="/en/stable/">stable</a></dd>
        
      </dl>
      <dl>
        <dt>Downloads</dt>
        
          <dd><a href="//photocad-docs.readthedocs.io/_/downloads/en/latest/pdf/">pdf</a></dd>
        
          <dd><a href="//photocad-docs.readthedocs.io/_/downloads/en/latest/epub/">epub</a></dd>
        
      </dl>
      <dl>
        
        <dt>On Read the Docs</dt>
          <dd>
            <a href="//readthedocs.org/projects/photocad-docs/?fromdocs=photocad-docs">Project Home</a>
          </dd>
          <dd>
            <a href="//readthedocs.org/builds/photocad-docs/?fromdocs=photocad-docs">Builds</a>
          </dd>
      </dl>
    </div>
  </div>
<script>
      jQuery(function () {
          SphinxRtdTheme.Navigation.enable(true);
      });
  </script> 

</body>
</html>
'''

# style_similarity(html_1, html_2)
print(style_similarity(html_1, html_2))
print(structural_similarity(html_1, html_2))
print(similarity(html_1, html_2))