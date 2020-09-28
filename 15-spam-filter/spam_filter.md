# Spam or Ham: SMS Edition
## SMS Spam Filtering with Naive Bayes

<a data-flickr-embed="true" href="https://www.flickr.com/photos/robinhutton/24324551027/in/photolist-D4tFyP-4YquSL-4C6NQo-Skcx6h-4mZsmC-hNh67-kCAL2L-kCANQm-9ivgoD-6Ys3vh-5Nfafk-b4ThXT-j76egA-j71TQi-4zGP8b-8jBWuu-9NZujn-6qY9vr-5Hf4WS-mSRtT-718hHC-71HDFc-2NYWTK-6eLuK-vVZqB-dgu3-79Z3X-mb7gL-39uw1-2NiBSN-6cSS7G-8b9Hjq-5f1fho-5pDMMS-9vw9hx-hfXfA-5xmaj-4sqgZw-8WuDpp-o9bd3k-pRrxLR-258kqqN-tuDnQ-5FQ3yz-5hrex8-8YeJPL-4nFSR8-pFKpm-563Gj-uvg4n" title="Spam!"><img src="https://live.staticflickr.com/4597/24324551027_88018de941.jpg" width="500" height="375" alt="Spam!"></a><script async src="//embedr.flickr.com/assets/client-code.js" charset="utf-8"></script>
_Robin Hutton on Flickr_

## Introduction

The purpose of this project is to produce an SMS spam filtering algorithm using a Naive Bayes approach.

