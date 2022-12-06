from keras import Sequential
from keras.layers import Embedding, LSTM, Dense
from keras.metrics import Precision, Recall

def create_lstm_model(embedding_input_dim, embedding_output_dim, input_length, lstm_units, dropout_rate):
    model = Sequential(name="LSTM")
    
    model.add(
        Embedding(
            input_dim=embedding_input_dim,
            output_dim=embedding_output_dim,
            input_length=input_length,
            name="embedding"
        )
    )
    
    for idx, units in enumerate(lstm_units):
        is_not_last_layer = (idx+1 != len(lstm_units))
        
        layer = LSTM(units=units,
                     dropout=dropout_rate, recurrent_dropout=dropout_rate,
                     return_sequences=is_not_last_layer, name=f"lstm_{idx+1}")
        model.add(layer)
    
    model.add(Dense(units=1, activation='sigmoid', name="output"))
    
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy', Precision(name='precision'), Recall(name='recall')]
    )
    
    print(model.summary())
    return model