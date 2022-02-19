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

Here is a snapshot of the power spectrum movie:

![Screenshot 2022-02-19 at 15 41 48](https://user-images.githubusercontent.com/22989643/154805670-c012053f-c910-47ff-a626-a4613143e2ed.png)

Here is a snapshot of the correlation function movie:

![Screenshot 2022-02-19 at 15 42 25](https://user-images.githubusercontent.com/22989643/154805674-74692ea8-d014-42ca-baa4-25b63fc45091.png)



https://user-images.githubusercontent.com/22989643/154807965-cadb654e-1feb-4abe-878f-54d30783dc52.mp4

