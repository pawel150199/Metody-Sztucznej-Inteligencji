from sklearn.datasets import make_classification
import numpy as np
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.feature_selection import SequentialFeatureSelector
#dane 
X, y = make_classification(
    n_samples = 1000,
    n_classes = 10,
    n_informative = 10
)

#klasyfikatory
clfs = {
    'GNB': GaussianNB(),
    'kNN': KNeighborsClassifier(),
    'SVC': SVC(),
}

#tablica z wartościami z rozkładu normalnego
rand = np.random.normal(size=X.shape[1])

#mnozenie elementów 
X = X*rand

n_splits = 2
n_repeats = 5

rskf = RepeatedStratifiedKFold(
    n_splits=n_splits,
    n_repeats=n_repeats,
    random_state=42,
)

print(f"X shape: {X.shape}\n")#kształt oryginalny

#selekcja danych
scoress = np.zeros((len(clfs), n_splits*n_repeats))
for fold_id, (train, test) in enumerate(rskf.split(X, y)):
    scaler = SequentialFeatureSelector(estimator=GaussianNB())
    scaler.fit(X[train], y[train])
    X_test = scaler.transform(X[test])
    X_train = scaler.transform(X[train])

    for clf_id, clf_name in enumerate(clfs):
        clf = clfs[clf_name]
        clf.fit(X_train, y[train])
        y_pred = clf.predict(X_test)
        scoress[clf_id, fold_id] = accuracy_score(y[test], y_pred)

mean = np.mean(scoress, axis=1)
std = np.std(scoress, axis=1)

for clf_id, clf_name in enumerate(clfs):
    print("%s: %.3f (%.3f)" % (clf_name, mean[clf_id], std[clf_id]))
print(f"\nLiczba atrybutów: {X_train.shape}\n")#kształt przed zmniejszeniem danych