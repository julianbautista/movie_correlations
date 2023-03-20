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

https://user-images.githubusercontent.com/22989643/226380063-4d8e6fbe-a69f-41cd-b727-64c17636f5de.mp4



Here is the correlation function movie:

https://user-images.githubusercontent.com/22989643/226380138-14fdccf6-9d1f-4738-8e47-9053aa9efebc.mp4




