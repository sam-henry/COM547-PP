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

data = pd.read_csv('./train.csv')
data = data[['Sentiment', 'SentimentText']]

pos = data[data['Sentiment'] == 1]
neg = data[data['Sentiment'] == 0]

x = []
y = []
for row in pos.itertuples(index=True, name='data'):
    x.append(getattr(row, "SentimentText"))
    y.append(1)


for row in neg.itertuples(index=True, name='data'):
    x.append(getattr(row, "SentimentText"))
    y.append(0)

# x = []
# y = []
# with open("./pos_tweets.txt", encoding='utf-8') as f:
#     for i in f:
#         x.append(i)
#         y.append(1)
# with open("./neg_tweets.txt", encoding='utf-8') as f:
#     for i in f:
#         x.append(i)
#         y.append(0)
#

vectorizer = CountVectorizer(
    analyzer='word',
    lowercase=False,
    max_features=10000,
)

features = vectorizer.fit_transform(
    x
)

features_nd = features.toarray()  # for easy usage

filename = 'Classifiers/vectorizer.pkl'
_ = joblib.dump(vectorizer, filename, compress=9)

x_train, x_test, y_train, y_test = train_test_split(
    features_nd,
    y,
    train_size=0.8,
    random_state=1234,
)

ext_model = ExtraTreesClassifier(
    n_estimators=45,
    max_features=45,
    max_depth=None,
    min_samples_leaf=2
)

# rnd_model = RandomForestClassifier(
#     n_estimators=44,
#     max_features=44,
#     max_depth=None,
#     min_samples_leaf=2,
#     bootstrap=True,
#     n_jobs=-1
# )

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

log_model = LogisticRegression(
    C=500
)

# sfct_model = LogisticRegression(
#     multi_class="multinomial",
#     solver="lbfgs",
#     C=50
# )

sgd_model = SGDClassifier(
    random_state=178,
    loss="modified_huber",
    penalty="l1",
)

# sgdlgl2_model = SGDClassifier(
#     random_state=42,
#     loss="log",
#     penalty="l2"
#
# )

mnnb_model = MultinomialNB()

voting_model = VotingClassifier(
    estimators=[('lr', log_model), ('sgd', sgd_model), ('svc', svm_model), ('et', ext_model), ('mnnb', mnnb_model)],
    voting='hard'
)

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
        # y_pred = clf.predict(x_test)
        # print(clf.__class__.__name__, accuracy_score(y_test, y_pred))
        # print(cross_val_score(clf, x_train, y_train, cv=3, scoring="accuracy"))
        # y_train_pred = cross_val_predict(clf, x_train, y_train, cv=3)
        # print(precision_score(y_train, y_train_pred))
        # print(recall_score(y_train, y_train_pred))

    _ = joblib.dump(clf, filename, compress=9)


