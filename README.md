# stock-price-prediction-ML
LSTM based model for stock price prediction

Simple model demonstration of stock price prediction using an LSTM RNN with adam optimizer
model is trained on 50 day rolling data for the INTEL stock closing price

Model accuracy is decent at 0.76 RSME
However as you'll notice on the final preditcion, it fails to account for earnings calls which affect stock prices beyond historical 50 day trends

Future work on such models should have them work ensemble with more advanced models trained on features relating to earnings performance oor sentiment
