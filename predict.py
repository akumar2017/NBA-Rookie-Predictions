import numpy as np
import pandas
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score

file = "dataset_preprocessed.csv"
df = pandas.read_csv(file)

x = df.iloc[:, 3:20]
y = df.iloc[:,34:]
y1 = df[['Tier1']]
y2 = df[['Tier2']]
y3 = df[['Tier3']]
y4 = df[['Tier4']]
y5 = df[['Tier5']]
#print(x.to_numpy())
x = x.to_numpy()
y1 = np.ravel(y1.to_numpy())
y2 = np.ravel(y2.to_numpy())
y3 = np.ravel(y3.to_numpy())
y4 = np.ravel(y4.to_numpy())
y5 = np.ravel(y5.to_numpy())

x_train, x_test, y_train, y_test = train_test_split(x,y1,test_size=0.2)

#Logistic Regression
lr = LogisticRegression()
lr.fit(x_train,y_train)
y_pred = lr.predict(x_test)
#print(confusion_matrix(y_test,y_pred))
#print(classification_report(y_test,y_pred))
print("LOGISTIC REGRESSION PREDICTION")
print(y_pred)
print(accuracy_score(y_test, y_pred))

#SVM
svm = svm.SVC()
svm.fit(x_train,y_train)
y_pred = svm.predict(x_test)
print("SVM PREDICTION")
print(y_pred)
print(accuracy_score(y_test,y_pred))

#Random Forest
rf = RandomForestClassifier()
rf.fit(x_train, y_train)
y_pred = rf.predict(x_test)
print("RANDOM FOREST PREDICTION")
print(y_pred)
print(accuracy_score(y_test, y_pred))
