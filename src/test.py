from sklearn.linear_model import SGDClassifier
X = [[0., 0.], [1., 1.]]
y = [0, 1]
clf = SGDClassifier(loss="log", penalty="l2")

classifier = clf.fit(X, y)

X1 = [[0.01, 0.02], [1.5, 1.5]]
res = classifier.predict(X1)

print res

X_p1 = [[0.01,0.02],[1.5,1.5]]
y_p1 = [1,1]

classifier.partial_fit(X_p1,y_p1)

res2 = classifier.predict(X1)
print res2
