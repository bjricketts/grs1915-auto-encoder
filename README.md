# grs1915-auto-encoder
Mapping the X-ray Varaibility patterns of the X-ray Black hole binary system GRS 1915+105. 

This repository only contains the projection plotter (app.py) and the UMAP co-ordinates (and associated information) in pickle files. For the original data used in this project, please go to zenodo: 10.5281/zenodo.7547328.

A few notes:
Your Pandas version needs to be 1.4.1 to be guaranteed to successfully unpickle.
You will need to have the dash package installed.
The images of original data and the reconstructed data will only be visible if you are online - they query my website for the images.
app.py and the pickle files need to be in the same folder when you run app.py
To view the projection, go to http://127.0.0.1:8050/ in your browser. The program shouldn't take long to load - it is only really loading a pandas dataframe and plotting it.

There are 3 different projections: a projection generated from data using 256 second long segments, another projection similarly generated with 1024 second long segments and finally another on the 2048 time scale.
There are also a number of other projections that only take into consideration some of the latent space produced by the UMAP for the 256 second timescale.
You can select 5 different ways of viewing each projection:
Only plotting points that have been definitively labelled with a high conifdence.
Plot all points including observations that are more tenously labeled or not labeled at all.
Plot all data points, colored by the intensity loss score of the reconstruction.
Plot all data points, colored by the HR1 loss score of the reconstruction.
Plot all data points, colored by the HR2 loss score of the reconstruction.
