import os
import json
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

TUNE_FILE_PATH = "../tuned/"
if not os.path.isdir(TUNE_FILE_PATH): os.makedirs(TUNE_FILE_PATH)

class SklearnHelper(object):
    def __init__(self, clf_base, seed=0, params=None):
        self.clf_base = clf_base
        self.params = params
        self.seed = seed

    def train(self, x_train, y_train):
        self.clf.fit(x_train, y_train)

    def predict(self, x):
        return self.clf.predict(x)

    def fit(self, x, y):
        return self.clf.fit(x, y)

    def feature_importances(self, x, y):
        return self.clf.fit(x, y).feature_importances_

    def tune(self, params_to_test: any, name: str):
        OUTPUT_FILE_PATH = f"{TUNE_FILE_PATH}{name}.json"

        params = None
        if os.path.isfile(OUTPUT_FILE_PATH):
            f = open(OUTPUT_FILE_PATH)
            params = json.load(f)
        else:
            gcv = GridSearchCV(estimator=self.clf_base, param_grid=params_to_test)
            gcv.fit(pd.DataFrame({'A': [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]}), pd.Series([0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0]))
            params = gcv.best_params_
            with open(OUTPUT_FILE_PATH, "w") as outfile:
                json.dump(params, outfile)
        
        print(params)


rf_params = {'n_estimators': [5, 10, 50, 100, 200], 'criterion': ['gini', 'entropy'], 'max_features': ['auto', 'sqrt', 'log2'], 'max_depth' : [4,5,6,7,8],}
model = SklearnHelper(clf_base=RandomForestClassifier())
model.tune(rf_params, 'rf')
