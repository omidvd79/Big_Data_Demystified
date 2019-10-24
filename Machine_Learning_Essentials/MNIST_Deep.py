#
#   Multiple layer MNIST classifier in tensorflow
#

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

# Create input object which reads data from MNIST datasets.  Perform one-hot encoding to define the digit
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

# Using Interactive session makes it the default sessions so we do not need to pass sess
sess = tf.InteractiveSession()

# Define placeholders for MNIST input data
x = tf.placeholder(tf.float32, shape=[None, 784])
y_ = tf.placeholder(tf.float32, [None, 10])

# change the MNIST input data from a list of values to a 28 pixel X 28 pixel X 1 
#    grayscale value cube which the Convolution NN can use.
x_image = tf.reshape(x, [-1,28,28,1], name="x_image")

# Define helper functions to created weights and biases variables, and convolution, and pooling layers
#   We are using RELU as our activation function.  These must be initialized to a small positive number 
#   and with some noise so you don't end up going to zero when comparing diffs
def init_weight_variables(TensorShape):
    initial = tf.truncated_normal(TensorShape, stddev=0.1)
    return tf.Variable(initial)

def init_bias_variables(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

#   Convolution 
def conv_2D(x, W): # x is the image and W=weights
    # stride= the steps and direction to shift for every feature
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME') 

# Pooling to control overfitting
def pool_2x2(x):
    # ksize = the kernel size = the area we are pooling together 
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                        strides=[1, 2, 2, 1], padding='SAME')

# Define layers in the NN

# 1st Convolution layer:
#    32 features for each 5X5 patch of the image
#    1 input channel since these are grayscale images (for color image we used 3 channels RGB)
W_conv1 = init_weight_variables([5, 5, 1, 32])
b_conv1 = init_bias_variables([32])

# Do convolution on images, add bias and push through RELU activation
h_conv1 = tf.nn.relu(conv_2D(x_image, W_conv1) + b_conv1)
# take results and run through max_pool
h_pool1 = pool_2x2(h_conv1)


# The output of pool1 will be 14x14 matrixes (because we started with 28x28 and stride = 2)

# 2nd Convolution layer
# Process the 32 features from Convolution layer 1, in 5 X 5 patch.  Return 64 features weights and biases
W_conv2 = init_weight_variables([5, 5, 32, 64])
b_conv2 = init_bias_variables([64])
# Do convolution of the output of the 1st convolution layer.  Pool results 
h_conv2 = tf.nn.relu(conv_2D(h_pool1, W_conv2) + b_conv2)
h_pool2 = pool_2x2(h_conv2)

# The output of pool1 will be 7x7 matrixes (because we started from pool1 
#    with 14x14 and stride = 2)

# Fully Connected Layer
W_fc1 = init_weight_variables([7 * 7 * 64, 1024])
b_fc1 = init_bias_variables([1024])
#   Connect output of pooling layer 2 as input to full connected layer
h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

# dropout some neurons to reduce overfitting
keep_prob = tf.placeholder(tf.float32)  # get dropout probability as a training input.
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

# Readout layer
W_fc2 = init_weight_variables([1024, 10])
b_fc2 = init_bias_variables([10])

# Define model
y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2

# Loss measurement
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=y_conv, labels=y_))

# loss optimization
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

# What is correct
correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
# How accurate is it?
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# Initialize all of the variables
sess.run(tf.global_variables_initializer())

# Train the model
import time

#  define number of steps and how often we display progress
num_steps = 2000
batch_size = 100

# Start timer
start_time = time.time()
end_time = time.time()
for i in range(num_steps):
    batch = mnist.train.next_batch(batch_size)
    train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})

    # Periodic status display
    if i%batch_size == 0:
        train_accuracy = accuracy.eval(feed_dict={
            x:batch[0], y_: batch[1], keep_prob: 1.0})
        end_time = time.time()
        print("step {0}, elapsed time {1:.2f} seconds, training accuracy {2:.3f}%".format(i, end_time-start_time, train_accuracy*100.0))

# Display summary 
#     Time to train
end_time = time.time()
print("Total training time for {0} batches: {1:.2f} seconds".format(i+1, end_time-start_time))
#     Accuracy on test data

print("Test accuracy {0:.3f}%".format(accuracy.eval(feed_dict={
    x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0})*100.0))

    