import numpy as np


def affine_forward(x, w, b):
  """
  Computes the forward pass for an affine (fully-connected) layer.

  The input x has shape (N, d_1, ..., d_k) and contains a minibatch of N
  examples, where each example x[i] has shape (d_1, ..., d_k). We will
  reshape each input into a vector of dimension D = d_1 * ... * d_k, and
  then transform it to an output vector of dimension M.

  Inputs:
  - x: A numpy array containing input data, of shape (N, d_1, ..., nk)
  - w: A numpy array of weights, of shape (D, M)
  - b: A numpy array of biases, of shape (M,)
  
  Returns a tuple of:
  - out: output, of shape (N, M)
  - cache: (x, w, b)
  """
  out = None
  #############################################################################
  # TODO: Implement the affine forward pass. Store the result in out. You     #
  # will need to reshape the input into rows.                                 #
  #############################################################################
  D = 1
  N = x.shape[0]
  for index, shape in enumerate(x.shape):
        if index == 0:
            continue 
        else:
            D *= shape 
  
  x_flattened = x.reshape(N, D)
  out = np.dot(x_flattened, w) + b
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = (x, w, b)
  return out, cache


def affine_backward(dout, cache):
  """
  Computes the backward pass for an affine layer.

  Inputs:
  - dout: Upstream derivative, of shape (N, M)
  - cache: Tuple of:
    - x: Input data, of shape (N, d_1, ... d_k)
    - w: Weights, of shape (D, M)

  Returns a tuple of:
  - dx: Gradient with respect to x, of shape (N, d1, ..., d_k)
  - dw: Gradient with respect to w, of shape (D, M)
  - db: Gradient with respect to b, of shape (M,)
  """
  x, w, b = cache
  dx, dw, db = None, None, None
  #############################################################################
  # TODO: Implement the affine backward pass.                                 #
  #############################################################################
  D = 1
  N = x.shape[0]
  for index, shape in enumerate(x.shape):
        if index == 0:
            continue 
        else:
            D *= shape 
            
  dloss = 1
  dx = np.dot(dout, w.T).reshape(x.shape)
  db = np.sum(dout.T, axis=1)
  dw = np.dot(x.reshape(N, D).T, dout)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx, dw, db


def relu_forward(x):
  """
  Computes the forward pass for a layer of rectified linear units (ReLUs).

  Input:
  - x: Inputs, of any shape

  Returns a tuple of:
  - out: Output, of the same shape as x
  - cache: x
  """
  out = None
  #############################################################################
  # TODO: Implement the ReLU forward pass.                                    #
  #############################################################################
  out = np.maximum(0, x)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = x
  return out, cache


def relu_backward(dout, cache):
  """
  Computes the backward pass for a layer of rectified linear units (ReLUs).

  Input:
  - dout: Upstream derivatives, of any shape
  - cache: Input x, of same shape as dout

  Returns:
  - dx: Gradient with respect to x
  """
  dx, x = None, cache
  #############################################################################
  # TODO: Implement the ReLU backward pass.                                   #
  #############################################################################
  dx = (dout * (x > 0).astype(int))
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx


