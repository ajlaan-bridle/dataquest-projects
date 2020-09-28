# %%
import pandas as pd
import re

'''
Import data and randomly select 80% for training and the remainder
for testing
'''
sms_data = pd.read_csv(
    './files/SMSSpamCollection',
    sep='\t',
    header=None,
    names=['cat_label', 'sms_message']
    )
sms_data = sms_data.sample(frac=1, random_state=1)
split = int(sms_data.shape[0] * 0.8)
training = sms_data.iloc[:split].reset_index(drop=True)
test = sms_data.iloc[split:].reset_index(drop=True)

'''
Clean `sms_message` columns on the training data to only inlude 
lower case words without any punctuation
'''
training['sms_message'] = training['sms_message']\
    .str.lower()\
    .str.replace(r'\W', ' ')

'''
Produce vocabulary list of training data set
'''
training['sms_message'] = training['sms_message'].str.split(r'\s')
vocabulary = []
for words in training['sms_message']:
    vocabulary += words
vocabulary = list(set(vocabulary))

'''
Produce vocabulary word count for each training message
and concatenate to `training`
'''
word_counts_per_sms = {vocab_word: [0] * training['sms_message'].size \
    for vocab_word in vocabulary}
for index, sms in enumerate(training['sms_message']):
    for word in sms:
        word_counts_per_sms[word][index] += 1
training = pd.concat([training, pd.DataFrame(word_counts_per_sms)], axis=1)

'''
Create the Naive Bayes spam filter algorithm

Uses Laplace smoothing with factor alpha

P(Wi|spam) = (n_Wi|spam + alpha) / (n_spam + alpha*n_vocabulary)
P(Wi|ham) = (n_Wi|ham + alpha) / (n_ham + alpha*n_vocabulary)
'''
# calculate p_spam, p_ham, word counts, and initialise alpha
p_spam = training['cat_label'].value_counts(normalize=True)['spam']
p_ham = 1 - p_spam
n_spam = training[training['cat_label'] == 'spam']['sms_message']\
    .apply(lambda x: len(x)).sum()
n_ham = training[training['cat_label'] == 'ham']['sms_message']\
    .apply(lambda x: len(x)).sum()
n_vocabulary = len(vocabulary)
alpha = 1.0

# calculate P(Wi|spam) and P(Wi|ham) for each vocabulary word
p_word_given_spam = {vocab_word: 0 for vocab_word in vocabulary}
p_word_given_ham = {vocab_word: 0 for vocab_word in vocabulary}
training_spam = training[training['cat_label'] == 'spam']
training_ham = training[training['cat_label'] == 'ham']
for word in vocabulary:
    n_word_given_spam = training_spam[word].sum()
    n_word_given_ham = training_ham[word].sum()

    p_word_given_spam[word] = (n_word_given_spam + alpha) / \
        (n_spam + alpha * n_vocabulary)

    p_word_given_ham[word] = (n_word_given_ham + alpha) / \
        (n_ham + alpha * n_vocabulary)


def classify(message: str) -> str:
    '''
    Determines whether a string message is spam or ham
    '''

    message = re.sub('\W', ' ', message)
    message = message.lower()
    message = message.split()

    p_spam_given_message = p_spam
    p_ham_given_message = p_ham

    for word in message:
        if word in vocabulary:
            p_spam_given_message *= p_word_given_spam[word]
            p_ham_given_message *= p_word_given_ham[word]

    return 'spam' if p_spam_given_message > p_ham_given_message else 'ham'

'''
Predict spam classification on the test set
'''
test['predicted'] = test['sms_message'].apply(classify)
accuracy = (test['cat_label'] == test['predicted']).sum() / test.shape[0]