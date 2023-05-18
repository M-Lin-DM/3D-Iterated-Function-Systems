# 3D-Stochastic-Iterated-Function-Systems
For generating and plotting object clusters in Cinema4D using an approach inspired by iterated function systems. 
See the [YouTube video](https://www.youtube.com/watch?v=EMZqDglulss) for visual results of this method. 

Here I created life-like fractal shapes using python and Cinema 4D. 
The program builds a tree where each parent node births several smaller children, and so on. All children are plotted as ellipsoids.
I introduce randomness to the process to allow a child's properties, namely color, shape, position, and rotation angle, to be a mutated version of the parent's. 
Adding stochasticity to the functions that create mutations allows us to get some very organic forms, which contrast with more mathematically perfect fractals (such as those from iterated function systems, which inspired my approach).

# Scripts
- `plot_objects.py` is the top-level script that is intended to be run inside Cinema4D's scripts section. Here you can change the parameters used to generate the objects.
- - You will need to place all .py files in the directory that C4D searches, and not within its own folder in that directory. For me it's the libs folder: C:\Users\MrLin\AppData\Roaming\Maxon\python\python39\libs. 
- - `generate_tree.py` contains the main logic that creates a list of objects to be plotted and the networkx graph that contains linkages between nodes.
- - the key function that is called in `plot_objects.py` is `generate_objects()`
- 
