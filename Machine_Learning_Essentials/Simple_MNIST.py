#
#   DeepMNIST.py - Multiple layer MNIST classifier in tensorflow
#

import tensorflow as tf

#Using the TensorFlow function to download the data from the MNIST site.
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

# x is the placeholder for the 28x28=784 pixels image data 
x = tf.placeholder(tf.float32, shape=[None, 784]) #None - the dimension exists but the size is unknown

# y_ (named "y bar") holds a 10 element vector containing the predicted probability 
# of each digit (0-9). for example: [0.1, 0.8, 0, 0, 0, 0, 0, 0, 0.1]
y_ = tf.placeholder(tf.float32, [None, 10])

# Define weights and biases - the variables
W = tf.Variable(tf.zeros([784,10]))
b = tf.Variable(tf.zeros([10]))

# Apply the sum of matrix multiplication and the activation function
y = tf.nn.softmax(tf.matmul(x,W) + b)

# We need to compare the predicted digit (in "y") with the actual digit in the data.
# so we define the loss measurement (or error measurement) function
cross_entropy = tf.reduce_mean(
                  tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y)) 

# each training step in gradient decent we want to minimize the cross entropy
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

# Initialize the global variables
init = tf.global_variables_initializer()

# Create an interactive session that can space multiple code blocks.
sess = tf.Session()

# Initialization of all global variables
sess.run(init)

batch_size = 100
for i in range (1000):
    # get 100 random images
    batch_xs, batch_ys = mnist.train.next_batch(batch_size) # batch_xs = image, batch_ys = digit (0-9) class

    # run the optimization with this data
    sess.run (train_step, feed_dict={x: batch_xs, y_: batch_ys})

# Evaluate how well the model did. Do this by comparing the digit with the highest probablity
#   in actual (y) and predicted (y_)
    
correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
test_accuracy = sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels})
print ("Test accuracy: {0}%".format(test_accuracy * 100.0))

sess.close()
