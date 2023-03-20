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

![](https://github.com/julianbautista/movie_correlations/blob/main/movies/pk_movie_ylog_mnu0.10.mp4)


Here is the correlation function movie:

https://github.com/julianbautista/movie_correlations/blob/main/movies/xi_movie_mnu0.10.mp4


