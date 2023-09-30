import torch
import tensorflow as tf
if torch.cuda.is_available():
    print("GPU is available.")
else:
    print("GPU is not available.")



print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