def batchnorm_forward(x, gamma, beta, bn_param):
  """
  Forward pass for batch normalization.
  
  During training the sample mean and (uncorrected) sample variance are
  computed from minibatch statistics and used to normalize the incoming data.
  During training we also keep an exponentially decaying running mean of the mean
  and variance of each feature, and these averages are used to normalize data
  at test-time.

  At each timestep we update the running averages for mean and variance using
  an exponential decay based on the momentum parameter:

  running_mean = momentum * running_mean + (1 - momentum) * sample_mean
  running_var = momentum * running_var + (1 - momentum) * sample_var

  Note that the batch normalization paper suggests a different test-time
  behavior: they compute sample mean and variance for each feature using a
  large number of training images rather than using a running average. For
  this implementation we have chosen to use running averages instead since
  they do not require an additional estimation step; the torch7 implementation
  of batch normalization also uses running averages.

  Input:
  - x: Data of shape (N, D)
  - gamma: Scale parameter of shape (D,)
  - beta: Shift paremeter of shape (D,)
  - bn_param: Dictionary with the following keys:
    - mode: 'train' or 'test'; required
    - eps: Constant for numeric stability
    - momentum: Constant for running mean / variance.
    - running_mean: Array of shape (D,) giving running mean of features
    - running_var Array of shape (D,) giving running variance of features

  Returns a tuple of:
  - out: of shape (N, D)
  - cache: A tuple of values needed in the backward pass
  """
  mode = bn_param['mode']
  eps = bn_param.get('eps', 1e-5)
  momentum = bn_param.get('momentum', 0.9)

  N, D = x.shape
  running_mean = bn_param.get('running_mean', np.zeros(D, dtype=x.dtype))
  running_var = bn_param.get('running_var', np.zeros(D, dtype=x.dtype))

  out, cache = None, None
  if mode == 'train':
    #############################################################################
    # TODO: Implement the training-time forward pass for batch normalization.   #
    # Use minibatch statistics to compute the mean and variance, use these      #
    # statistics to normalize the incoming data, and scale and shift the        #
    # normalized data using gamma and beta.                                     #
    #                                                                           #
    # You should store the output in the variable out. Any intermediates that   #
    # you need for the backward pass should be stored in the cache variable.    #
    #                                                                           #
    # You should also use your computed sample mean and variance together with  #
    # the momentum variable to update the running mean and running variance,    #
    # storing your result in the running_mean and running_var variables.        #
    #############################################################################
    sample_mean = x.mean(axis=0) 
    x_shifted = x - sample_mean
    x_shifted_squared = np.square(x_shifted)
    x_shifted_squared_summed = np.sum(x_shifted_squared, axis=0) / x.shape[0]
    sample_var = np.sqrt(x_shifted_squared_summed) + eps
    x_normalized = x_shifted / sample_var
    out = (x_normalized * gamma) + beta
    cache = (
        x, gamma, beta, x_normalized, sample_var, x_shifted_squared_summed, 
        x_shifted_squared, x_shifted, sample_mean
    )
    running_mean = (running_mean * momentum) + ((1 - momentum) * sample_mean)
    running_var = ((running_var * momentum)) + ((1 - momentum) * sample_var)
    #############################################################################
    #                             END OF YOUR CODE                              #
    #############################################################################
  elif mode == 'test':
    #############################################################################
    # TODO: Implement the test-time forward pass for batch normalization. Use   #
    # the running mean and variance to normalize the incoming data, then scale  #
    # and shift the normalized data using gamma and beta. Store the result in   #
    # the out variable.                                                         #
    #############################################################################
    x_normalized = (x - running_mean) / (running_var + eps)
    out = (x_normalized * gamma) + beta
    #############################################################################
    #                             END OF YOUR CODE                              #
    #############################################################################
  else:
    raise ValueError('Invalid forward batchnorm mode "%s"' % mode)

  # Store the updated running means back into bn_param
  bn_param['running_mean'] = running_mean
  bn_param['running_var'] = running_var

  return out, cache


def batchnorm_backward(dout, cache):
  """
  Backward pass for batch normalization.
  
  For this implementation, you should write out a computation graph for
  batch normalization on paper and propagate gradients backward through
  intermediate nodes.
  
  Inputs:
  - dout: Upstream derivatives, of shape (N, D)
  - cache: Variable of intermediates from batchnorm_forward.
  
  Returns a tuple of:
  - dx: Gradient with respect to inputs x, of shape (N, D)
  - dgamma: Gradient with respect to scale parameter gamma, of shape (D,)
  - dbeta: Gradient with respect to shift parameter beta, of shape (D,)
  """
  x, gamma, beta, x_normalized, sample_var, x_shifted_squared_summed, x_shifted_squared, x_shifted, sample_mean = cache
  dx, dgamma, dbeta = None, None, None
  #############################################################################
  # TODO: Implement the backward pass for batch normalization. Store the      #
  # results in the dx, dgamma, and dbeta variables.                           #
  #############################################################################
  # out = (x_normalized * gamma) + beta
  dx_normalized = dout * gamma
  dgamma = np.sum(x_normalized * dout, axis=0)
  dbeta = np.sum(dout, axis=0)

  # x_normalized = x_shifted / sample_var
  dx_shifted = dx_normalized / sample_var
  dsample_var = np.sum(x_shifted * dx_normalized * (-1 / np.square(sample_var)), axis=0)
    
  # sample_var = np.sqrt(x_shifted_squared_summed) + eps
  dx_shifted_squared_summed = dsample_var * (0.5 * (1 / np.sqrt(x_shifted_squared_summed)))
  
  # x_shifted_squared_summed = np.sum(x_shifted_squared, axis=0) / x.shape[0]
  dx_shifted_squared = np.ones(x_shifted_squared.shape) * dx_shifted_squared_summed / x.shape[0] 

  # x_shifted_squared = np.square(x_shifted)
  dx_shifted += dx_shifted_squared * x_shifted * 2

  # x_shifted = x - sample_mean
  dx = dx_shifted
  dsample_mean = -1 * np.sum(dx_shifted, axis=0)
    
  # sample_mean = x.mean(axis=0) 
  dx += (np.ones(x.shape) * dsample_mean / x.shape[0])

  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  
  return dx, dgamma, dbeta


