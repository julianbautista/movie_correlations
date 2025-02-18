# movie_correlations
Scripts to generate movies of evolution of power-spectrum and correlation function of different species in the Universe.

Requires: 
- camb
- hankl 
- ffmpeg

First, we need to run camb to obtain transfer functions and derived parameters. This writes a ~100Mb pickle format file containing the outputs. 

`python write_camb_transfer_functions.py `



Then, we make the movies running:

`python make_movies.py`


Here is the power spectrum movie:



https://github.com/user-attachments/assets/678b9708-99e2-48af-87c6-164c145649d3





Here is the correlation function movie:



https://github.com/user-attachments/assets/034c8674-8687-4efd-ba26-05ed3a4bb246





