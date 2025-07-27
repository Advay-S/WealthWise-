import numpy as np
from keras.layers import Dense, LSTM
from keras.models import Sequential
from sklearn.preprocessing import MinMaxScaler

def prediction_stock_price(prices):
    prices = np.array(prices).reshape(-1,1)

    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_prices = scaler.fit_transform(prices)

    look_back = 45
    x,y = [] , []

    for i in range(len(scaled_prices) - look_back):
        x.append(scaled_prices[i:i + look_back])
        y.append(scaled_prices[i + look_back])


    x = np.array(x)
    y = np.array(y)

    x = x.reshape((x.shape[0], x.shape[1], 1))

    model = Sequential()
    model.add(LSTM(50, return_sequences=False, input_shape = (look_back, 1)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')

    model.fit(x , y , epochs=10, batch_size=1, verbose=0)

    last_45_days = scaled_prices[-look_back:]
    last_45_days = last_45_days.reshape((1, look_back, 1))
    predicted_scaled = model.predict(last_45_days)
    predicted_price = scaler.inverse_transform(predicted_scaled)

    return predicted_price[0][0]