def batchnorm_backward_alt(dout, cache):
  """
  Alternative backward pass for batch normalization.
  
  For this implementation you should work out the derivatives for the batch
  normalizaton backward pass on paper and simplify as much as possible. You
  should be able to derive a simple expression for the backward pass.
  
  Note: This implementation should expect to receive the same cache variable
  as batchnorm_backward, but might not use all of the values in the cache.
  
  Inputs / outputs: Same as batchnorm_backward
  """
  dx, dgamma, dbeta = None, None, None
  #############################################################################
  # TODO: Implement the backward pass for batch normalization. Store the      #
  # results in the dx, dgamma, and dbeta variables.                           #
  #                                                                           #
  # After computing the gradient with respect to the centered inputs, you     #
  # should be able to compute gradients with respect to the inputs in a       #
  # single statement; our implementation fits on a single 80-character line.  #
  #############################################################################
  pass
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  
  return dx, dgamma, dbeta


def dropout_forward(x, dropout_param):
  """
  Performs the forward pass for (inverted) dropout.

  Inputs:
  - x: Input data, of any shape
  - dropout_param: A dictionary with the following keys:
    - p: Dropout parameter. We drop each neuron output with probability p.
    - mode: 'test' or 'train'. If the mode is train, then perform dropout;
      if the mode is test, then just return the input.
    - seed: Seed for the random number generator. Passing seed makes this
      function deterministic, which is needed for gradient checking but not in
      real networks.

  Outputs:
  - out: Array of the same shape as x.
  - cache: A tuple (dropout_param, mask). In training mode, mask is the dropout
    mask that was used to multiply the input; in test mode, mask is None.
  """
  p, mode = dropout_param['p'], dropout_param['mode']
  if 'seed' in dropout_param:
    np.random.seed(dropout_param['seed'])

  mask = None
  out = None

  if mode == 'train':
    ###########################################################################
    # TODO: Implement the training phase forward pass for inverted dropout.   #
    # Store the dropout mask in the mask variable.                            #
    ###########################################################################
    mask = np.random.rand(x.shape[0], x.shape[1]) < p
    out = x * mask
    #print(out.shape)
    ###########################################################################
    #                            END OF YOUR CODE                             #
    ###########################################################################
  elif mode == 'test':
    ###########################################################################
    # TODO: Implement the test phase forward pass for inverted dropout.       #
    ###########################################################################
    out = x * p 
    ###########################################################################
    #                            END OF YOUR CODE                             #
    ###########################################################################

  cache = (dropout_param, mask)
  out = out.astype(x.dtype, copy=False)
  #print(out)

  return out, cache


def dropout_backward(dout, cache):
  """
  Perform the backward pass for (inverted) dropout.

  Inputs:
  - dout: Upstream derivatives, of any shape
  - cache: (dropout_param, mask) from dropout_forward.
  """
  dropout_param, mask = cache
  mode = dropout_param['mode']
  
  dx = None
  if mode == 'train':
    ###########################################################################
    # TODO: Implement the training phase backward pass for inverted dropout.  #
    ###########################################################################
    dx = dout * mask
    ###########################################################################
    #                            END OF YOUR CODE                             #
    ###########################################################################
  elif mode == 'test':
    dx = dout
  return dx


