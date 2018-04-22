# import statements
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import VotingClassifier, ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import LinearSVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
# from sklearn.model_selection import cross_val_score, cross_val_predict
# from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib

import pandas as pd
# read in the training data
data = pd.read_csv('./train.csv')
data = data[['Sentiment', 'SentimentText']]
# split into positve and negative
pos = data[data['Sentiment'] == 1]
neg = data[data['Sentiment'] == 0]
# create two lists of data x for text y for sentiment
x = []
y = []
for row in pos.itertuples(index=True, name='data'):
    x.append(getattr(row, "SentimentText"))
    y.append(1)


for row in neg.itertuples(index=True, name='data'):
    x.append(getattr(row, "SentimentText"))
    y.append(0)
# create vectoriszer object
vectorizer = CountVectorizer(
    analyzer='word',
    lowercase=False,
    max_features=10000,
)
# fit the vectorizer on the training data
features = vectorizer.fit_transform(
    x
)
# convert features to array
features_nd = features.toarray()  # for easy usage
# save the vectorizer object to disk
filename = 'Classifiers/vectorizer.pkl'
_ = joblib.dump(vectorizer, filename, compress=9)
# split the data into training and test sets
x_train, x_test, y_train, y_test = train_test_split(
    features_nd,
    y,
    train_size=0.8,
    random_state=1234,
)
# create the classification models
ext_model = ExtraTreesClassifier(
    n_estimators=45,
    max_features=45,
    max_depth=None,
    min_samples_leaf=2
)

log_model = LogisticRegression(
    C=500
)

sgd_model = SGDClassifier(
    random_state=178,
    loss="modified_huber",
    penalty="l1",
)

mnnb_model = MultinomialNB()

svm_model = Pipeline((
    ("scaler", StandardScaler(with_mean=False)),
    ("linear_svc", LinearSVC(
        C=0.002,
        loss="squared_hinge",
        max_iter=1000,
        penalty='l2',
        random_state=678,
        dual=True
    )),
    ))

voting_model = VotingClassifier(
    estimators=[('lr', log_model), ('sgd', sgd_model), ('svc', svm_model), ('et', ext_model), ('mnnb', mnnb_model)],
    voting='hard'
)
# train the classification models and save them to disk
for clf in (log_model, sgd_model, svm_model, ext_model, mnnb_model, voting_model):
    clf.fit(x_train, y_train)
    if clf is log_model:
        filename = 'Classifiers/log_model.pkl'
    elif clf is sgd_model:
        filename = 'Classifiers/sgd_model.pkl'
    elif clf is svm_model:
        filename = 'Classifiers/svm_model.pkl'
    elif clf is ext_model:
        filename = 'Classifiers/ext_model.pkl'
    elif clf is mnnb_model:
        filename = 'Classifiers/mnnb_model.pkl'
    else:
        filename = 'Classifiers/voting_model.pkl'

        # this code was used to output the accuracy and recall values of the trained models.
        # it has been left here commented out for when the models need to be retrained
        # y_pred = clf.predict(x_test)
        # print(clf.__class__.__name__, accuracy_score(y_test, y_pred))
        # print(cross_val_score(clf, x_train, y_train, cv=3, scoring="accuracy"))
        # y_train_pred = cross_val_predict(clf, x_train, y_train, cv=3)
        # print(precision_score(y_train, y_train_pred))
        # print(recall_score(y_train, y_train_pred))

    _ = joblib.dump(clf, filename, compress=9)
