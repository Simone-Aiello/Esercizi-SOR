import joblib
from sklearn.linear_model import LinearRegression

model = LinearRegression()
joblib.dump(value=model,filename="linear_model",compress=9)