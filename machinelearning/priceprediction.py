import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt
import seaborn as sns


#df = pd.read_csv(r'C:\Users\portable\oldtimertrends\280sl_full_auction_cleaned.csv')
df = pd.read_csv(r'dataframe2.csv')
df['quote_model'] = "280 SL cabriolet hard-top"

df["auction_price"].div(10).round(2)
df.drop('quote_id', axis =1, inplace=True)
df.drop('auction_url', axis =1, inplace=True)


# creating instance of labelencoder
labelencoder = LabelEncoder()

df['auction_location'] = labelencoder.fit_transform(df['auction_location'])
df['auction_model'] = labelencoder.fit_transform(df['auction_model'])
df['auction_organizor'] = labelencoder.fit_transform(df['auction_organizor'])
df['auction_restauration_code'] = labelencoder.fit_transform(df['auction_restauration_code'])
df['auction_sales_code'] = labelencoder.fit_transform(df['auction_sales_code'])
df['auction_brand'] = labelencoder.fit_transform(df['auction_brand'])
df['quote_model'] = labelencoder.fit_transform(df['quote_model'])
df['quote_max_price'] = labelencoder.fit_transform(df['quote_max_price'])


plt.figure(figsize=(12,10))
cor = df.corr()
sns.heatmap(cor, annot=True, cmap=plt.cm.Reds)
plt.show()

#df.to_csv("280sl_encoded.csv", encoding='utf-8', index=False)

X = df.loc[:, df.columns != 'auction_price']
print(X.columns)
y = df['quote_max_price']
print(y.head())

#Using Pearson Correlation



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
regressor = LinearRegression()
regressor.fit(X_train, y_train)
print(regressor.coef_)
print(regressor.intercept_)
y_pred = regressor.predict(X_test)
df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
df

from sklearn import metrics
print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))