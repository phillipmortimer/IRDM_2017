import numpy as np
from keras import metrics
from keras.layers import Activation, Dense
from keras.models import Sequential
from keras.optimizers import SGD, Adam, RMSprop
from keras.regularizers import l2
from keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard
import os
import glob


class PointwiseRanker(object):
  """Pointwise ranking algorithm using a logistic regression or MLP models.

  :param input_dim: int
    The dimensionality of the input features.
  :param n_classes: int
    The number of classes.
  :param model_type: string (optional)
    One of `"logreg"`, `"MLP"`. Specifies the type of model for the classifer.
    `"logreg"` uses logistic regression, `"MLP"` multi-layer perceptron.
  :param C: float (optional)
    L2 reguralisation coefficient for logistic regression.
  :param epochs: int (optional)
    The maximum number of epoch to train for.
  :param batch_size: int (optional)
    The batch size used in training.
  :param class_weight: string (optional)
    One of "`balanced`" or None.  "`balanced`" results in rebalancing
    the class weights in the loss function.
  :param: model_dir: string (optional)
    Specifies directory to save the trained model.
    If None, the model is not saved.
  """

  def __init__(self, input_dim, n_classes, model_type='logreg', C=0.1, epochs=10, batch_size=256,
               class_weight=None, model_dir=None):
    self.input_dim = input_dim
    self.n_classes = n_classes
    self.model = None
    self.C = C
    self.epochs = epochs
    self.batch_size = batch_size
    self.class_weight = class_weight
    self.model = None
    self.model_dir = model_dir
    self.model_type = model_type
    self.model_init()


  def fit(self, X, y, validation_data=None):
    """Fits the model.

    :param  X: Numpy array
      Samples in rows, features in columns.
    :param y: Numpy vector
      Labels.
    :param validation_data: tuple
      A tuple (X_val, y_val) of validation data. If None, validation score
      is not reported during the training.
    """
    callbacks = []
    early_stopping = EarlyStopping(monitor='val_loss', patience=2,
                                   verbose=1, mode='auto')
    callbacks.append(early_stopping)

    if self.model_dir is not None:
      os.makedirs(self.model_dir, exist_ok=True)
      checkpointer = ModelCheckpoint(
        filepath=self.model_dir + os.sep + 'weights-{val_loss:.3f}-{epoch:02d}.hdf5',
        verbose=1, save_best_only=True, save_weights_only=True)
      callbacks.append(checkpointer)

    if self.class_weight == 'balanced':
      classes_counts, _ = np.histogram(y, bins=self.n_classes)
      class_weights = 1 / classes_counts
      class_weights = self.n_classes * class_weights / np.sum(class_weights)
    else:
      class_weights = np.ones((self.n_classes))

    class_weights_dict = dict(zip(list(range(self.n_classes)),
                                  class_weights.tolist()))

    self.model.fit(X, y, batch_size=self.batch_size, epochs=self.epochs,
                   validation_data=validation_data,
                   class_weight=class_weights_dict,
                   callbacks=callbacks)


  def model_init(self):
    optimizer = RMSprop()
    self.model = Sequential()

    if self.model_type == 'MLP':
      self.model.add(Dense(200, input_dim=self.input_dim, activation='relu'))
      self.model.add(Dense(200, activation='relu'))
      self.model.add(Dense(self.n_classes))
    elif self.model_type == 'logreg':
      reg = l2(self.C)
      self.model.add(Dense(self.n_classes, kernel_regularizer=reg,
                           input_dim=self.input_dim))
    else:
      raise ValueError('Unsupported model type: ' + self.model_type)

    self.model.add(Activation('softmax'))
    self.model.compile(optimizer=optimizer,
                       loss='sparse_categorical_crossentropy',
                       metrics=['accuracy'])


  def predict(self, X):
    """Predicts classes given features.

    :param X: Numpy array
      Samples in rows, features in columns.

    :return: Numpy vector
      Predicted classes.
    """
    predictions = self.model.predict_classes(X, batch_size=self.batch_size,
                                             verbose=1)
    return predictions


  def load_model(self):
    models = glob.glob(self.model_dir + os.sep + 'weights-*-*.hdf5')
    losses = np.array([float(model.split(os.sep)[-1].split('-')[1]) for model in models])
    idx = np.argmin(losses)
    self.model.load_weights(models[idx])
