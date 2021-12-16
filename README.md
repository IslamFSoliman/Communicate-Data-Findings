# Communicate-Data-Findings
# FordGo Bike Sharing System

## Data visualization is an important skill that is used in many parts of the data analysis process.

>Exploratory data visualization usually occurs during and after the data wrangling process, and is the main method that we use to understand the patterns and relationships presented in our data. This understanding will help us approach any statistical analysis and will help us build conclusions and findings.
<br>This process might also illuminate additional data cleaning tasks to be performed.

>Explanatory data visualization techniques are used after generating our findings, and are used to help communicate our results to others. Understanding design considerations will make sure that our message is clear and effective. In addition to being a good producer of visualizations, going through this project would also help us to be a good consumer of visualizations that are presented to us by others.
****

## Project Details
<ol>
  <li>Dataset: <a href="https://s3.amazonaws.com/baywheels-data/index.html" target="_blank">Ford GoBike</a> for the months of February, and March 2020. Consisted of 609,153 observations (rows) and 18 features (columns).
  <li>Exploring the data: Please explore the jupyter notebook file where the dataset is programatically, and visually explored.
  <li>Document the story: Please check Readme.md file where the findings are documented to convey a story to present to an audience.
  <li>Communicate the findings: Please check the finalized slide deck with my findings is prepared for a curious audience.
</ol>

## Project Findings
This project is a *win - win situation* where the company and a large number of people can benefit from this program:
<ul>
  <li>**Subscribers** `61.3%` (i.e. daily commuters) benefit from a healthy commuting choice.
  <li>**Customers** `38.7%` (i.e. tourists, students, etc.) have a sustainable, yet flexible option for touring the city.
  <li>The use of the service peaks mainly at `08:00AM` and `05:00PM`. This is due to work and school times in the United States.
  <li>**Weekdays** shows *`more demand`* for the service, while **weekends** witness the *`lowest utilisation`* of service.
  <li>The majority of **trip duration** falls between *`20 minutes or less`*.
  <li>The busiest day of week is **Monday**.
  <li>The **average** subscriber **trip duration** is about *`10 minutes`* and it seems to be fixed within that range without major fluctuations.
  <li>The **variation** for *`customers`* tends to be more that that of *`subscribers`*.
</ul>

## Key Points for The Presentation
<ul>
  <li>Ford GoBike Usage Per Hour
  <li>Average Trip Time in Minutes
  <li>Ford GoBike System - Customers Vs Subscribers
  <li>Ford GoBike System Trends by User Type
  <li>Ford GoBike System - Customers vs. Subscribers Ride Duration in Minutes 
</ul>

## Project Files
<ol>
  <li>readme.md - This Markdown file contains sections I've filled out after selecting the dataset, completed the exploration, and planed my explanatory analysis.
  <li>exploration.ipynb - This Jupyter Notebook contains my dataset exploration, starting from loading in the data, working through univariate visualizations, and ending with bivariate and multivariate exploration.
  <li>slides.ipynb - This Jupyter Notebook contains my slide deck deliverable.

To view the slide deck, you will need to use the expression (all one line):
<br>! jupyter nbconvert slides.ipynb --to slides --post serve  --no-input --no-prompt<br>
  
  <li>slides.slides.html - This file can be used to view the slide deck directly in the internet browser without viewing the original.
</ol>
