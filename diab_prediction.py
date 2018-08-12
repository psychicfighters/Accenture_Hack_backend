import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
import numpy as np
from sklearn.model_selection import train_test_split


def get(list):
    diabetes = pd.read_csv('diabetes.csv')
    # print(diabetes.columns)
    # print(diabetes.head())
    # print("dimension of diabetes data: {}".format(diabetes.shape))
    diabetes = diabetes.drop(['SkinThickness', 'Insulin', 'DiabetesPedigreeFunction'], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(diabetes.loc[:, diabetes.columns != 'Outcome'],
                                                        diabetes['Outcome'], stratify=diabetes['Outcome'], random_state=66)


    gb = GradientBoostingClassifier(min_samples_split=4, random_state=0)
    gb.fit(X_train, y_train)
    # print("Accuracy on training set: {:.3f}".format(gb.score(X_train, y_train)))
    # print("Accuracy on test set: {:.3f}".format(gb.score(X_test, y_test)))
    # #pr = []
    #pr =[6,148,72,35,0,33.6,0.627,50]
    B = np.reshape(list, (-1, 5))
    #print(B)
    return gb.predict(B)

print(get([0,148,72,33.6,50]))  #Pregnancies,Glucose,BloodPressure,SkinThickness,Insulin,BMI,DiabetesPedigreeFunction,Age,Outcome