# grs1915-auto-encoder
My thesis work on mapping the X-ray Varaibility patterns of the X-ray Black hole binary system GRS 1915+105. This repository only contains the projection plotter (app.py) and the UMAP co-ordinates (and associated information) in a pickle file. For the original data used in this project, please go to my website benricketts.com or send me an email/message.
A few notes:
Your Pandas version needs to be 1.4.1 to be guaranteed to successfully unpickle.
You will need to have the dash package installed.
The images of original data and the reconstructed data will only be visible if you are online - they query my website for the images.
app.py and the pickle file need to be in the same folder when you run app.py
To view the projection, go to http://127.0.0.1:8050/ in your browser. The program shouldn't take long to load - it is only really loading a pandas dataframe and plotting it.
