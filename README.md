This is my first project in recommender system fields.

Idea: My team and I are maintaining a facebook page called "LHP Confessions". Since this page was created in 2013, it has been lots of
posts already and it's hard to find the old posts on facebook. So, I want to take this opportunity to create a recommender system that 
can give our users their "favorite" kind of posts.

- In this project, I implement two kind of model for recommendation system: 
+ Matrix Factorize with ALS
+ Probabilistic Matrix Factorize with Momentum Gradient Descent (include users and items bias). Beside that, I also tried online-update with Stochastic Gradient Descent. In this second approach, I will change the model to more advance way: Change the users and items bias to time dependence. And choose the sample for online-update more carefully instead randomly.

- Beside recommendation system, I also analyzed posts on facebook by doc2vec with some pre-processing steps.

- Further work, I will implement long-short term memory to this data to test the accuracy. 