def conv_forward_naive(x, w, b, conv_param):
  """
  A naive implementation of the forward pass for a convolutional layer.

  The input consists of N data points, each with C channels, height H and width
  W. We convolve each input with F different filters, where each filter spans
  all C channels and has height HH and width HH.

  Input:
  - x: Input data of shape (N, C, H, W)
  - w: Filter weights of shape (F, C, HH, WW)
  - b: Biases, of shape (F,)
  - conv_param: A dictionary with the following keys:
    - 'stride': The number of pixels between adjacent receptive fields in the
      horizontal and vertical directions.
    - 'pad': The number of pixels that will be used to zero-pad the input.

  Returns a tuple of:
  - out: Output data, of shape (N, F, H', W') where H' and W' are given by
     1 + (4 + 2*1 - 4) / 2 = 3
    H' = 1 + (H + 2 * pad - HH) / stride
    W' = 1 + (W + 2 * pad - WW) / stride
  - cache: (x, w, b, conv_param)
  """
   
  out = None
  pad = conv_param['pad']
  stride = conv_param['stride']
  N = x.shape[0]
  C = x.shape[1]
  H = x.shape[2]
  W = x.shape[3]
  F = w.shape[0]
  FILTER_HEIGHT = w.shape[2]
  FILTER_WIDTH = w.shape[3]
  H_prime = int(1 + np.true_divide(H + 2 * pad - FILTER_HEIGHT, stride))
  W_prime = int(1 + np.true_divide(W + 2 * pad - FILTER_WIDTH,  stride))
  out = np.zeros((N, F, H_prime, W_prime))
  #############################################################################
  # TODO: Implement the convolutional forward pass.                           #
  # Hint: you can use the function np.pad for padding.                        #
  #############################################################################
  for example_index in range(0, x.shape[0]):
        example = np.pad(x[example_index], pad_width=((0, 0), (pad, pad), (pad, pad)), mode='constant')
        example_height = example.shape[1]
        example_width = example.shape[2]
        
        # Iterate over each filter. 
        for filter_index in range(0, w.shape[0]):
            current_w = w[filter_index]
            
            start_i = 0
            start_j = 0
            out_i = 0
            out_j = 0
            while(start_i + FILTER_HEIGHT <= example_height):
                # Get example volume at start_i, start_j. 
                current_X = example[
                    :, 
                    start_i: start_i + FILTER_HEIGHT, 
                    start_j: start_j + FILTER_WIDTH
                ]
                current_result = np.sum(current_X * current_w) + b[filter_index]
                
                # Update out
                out[example_index, filter_index, out_i, out_j] = current_result 
         
                # Code to organize the update
                if start_j + FILTER_WIDTH >= example_width:
                    start_i += stride
                    start_j = 0
                else:
                    start_j += stride
                if out_j == W_prime - 1:
                    out_i += 1
                    out_j = 0
                else:
                    out_j += 1
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = (x, w, b, conv_param)
  return out, cache

def is_pad_coordinate(i, j, pad, padded_dim):
    if (
        i < pad or 
        i >= padded_dim[0] - pad or 
        j < pad or 
        j >= padded_dim[1] - pad
    ):
        return True
    else:
        return False

def padded_coordinate_to_reg(pad_i, pad_j, pad):
    return (pad_i - pad, pad_j - pad)
    
