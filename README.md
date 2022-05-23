# /r/WallStreetBets Impact on Meme Stocks
Primary Language Used: Pyspark


This code tests to see if there is evidence that [wallstreetbets](https://old.reddit.com/r/wallstreetbets/) was behind the historic rise of certain stocks in the year 2021. Data was collected using reddits API, over the course of 10 months of 2021.

Using machine learning (topic modeling), specificically I believe there is sufficient evidence that discussions around the topic of GME preceeded the rise of the stock. The code uses Latent Dirichlet Allocation (LDA) to group certain topics discussed over the course of the 10 months. I aggregated the probability of each day mapped against the price of our target stocks to see if there was any correlation between them both. The blue line represents the likihood that each word discussion pertains to the target topic.


We can see a rise in discussion right before a spike in price in early 2021
![alt text](https://github.com/GrantRedfield/WallStreetBets/blob/main/GME_PLOT.png)



Similarly, we can see a gradual rise in discussion of AMC before a large spike mid 2021
![alt text](https://github.com/GrantRedfield/WallStreetBets/blob/main/AMC_PLOT.png)
