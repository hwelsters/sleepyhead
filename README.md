![image](https://user-images.githubusercontent.com/84760072/221109482-cc57c5a9-2d6b-42cc-b8e1-fd91ec2c733b.png)

<p align="center">
  For doing data collection, analysis and research related to ChatGPT while sleeping 💤.
</p>


## Steps
- Generates math questions (generated math equations do not enforce semantic limitations.)
- Asks ChatGPT math equations
- Calculate causality values
- Model fitting -> tries out base models and then tries numerous combinations of ensembling, boosting and stacking outputs everything into json.
- Sleep for 8 hrs (important for brain function)
- Wake up
- Profit 💰

## Get involved
- 🐛 **Found a bug?** - Create an [issue][issue]  
- ⚙️ **Interested in adding a feature?** - Check out the [project roadmap](ROADMAP.md) or suggest your own changes by creating an [issue][issue]   
- 📖 **Can we improve the documentation?** - Even pull requests for small changes can be helpful. Feel free to change the [documentation][docs]!  
- 😵 **See something wrong with the dataset?** - While our dataset may be accurate most of the time, there are cases where the solutions might not make sense in relation to the question.  
  
For example, take this question:
```
The sum of two consecutive odd integers is at least 36 . What are the integers ?
```
Our algorithms do not pick up constraints between two numbers. Constraints like these have to be tuned by hand. (Interestingly, our algorithm actually filters this question out but there definitely will be cases where our code is susceptible.)
  
[bugs]: https://github.com/hwelsters/axolotl-src/issues
[issue]: https://github.com/hwelsters/axolotl-src/issues
[docs]: documentation
[line]: https://user-images.githubusercontent.com/84760072/220297409-f97511e8-95e5-4204-9217-67d9f9353b76.png
[cecdown]: https://github.com/hwelsters/cecdown

## References
- N. Kushman, Y. Artzi, L. Zettlemoyer, R. Barzilay, Learning to Automatically Solve Algebra Word Problems ([link](https://aclanthology.org/P14-1026.pdf))
- N. Kushman, Y. Artzi, L. Zettlemoyer, R. Barzilay, ALG-514 dataset ([link](https://groups.csail.mit.edu/rbg/code/wordprobs/))
- S. Upadhyay, M.-W. Chang, DRAW: A Challenging and Diverse Algebra Word Problem Set, ([link](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tech_rep.pdf))
- S. Upadhyay, M.-W. Chang, DRAW-1K dataset, ([link](https://paperswithcode.com/dataset/draw-1k#:~:text=DRAW%2D1K%20is%20a%20dataset,derivation%20of%20an%20equation%20system.))
- S. Kleinberg, B. Mishra, The Temporal Logic of Causal Structures ([link](http://www.skleinberg.org/papers/uai09.pdf))
- D. Saxton, E. Grefenstette, F. Hill, P. Kohli, Analysing Mathematical Reasoning Abilities of Neural Models ([link](https://openreview.net/pdf?id=H1gR5iR5FX))