def conv_backward_naive(dout, cache):
  """
  A naive implementation of the backward pass for a convolutional layer.

  Inputs:
  - dout: Upstream derivatives.
  - cache: A tuple of (x, w, b, conv_param) as in conv_forward_naive

  Returns a tuple of:
  - dx: Gradient with respect to x
  - dw: Gradient with respect to w
  - db: Gradient with respect to b
  """
  x, w, b, conv_param = cache
  pad = conv_param['pad']
  stride = conv_param['stride']
  N = x.shape[0]
  C = x.shape[1]
  H = x.shape[2]
  W = x.shape[3]
  F = w.shape[0]
  C = w.shape[1]
  FILTER_HEIGHT = w.shape[2]
  FILTER_WIDTH = w.shape[3]
  H_prime = int(1 + np.true_divide(H + 2 * pad - FILTER_HEIGHT, stride))
  W_prime = int(1 + np.true_divide(W + 2 * pad - FILTER_WIDTH,  stride))
  out = np.zeros((N, F, H_prime, W_prime))
  dx, dw, db = np.zeros(x.shape), np.zeros(w.shape), np.zeros(b.shape)
  #############################################################################
  # TODO: Implement the convolutional backward pass.                          #
  #############################################################################
  for example_index in range(0, x.shape[0]):
      example = np.pad(x[example_index], pad_width=((0, 0), (pad, pad), (pad, pad)), mode='constant')
      example_height = example.shape[1]
      example_width = example.shape[2]

      # Iterate over each filter. 
      for filter_index in range(0, w.shape[0]):
          current_w = w[filter_index]

          start_i = 0
          start_j = 0
          out_i = 0
          out_j = 0
          while(start_i + FILTER_HEIGHT <= example_height):
              # Get example volume at start_i, start_j. 
              current_X = example[
                  :, 
                  start_i: start_i + FILTER_HEIGHT, 
                  start_j: start_j + FILTER_WIDTH
              ]
              current_result = np.sum(current_X * current_w) + b[filter_index]
              
              # Update dw 
              dw[filter_index, :, :, :] += current_X * dout[example_index, filter_index, out_i, out_j]
              
              # Update dx 
              #print(dout[example_index, filter_index, out_i, out_j], dout[example_index, filter_index, out_i, out_j].shape)
              padded_update = current_w * dout[example_index, filter_index, out_i, out_j]
              for pad_c in range(0, C):
                for pad_i in range(start_i, start_i + FILTER_HEIGHT):
                    for pad_j in range(start_j, start_j + FILTER_WIDTH):
                        if not is_pad_coordinate(pad_i, pad_j, pad, (example_height, example_width)):
                            mapped_i, mapped_j = padded_coordinate_to_reg(pad_i, pad_j, pad)
                            #print("dx shape", dx.shape)
                            #print("dx indices access", example_index, pad_c, mapped_i, mapped_j)
                            dx[example_index, pad_c, mapped_i, mapped_j] += (
                                current_w[pad_c, pad_i - start_i, pad_j - start_j] * 
                                dout[example_index, filter_index, out_i, out_j]
                            )
            
              # Update b
              db[filter_index] += dout[example_index, filter_index, out_i, out_j]
              
              # Update out
              out[example_index, filter_index, out_i, out_j] = current_result 

              # Code to organize the update
              if start_j + FILTER_WIDTH >= example_width:
                  start_i += stride
                  start_j = 0
              else:
                  start_j += stride
              if out_j == W_prime - 1:
                  out_i += 1
                  out_j = 0
              else:
                  out_j += 1
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx, dw, db


def max_pool_forward_naive(x, pool_param):
  """
  A naive implementation of the forward pass for a max pooling layer.

  Inputs:
  - x: Input data, of shape (N, C, H, W)
  - pool_param: dictionary with the following keys:
    - 'pool_height': The height of each pooling region
    - 'pool_width': The width of each pooling region
    - 'stride': The distance between adjacent pooling regions

  Returns a tuple of:
  - out: Output data
  - cache: (x, pool_param)
  """
  stride = pool_param['stride']
  N = x.shape[0]
  C = x.shape[1]
  H = x.shape[2]
  W = x.shape[3]
  POOL_HEIGHT = pool_param['pool_height']
  POOL_WIDTH = pool_param['pool_width']
  X_HEIGHT = x.shape[2]
  X_WIDTH = x.shape[3]
  H_prime = int(1 + np.true_divide(H - POOL_HEIGHT, stride))
  W_prime = int(1 + np.true_divide(W - POOL_WIDTH,  stride))
  out = np.zeros((N, C, H_prime, W_prime))
  #############################################################################
  # TODO: Implement the max pooling forward pass                              #
  #############################################################################
  for example_index in range(0, N):
          example = x[example_index]

          # Iterate over each volume. 
          for volume_index in range(0, C):

              start_i = 0
              start_j = 0
              out_i = 0
              out_j = 0
              while(start_i + POOL_HEIGHT <= X_HEIGHT):
                  # Get example volume at start_i, start_j. 
                  current_X = example[
                      volume_index, 
                      start_i: start_i + POOL_HEIGHT, 
                      start_j: start_j + POOL_WIDTH
                  ]
                  current_result = np.max(current_X)

                  # Update out
                  out[example_index, volume_index, out_i, out_j] = current_result 

                  # Code to organize the update
                  if start_j + POOL_WIDTH >= X_WIDTH:
                      start_i += stride
                      start_j = 0
                  else:
                      start_j += stride
                  if out_j == W_prime - 1:
                      out_i += 1
                      out_j = 0
                  else:
                      out_j += 1
    
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = (x, pool_param)
  return out, cache


