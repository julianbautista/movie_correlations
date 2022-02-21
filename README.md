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


https://user-images.githubusercontent.com/22989643/155038475-a98811b2-cb32-44b3-993d-b93ade777ed2.mp4


Here is the correlation function movie:

https://user-images.githubusercontent.com/22989643/155038502-40a8d110-eed7-4b69-bb2d-e02f87bc33e1.mp4



