import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
import numpy as np
from sklearn.model_selection import train_test_split


def get(list):
    diabetes = pd.read_csv('diabetes.csv')

    diabetes = diabetes.drop(['SkinThickness', 'Insulin', 'DiabetesPedigreeFunction'], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(diabetes.loc[:, diabetes.columns != 'Outcome'],
                                                        diabetes['Outcome'], stratify=diabetes['Outcome'], random_state=66)


    gb = GradientBoostingClassifier(min_samples_split=4, random_state=0)
    gb.fit(X_train, y_train)
    B = np.reshape(list, (-1, 5))
    #print(B)
    return gb.predict(B)