def max_pool_backward_naive(dout, cache):
  """
  A naive implementation of the backward pass for a max pooling layer.

  Inputs:
  - dout: Upstream derivatives
  - cache: A tuple of (x, pool_param) as in the forward pass.

  Returns:
  - dx: Gradient with respect to x
  """
  x, pool_param = cache
  stride = pool_param['stride']
  N = x.shape[0]
  C = x.shape[1]
  H = x.shape[2]
  W = x.shape[3]
  POOL_HEIGHT = pool_param['pool_height']
  POOL_WIDTH = pool_param['pool_width']
  X_HEIGHT = x.shape[2]
  X_WIDTH = x.shape[3]
  H_prime = int(1 + np.true_divide(H - POOL_HEIGHT, stride))
  W_prime = int(1 + np.true_divide(W - POOL_WIDTH,  stride))
  out = np.zeros((N, C, H_prime, W_prime))
  dx = np.zeros(x.shape)
  #############################################################################
  # TODO: Implement the max pooling backward pass                              #
  #############################################################################
  for example_index in range(0, N):
          example = x[example_index]

          # Iterate over each volume. 
          for volume_index in range(0, C):

              start_i = 0
              start_j = 0
              out_i = 0
              out_j = 0
              while(start_i + POOL_HEIGHT <= X_HEIGHT):
                  # Get example volume at start_i, start_j. 
                  current_X = example[
                      volume_index, 
                      start_i: start_i + POOL_HEIGHT, 
                      start_j: start_j + POOL_WIDTH
                  ]
                  current_max_index = np.argmax(current_X)
                  max_i, max_j = current_max_index / current_X.shape[0], (current_max_index % current_X.shape[0])
                  #print(max_i, max_j, current_max_index, current_X.shape)
                  update_x = np.zeros(current_X.shape)
                  #print("update_X shape", update_x.shape)
                  update_x[max_i, max_j] = dout[example_index, volume_index, out_i, out_j]

                  # Update out
                  current_result = np.max(current_X)
                  out[example_index, volume_index, out_i, out_j] = current_result 
                  
                  # Update dx. 
                  #print(update_x.shape)
                  dx[
                    example_index,
                    volume_index, 
                    start_i: start_i + POOL_HEIGHT, 
                    start_j: start_j + POOL_WIDTH
                  ] += update_x

                  # Code to organize the update
                  if start_j + POOL_WIDTH >= X_WIDTH:
                      start_i += stride
                      start_j = 0
                  else:
                      start_j += stride
                  if out_j == W_prime - 1:
                      out_i += 1
                      out_j = 0
                  else:
                      out_j += 1
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx


