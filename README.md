This is my first project in applying deep learning into eCommerce.

Idea: My team and I are maintaining a facebook page called "LHP Confessions". Since this page was created in 2013, it has been lots of
posts already and it's hard to find the old posts on facebook. So, I want to take this opportunity to create a recommender system that 
can give our users their "favorite" kind of posts.

- In this project, there are two important aspects. First, that is the recommendation system. For this part, I tried matrix factorization, dot neural network, and users-items embedding neural network with softmax. The second part, I analyzed the posts with BERT and fully connected network with BERT feature.

You can check model/admin_post_helpers.ipynb and model/collaborating_filter.ipynb for more detail

- For further work, I will add question-answer algorithm because we are currently received many similar questions from students about certain topic. Therefore, I think this would make sense if I made a model that can briefly answer students' questions. In addition, I will try sequential recommendation and temporal ranking for students in order to improve the students' experience when they read the posts.