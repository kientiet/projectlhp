This is my first project in recommender system fields.

Idea: My team and I are maintaining a facebook page called "LHP Confessions". Since this page was created in 2013, it has been lots of
posts already and it's hard to find the old posts on facebook. So, I want to take this opportunity to create a recommender system that 
can give our users their "favorite" kind of posts.

Strategy: I plan to build the content-based model first. Because it takes lots of time and effort to analyze and understand about posts,
specially, topic of posts that we have. Second reason is I want to build automatic system that can eliminate posts that are not suitable 
with our rules.
  After I done with content-based model, I will start to build CF on the implicit feedback.

This project is still in developing times. But I've done some technique:
- Find to token paragraph - using CRF
- I put all the token to mongodb. 

Next step:
- I will put word2vec and paragraph2vec to my project. I plan to use these technologies because the result of those are in vector form,
which is suitable for other part of learning.