def spatial_batchnorm_forward(x, gamma, beta, bn_param):
  """
  Computes the forward pass for spatial batch normalization.
  
  Inputs:
  - x: Input data of shape (N, C, H, W)
  - gamma: Scale parameter, of shape (C,)
  - beta: Shift parameter, of shape (C,)
  - bn_param: Dictionary with the following keys:
    - mode: 'train' or 'test'; required
    - eps: Constant for numeric stability
    - momentum: Constant for running mean / variance. momentum=0 means that
      old information is discarded completely at every time step, while
      momentum=1 means that new information is never incorporated. The
      default of momentum=0.9 should work well in most situations.
    - running_mean: Array of shape (D,) giving running mean of features
    - running_var Array of shape (D,) giving running variance of features
    
  Returns a tuple of:
  - out: Output data, of shape (N, C, H, W)
  - cache: Values needed for the backward pass
  """
  out, cache = None, {}
  cache['x'] = x
  cache['gamma'] = gamma
  cache['beta'] = beta
  cache['bn_param'] = bn_param
  N, C, H, W = x.shape
  #############################################################################
  # TODO: Implement the forward pass for spatial batch normalization.         #
  #                                                                           #
  # HINT: You can implement spatial batch normalization using the vanilla     #
  # version of batch normalization defined above. Your implementation should  #
  # be very short; ours is less than five lines.                              #
  #############################################################################
  x_by_channel = x.transpose(1, 0, 2, 3)
  x_by_channel_flattened = x_by_channel.reshape(C, N * H * W).transpose(1, 0)
  out, current_cache = batchnorm_forward(x_by_channel_flattened, gamma, beta, bn_param) 
  out = out.transpose(1, 0).reshape(C, N * H * W)
  out = out.reshape(C, N, H, W).transpose(1, 0, 2, 3) 
  cache['bp_cache'] = current_cache
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  
  return out, cache


def spatial_batchnorm_backward(dout, cache):
  """
  Computes the backward pass for spatial batch normalization.
  
  Inputs:
  - dout: Upstream derivatives, of shape (N, C, H, W)
  - cache: Values from the forward pass
  
  Returns a tuple of:
  - dx: Gradient with respect to inputs, of shape (N, C, H, W)
  - dgamma: Gradient with respect to scale parameter, of shape (C,)
  - dbeta: Gradient with respect to shift parameter, of shape (C,)
  """
  dx, dgamma, dbeta = np.zeros(dout.shape), np.zeros(cache['gamma'].shape), np.zeros(cache['beta'].shape)
  N, C, H, W = dout.shape
  #############################################################################
  # TODO: Implement the backward pass for spatial batch normalization.        #
  #                                                                           #
  # HINT: You can implement spatial batch normalization using the vanilla     #
  # version of batch normalization defined above. Your implementation should  #
  # be very short; ours is less than five lines.                              #
  #############################################################################
  dout_reshaped = dout.transpose(1, 0, 2, 3).reshape(C, N * H * W).transpose(1, 0)
  dx, dgamma, dbeta = batchnorm_backward(dout_reshaped, cache['bp_cache'])
  dx = dx.transpose(1, 0).reshape(C, N, H, W).transpose(1, 0, 2, 3)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

  return dx, dgamma, dbeta
  

def svm_loss(x, y):
  """
  Computes the loss and gradient using for multiclass SVM classification.

  Inputs:
  - x: Input data, of shape (N, C) where x[i, j] is the score for the jth class
    for the ith input.
  - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
    0 <= y[i] < C

  Returns a tuple of:
  - loss: Scalar giving the loss
  - dx: Gradient of the loss with respect to x
  """
  N = x.shape[0]
  correct_class_scores = x[np.arange(N), y]
  margins = np.maximum(0, x - correct_class_scores[:, np.newaxis] + 1.0)
  margins[np.arange(N), y] = 0
  loss = np.sum(margins) / N
  num_pos = np.sum(margins > 0, axis=1)
  dx = np.zeros_like(x)
  dx[margins > 0] = 1
  dx[np.arange(N), y] -= num_pos
  dx /= N
  return loss, dx


def softmax_loss(x, y):
  """
  Computes the loss and gradient for softmax classification.

  Inputs:
  - x: Input data, of shape (N, C) where x[i, j] is the score for the jth class
    for the ith input.
  - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
    0 <= y[i] < C

  Returns a tuple of:
  - loss: Scalar giving the loss
  - dx: Gradient of the loss with respect to x
  """
  probs = np.exp(x - np.max(x, axis=1, keepdims=True))
  probs /= np.sum(probs, axis=1, keepdims=True)
  N = x.shape[0]
  loss = -np.sum(np.log(probs[np.arange(N), y])) / N
  dx = probs.copy()
  dx[np.arange(N), y] -= 1
  dx /= N
  return loss, dx