A [data set](https://archive.ics.uci.edu/ml/datasets/sms+spam+collection) of existing spam and non-spam SMS messages, available at the University of California Irvine machine learning repository, is used to produce the algorithm. A [description](http://www.dt.fee.unicamp.br/~tiago/smsspamcollection/#composition) of the data set shows that the 747 spam messages are extracted from sources including: the UK forum Grumbletext, and Universidad Europa Madrid. The data set also contains 4,825 non-spam, or 'ham', messages extracted from sources including: Caroline Tag's PhD thesis at the University of Birmingham, and a random selection from a repository of around 10,000 at the National University of Singapore Corpus.

### Objectives

The primary objectives are to:

- Produce a Naive Bayes algorithm that assesses the written content of an SMS to determine whether it is a spam message or not (ham).
- Achieve an accuracy of greater than 80% against a set of test cases that have been pre-categorised.

### High Level Workflow

_\<A flowchart would be good instead of the bullet list below - how to do this?\>_

- Split data into training and test subsets.
- Transform SMS content in the training data into lists of lower case alphanumeric words without any punctuation or special characters.
- Develop a vocabulary (all unique words) from the training data.
- Calculate Naive Bayes algorithm parameters for each word in the vocabulary.
- Write a function that uses the Naive Bayes parameters to classify an SMS string as 'spam' or 'ham'.
- Test the function using the test subset and determine the accuracy of the spam filter.

## A Brief Overview of Naive Bayes

For the uninitiated, this section provides a brief explanation of the mathematical equation implemented for this spam filter. A Naive Bayes method is a supervised learning algorithm that is based on Bayes' Theorem of conditional probability, where the probability of class variable y given a feature set of x's is provide by:

<img src="https://latex.codecogs.com/png.latex?\dpi{120}&space;\bg_white&space;\large&space;P(y&space;\mid&space;x_1,&space;\dots,&space;x_n)&space;=&space;\frac{P(y)&space;P(x_1,&space;\dots,&space;x_n&space;\mid&space;y)}&space;{P(x_1,&space;\dots,&space;x_n)}" title="\large P(y \mid x_1, \dots, x_n) = \frac{P(y) P(x_1, \dots, x_n \mid y)} {P(x_1, \dots, x_n)}" />

In the application of an SMS spam filter, the class variable is the classification of a message as spam or ham, and the feature set is the text content of a message. To be able to define calculations with a practical level of complexity, a simplifying assumption of conditional independence is made such that:

<img src="https://latex.codecogs.com/png.latex?\dpi{120}&space;\bg_white&space;\large&space;\large&space;P(x_i&space;|&space;y,&space;x_1,&space;\dots,&space;x_{i-1},&space;x_{i&plus;1},&space;\dots,&space;x_n)&space;=&space;P(x_i&space;|&space;y)" title="\large \large P(x_i | y, x_1, \dots, x_{i-1}, x_{i+1}, \dots, x_n) = P(x_i | y)" />

This assumption is the 'Naive' in Naive Bayes, since it ignores any potential dependency between the features. In a spam filter vernacular this would be the ignorance of some words being more likely to appear in a message if other words are present. For example, 'minutes' might be more likely to appear in an SMS message if 'unlimited' is present.

The above assumption simplifies the general Bayes' Theorem equation to:

<img src="https://latex.codecogs.com/png.latex?\dpi{120}&space;\bg_white&space;\large&space;P(y&space;\mid&space;x_1,&space;\dots,&space;x_n)&space;=&space;\frac{P(y)&space;\prod_{i=1}^{n}&space;P(x_i&space;\mid&space;y)}&space;{P(x_1,&space;\dots,&space;x_n)}" title="\large P(y \mid x_1, \dots, x_n) = \frac{P(y) \prod_{i=1}^{n} P(x_i \mid y)} {P(x_1, \dots, x_n)}" />

Going further still, the approach for this algorithm will be to compare the estimated probability of a message being spam given its written content with the estimated probability of the same message being not spam given its written content. To this end, calculating <img src="https://latex.codecogs.com/png.latex?\inline&space;\dpi{120}&space;\bg_white&space;\large&space;P(x_1,&space;\dots,&space;x_n)" title="\large P(x_1, \dots, x_n)" /> becomes redundant, so is no longer needed. Calculating absolute probabilities is not required, only a way to determine whether a spam or ham classification is more likely. Thus the Naive Bayes mathematical equations implemented for this spam filter are:

<img src="https://latex.codecogs.com/png.latex?\dpi{120}&space;\bg_white&space;\large&space;\large&space;P(spam&space;\mid&space;x_1,&space;\dots,&space;x_n)&space;=&space;P(spam)&space;\prod_{i=1}^{n}&space;P(x_i&space;\mid&space;spam)" title="\large \large P(spam \mid x_1, \dots, x_n) = P(spam) \prod_{i=1}^{n} P(x_i \mid spam)" />

<img src="https://latex.codecogs.com/png.latex?\dpi{120}&space;\bg_white&space;\large&space;\large&space;P(ham&space;\mid&space;x_1,&space;\dots,&space;x_n)&space;=&space;P(ham)&space;\prod_{i=1}^{n}&space;P(x_i&space;\mid&space;ham)" title="\large \large P(ham \mid x_1, \dots, x_n) = P(ham) \prod_{i=1}^{n} P(x_i \mid ham)" />

Where <img src="https://latex.codecogs.com/png.latex?\inline&space;\dpi{120}&space;\bg_white&space;\large&space;P(spam)" title="\large P(spam)" /> and <img src="https://latex.codecogs.com/png.latex?\inline&space;\dpi{120}&space;\bg_white&space;\large&space;P(ham)" title="\large P(ham)" /> are the relative frequency of spam messages and ham messages respectively in the training set. Each term in one of the products can be broken down as follows:

<img src="https://latex.codecogs.com/png.latex?\dpi{120}&space;\bg_white&space;\large&space;\large&space;P(x_i&space;\mid&space;spam)&space;=&space;\frac{&space;N_{spam,i}&space;}{&space;N_{spam}&space;}" title="\large \large P(x_i \mid spam) = \frac{ N_{spam,i} }{ N_{spam} }" />

Where <img src="https://latex.codecogs.com/png.latex?\inline&space;\dpi{120}&space;\bg_white&space;\large&space;N_{spam,i}" title="\large N_{spam,i}" /> is the number of occurrences of of the word <img src="https://latex.codecogs.com/png.latex?\inline&space;\dpi{120}&space;\bg_white&space;\large&space;x_i" title="\large x_i" /> in the spam messages of the training set, and <img src="https://latex.codecogs.com/png.latex?\inline&space;\dpi{120}&space;\bg_white&space;\large&space;N_{spam}" title="\large N_{spam}" /> is the total number of words across all spam messages in the training set.

### Laplace Smoothing

Since the Naive Bayes algorithm uses relative occurrences of words in spam or ham messages in the training set, it is possible that there are words in the derived vocabulary that exist in spam messages and not in ham messages, or vice versa. Treating these strictly as above would result in a zero term that would de-rail the algorithm. Rather than ignore these words, a modified version of the above equation is implemented to include Laplace smoothing terms, such that a word with zero occurances in one classification (e.g. spam) still produces a non-zero term within the product.

<img src="https://latex.codecogs.com/png.latex?\dpi{120}&space;\bg_white&space;\large&space;\large&space;\large&space;P(x_i&space;\mid&space;spam)&space;=&space;\frac{&space;N_{spam,i}&space;&plus;&space;\alpha}{N_{spam}&space;&plus;&space;\alpha&space;n}" title="\large \large \large P(x_i \mid spam) = \frac{ N_{spam,i} + \alpha}{N_{spam} + \alpha n}" />

Where <img src="https://latex.codecogs.com/png.latex?\inline&space;\dpi{120}&space;\bg_white&space;\large&space;\alpha" title="\large \alpha" /> is the smoothing factor (set to 1.0), and <img src="https://latex.codecogs.com/png.latex?\inline&space;\dpi{120}&space;\bg_white&space;\large&space;n" title="\large n" /> is the total number of unique words in the vocabulary derived from the training set.

## Splitting into Training and Test Data Sets

A total of 5,572 pre-existing SMS messages, of which 87% are ham and the remaining 13% are spam, are available in the data set to train and test the algorithm.

To test the accuracy of the spam filter, a subset of this data set will be siphoned off for use as a test set. These messages will already have been classified as spam or ham, so for each test case the model will either correctly or incorrectly label the message as spam/ham. This test set will not be used to train the algorithm so that these messages are independent test cases.

To this end, 80% (4457 messages) of the data set has been randomly selected to train the Naive Bayes algorithm, and the remaining 20% will be used to test it. Both sets contain 13% spam messages, matching the proportion of the total data set.

## Preparing the Training Data

To assess the written content of an SMS message, some homogenisation is required to break it down into standardised components for the algorithm's parameters. Each message in the training data has gone through a preparation stage to remove any characters that are not basic alphanumeric characters. All the text has then been converted to lower case and then split into a list of words.

For example:

`'Unlimited texts. Limited minutes.'` &#8594; `['unlimited', 'texts', 'limited', 'minutes']`

This step is also implemented into the function to convert a new message into a list of lower case alphanumeric words as part of the classification process.

