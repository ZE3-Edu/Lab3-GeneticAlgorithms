# Evolution *in silico* Lab 3 - Genetic Algorithms

## Overview
In class, we talked about a situation some of you correctly identified as the **Knapsack** problem, where we're trying to fill a bag with the most total *value*. Here let's start playing with a different classic problem in computer science (that has many many practical uses), the **Traveling Salesman Problem** (TSP). 

But, let's make it more fun. Let's imagine we are in a post-pandemic world, and you're getting ready to take the roadtrip of a lifetime. You've made a list of some of the most amazing National Parks, tourist attractions, and friends to stop at. But, you're a college student, and an eco-conscious one at that, so don't want to spend more money or waste more gas than you need. How else would you solve this problem, other than use a Genetic Algorithm?! 

You know the location of every stop you want to make, and you can easily calculate the distance between any of the locations, so you need to figure out how to leave and get back to the same spot (Ann Arbor, for example) while traveling the shortest distance (ignoring differential fuel efficiency and toll roads for now). Let's call this the Post-Pandemic Roadtrip Problem (**PPRP**). 

Here's a fun video of the TSP being explained on a [whiteboard](https://www.youtube.com/watch?v=CPetTODX-FA)

Now, I'll pick one way of representing possible solutions in the boilerplate code, but it's not a good one and you should definitely improve on it! You'll have to implement a few things to get a working genetic algorithm, but most of your time will probably go towards improving it beyond just *working*. Look back to our lectures and forward to the next reading for some ideas. Feel free to talk with each other and your HW groups for inspiration!

## What You Should Do
First, get comfortable with the code I've provided! After that, focus on improvements. 

Think about some of the ideas covered in the Lecture 7 and 8, and which ones might be useful for the PPRP. 

Use graphs of the population dynamics (e.g., fitness over time) to help diagnose potential issues. For example, if your population seems to quickly settle and *converge* on a single solution, maybe you need to introduce some features that help preserver diversity. 

Think about the representation of this solution, and what kinds of genetic operators (mutations, crossover) might be useful. Try a different representation of solutions if you're up for it. The next reading assignment has a really clever encoding that might be useful. 

See how you do finding a roadtrip for a *big* list of locations.