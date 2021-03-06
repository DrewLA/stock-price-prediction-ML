# Author: Andrew Lewis
# Description: Stock Price Prediction using an RNN (LSTM) model trained on 50 day rolling data
#              Uses adam optimizer
#              Example based on INTEL stock price from 2019 till date
#              Datasource: Yahoo finance

# Import libraries
import math
import pandas_datareader as web
import numpy as np
import matplotlib.pyplot as plt
import tensorflow.keras as k
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Dense, LSTM
plt.style.use('fivethirtyeight')

# Get stock quote
df = web.DataReader('INTC', data_source='yahoo', start='2013-07-03', end='2020-07-23')

# Get data shape: rows x columns
df.shape

# Visualize data closing price history
plt.figure(figsize=(20, 8))
plt.title('Intel Closing Price History')
plt.plot(df['Close'])
plt.xlabel('Date', fontsize = 15)
plt.ylabel('Price $USD', fontsize=17)
plt.show()

# Filter to get just the close price dataframe
closeDf = df.filter(['Close'])

# convert the dataframe to a numpy array
dataset = closeDf.values
print(dataset)
# get training data length: 70%
training_data_len = math.ceil(len(dataset) * .7)

# Preprocess data by scaling
scaler = MinMaxScaler(feature_range=(0,1))

scaled_data = scaler.fit_transform(dataset)
scaled_data.shape

# split training data from sacled dataset
train_data = scaled_data[0:training_data_len]

train_data

# split features on 50 day price windows where features are 50 day rolling values
# and predictions are the next value after each window

x_train = []
y_train = []

for i in range(50, training_data_len):
    x_train.append(train_data[i-50:i])
    y_train.append(train_data[i])

# Convert the x and y train values into numpy arrays
x_train, y_train = np.array(x_train), np.array(y_train)

# Build model layers
model = k.Sequential()
layer1 = k.layers.LSTM(50, return_sequences=True, input_shape=(50, 1))
model.add(layer=layer1)
layer2 = k.layers.LSTM(50, return_sequences=False)
model.add(layer=layer2)
model.add(k.layers.Dense(25))
model.add(k.layers.Dense(1))

# Compile model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train model
model.fit(x_train, y_train, batch_size=1, epochs=1)

# Create testing dataset for x_train and y_train
test_data = scaled_data[training_data_len - 50:]
x_test = []
y_test = dataset[training_data_len : ]

for i in range(50 , len(test_data)):
  x_test.append(test_data[i - 50 : i])

# convert x_test to numpy array
x_test = np.array(x_test)

# get predictions for x_test
predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)

# get RMSE
rmse = np.sqrt(np.mean(predictions - y_test)**2)
rmse

print(predictions[532])
print(y_test[532])

# Visualize data
train = closeDf[:training_data_len]
valid = closeDf[training_data_len:]
valid['predictions'] = predictions

plt.figure(figsize=(16, 8))
plt.title('Model predictions')
plt.xlabel('Date')
plt.ylabel('Close price $USD')
plt.plot(train['Close'])
plt.plot(valid['Close'])
plt.plot(valid['predictions'])
plt.legend(['Train', 'Valid', 'Prediction'], loc='upper left')
plt.show()

# Predict the weeks close
test = []
test.append(scaled_data[ -50:])
test = np.array(test)
predicted_close = model.predict(test, batch_size=1)
predicted_close = scaler.inverse_transform(predicted_close)

# Actual data
close = web.DataReader('INTC', data_source='yahoo', start='2020-07-24', end='2020-07-24')

assertion = {
    "Prediction": predicted_close[0][0],
    "Actual": close['Close'][-1]
}

# INTEL price dropped on the 24th following an earnings call
# Future work would be to making a model that's dynamic around such quarterly results
print(assertion)