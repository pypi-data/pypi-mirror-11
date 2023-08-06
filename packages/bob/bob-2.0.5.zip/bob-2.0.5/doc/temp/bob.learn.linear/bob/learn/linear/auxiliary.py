"""Auxiliary functions to be used for preparing the training data."""


def bic_intra_extra_pairs(training_data):
  """bic_intra_extra_pairs(training_data) -> intra_pairs, extra_pairs

  Computes intra-class and extra-class pairs from given training data.

  The ``training_data`` should be aligned in a list of sub-lists, where each sub-list contains the data of one class.
  This function will return two lists of tuples of data, where the first list contains tuples of the same class, while the second list contains tuples of different classes.
  These tuples can be used to compute difference vectors, which then can be fed into the :py:meth:`bob.learn.linear.BICTrainer.train` method.

  Note that in general many more ``extra_pairs?`` than ``intra_pairs`` are returned.

  **Keyword parameters**

  training_data : [[array_like]]
    The training data, where the data for each class are enclosed in one list.

  **Return values**

  intra_pairs : [(array_like, array_like)]
    A list of tuples of data, where both data belong to the same class, where each data element is a reference to one element of the given ``training_data``.

  extra_pairs : [(array_like, array_like)]
    A list of tuples of data, where both data belong to different classes, where each data element is a reference to one element of the given ``training_data``.
  """
  # generate intra-class pairs
  intra_pairs = []
  for clazz in range(len(training_data)):
    for c1 in range(len(training_data[clazz])-1):
      for c2 in range (c1+1, len(training_data[clazz])):
        intra_pairs.append((training_data[clazz][c1], training_data[clazz][c2]))

  # generate extra-class pairs
  extra_pairs = []
  for clazz1 in range(len(training_data)-1):
    for c1 in range(len(training_data[clazz1])):
      for clazz2 in range(clazz1+1, len(training_data)):
        if clazz1 != clazz2:
          for c2 in range(len(training_data[clazz2])):
            extra_pairs.append((training_data[clazz1][c1], training_data[clazz2][c2]))

  # return a tuple of pairs
  return (intra_pairs, extra_pairs)
