import numpy as np


def distribute_value(dz, shape):
    """
    Distributes the input value in the matrix of dimension shape

    Arguments:
    dz -- input scalar
    shape -- the shape (n_H, n_W) of the output matrix for which we want to distribute the value of dz

    Returns:
    a -- Array of size (n_H, n_W) for which we distributed the value of dz
    """
    # Retrieve dimensions from shape (≈1 line)
    (n_H, n_W) = shape

    # Compute the value to distribute on the matrix (≈1 line)
    value = dz / (n_H * n_W)

    # Create a matrix where every entry is the "average" value (≈1 line)
    # a = None
    # YOUR CODE STARTS HERE

    a = np.full(shape, value)

    # YOUR CODE ENDS HERE
    return a


def create_mask_from_window(x):
    """
    Creates a mask from an input matrix x, to identify the max entry of x.

    Arguments:
    x -- Array of shape (f, f)

    Returns:
    mask -- Array of the same shape as window, contains a True at the position corresponding to the max entry of x.
    """
    # (≈1 line)
    # mask = None
    # YOUR CODE STARTS HERE

    mask = (np.max(x) == x)

    # YOUR CODE ENDS HERE
    return mask


def pool_forward(A_prev__, hparameters__, mode__="max"):
    """
    Implements the forward pass of the pooling layer

    Arguments:
    A_prev -- Input data, numpy array of shape (m, n_H_prev, n_W_prev, n_C_prev)
    hparameters -- python dictionary containing "f" and "stride"
    mode -- the pooling mode you would like to use, defined as a string ("max" or "average")

    Returns:
    A -- output of the pool layer, a numpy array of shape (m, n_H, n_W, n_C)
    cache -- cache used in the backward pass of the pooling layer, contains the input and hparameters
    """

    # Retrieve dimensions from the input shape
    (m__, n_H_prev__, n_W_prev__, n_C_prev__) = A_prev__.shape

    # Retrieve hyperparameters from "hparameters"
    f__ = hparameters__["f"]
    stride__ = hparameters__["stride"]

    # Define the dimensions of the output
    n_H__ = int(1 + (n_H_prev__ - f__) / stride__)
    n_W__ = int(1 + (n_W_prev__ - f__) / stride__)
    n_C__ = n_C_prev__

    # Initialize output matrix A
    A__ = np.zeros((m__, n_H__, n_W__, n_C__))

    # YOUR CODE STARTS HERE

    for i__ in range(m__):  # loop over the training examples

        for h__ in range(n_H__):  # loop on the vertical axis of the output volume

            # Find the vertical start and end of the current "slice" (≈2 lines)

            vert_start__ = h__ * stride__
            vert_end__ = vert_start__ + f__

            for w__ in range(n_W__):  # loop on the horizontal axis of the output volume

                # Find the vertical start and end of the current "slice" (≈2 lines)
                horiz_start__ = w__ * stride__
                horiz_end__ = horiz_start__ + f__

                for c__ in range(n_C__):  # loop over the channels of the output volume

                    # Use the corners to define the current slice on the ith training example of A_prev, channel c. (≈1 line)
                    a_prev_slice__ = A_prev__[i__, vert_start__:vert_end__, horiz_start__:horiz_end__, c__]

                    # Compute the pooling operation on the slice.
                    # Use an if statement to differentiate the modes.
                    # Use np.max and np.mean.
                    if mode__ == "max":

                        A__[i__, h__, w__, c__] = np.max(a_prev_slice__)

                    elif mode__ == "average":

                        A__[i__, h__, w__, c__] = np.mean(a_prev_slice__)

    # YOUR CODE ENDS HERE

    # Store the input and hparameters in "cache" for pool_backward()
    cache__ = (A_prev__, hparameters__)

    # Making sure your output shape is correct
    # assert(A__.shape == (m__, n_H__, n_W__, n_C__))

    return A__, cache__

def pool_backward(dA_, cache_, mode_="max"):

    # YOUR CODE STARTS HERE

    # Retrieve information from cache (≈1 line)
    (A_prev_, hparameters_) = cache_
    # print(f"A_prev_.shape = {A_prev_.shape};hparameters_ = {hparameters_}")

    # Retrieve hyperparameters from "hparameters" (≈2 lines)
    stride_ = hparameters_["stride"]
    f_ = hparameters_["f"]
    # print(f"stride_ = {stride_};f_ = {f_}")

    # Retrieve dimensions from A_prev's shape and dA's shape (≈2 lines)
    m_, n_H_prev_, n_W_prev_, n_C_prev_ = A_prev_.shape
    # print(f"m_ = {m_};n_H_prev_ = {n_H_prev_};n_H_prev_ = {n_H_prev_};n_C_prev_ = {n_C_prev_}")

    m_, n_H_, n_W_, n_C_ = dA_.shape

    # Initialize dA_prev with zeros (≈1 line)
    dA_prev_ = np.zeros(A_prev_.shape)

    for i_ in range(m_):  # loop over the training examples

        # select training example from A_prev (≈1 line)
        a_prev_ = A_prev_[i_]

        for h_ in range(n_H_):  # loop on the vertical axis

            for w_ in range(n_W_):  # loop on the horizontal axis

                for c_ in range(n_C_):  # loop over the channels (depth)

                    # Find the corners of the current "slice" (≈4 lines)
                    vert_start_ = h_ * stride_
                    vert_end_ = vert_start_ + f_

                    horiz_start_ = w_ * stride_
                    horiz_end_ = horiz_start_ + f_

                    # Compute the backward propagation in both modes.
                    if mode_ == "max":

                        # Use the corners and "c" to define the current slice from a_prev (≈1 line)
                        a_prev_slice_ = a_prev_[vert_start_:vert_end_, horiz_start_:horiz_end_, c_]

                        # Create the mask from a_prev_slice (≈1 line)
                        mask_ = create_mask_from_window(a_prev_slice_)

                        # Set dA_prev to be dA_prev + (the mask multiplied by the correct entry of dA) (≈1 line)
                        dA_prev_[i_, vert_start_:vert_end_, horiz_start_:horiz_end_, c_] += mask_ * dA_[i_, h_, w_, c_]
                        print(f"mask_ * dA_[i_, h_, w_, c_] =\n{mask_ * dA_[i_, h_, w_, c_]}"); return 0


                    elif mode_ == "average":

                        # Get the value da from dA (≈1 line)
                        da_ = dA[i_, h_, w_, c_]

                        # Define the shape of the filter as fxf (≈1 line)
                        shape_ = (f_, f_)

                        # Distribute it to get the correct slice of dA_prev. i.e. Add the distributed value of da. (≈1 line)
                        dA_prev_[i_, vert_start_:vert_end_, horiz_start_:horiz_end_, c_] += distribute_value(da_, shape_)

                    else:

                        pass

    # YOUR CODE ENDS HERE

    # Making sure your output shape is correct
    assert (dA_prev_.shape == A_prev_.shape)

    return dA_prev_

np.random.seed(1)
A_prev = np.random.randn(5, 5, 3, 2)
hparameters = {"stride" : 1, "f": 2}
A, cache = pool_forward(A_prev, hparameters)
print(A.shape)
print(cache[0].shape)
dA = np.random.randn(5, 4, 2, 2)

dA_prev1 = pool_backward(dA, cache, mode_ = "max")
print("mode = max")
print('mean of dA = ', np.mean(dA))
print('dA_prev1[1,1] = ', dA_prev1[1, 1])
print()
dA_prev2 = pool_backward(dA, cache, mode_= "average")
print("mode = average")
print('mean of dA = ', np.mean(dA))
print('dA_prev2[1,1] = ', dA_prev2[1, 1])

print(f"dA_prev2[1, 1] =\n{dA_prev2[1, 1]}\n")

assert type(dA_prev1) == np.ndarray, "Wrong type"
assert dA_prev1.shape == (5, 5, 3, 2), f"Wrong shape {dA_prev1.shape} != (5, 5, 3, 2)"
assert np.allclose(dA_prev1[1, 1], [[0, 0],
                                    [ 5.05844394, -1.68282702],
                                    [ 0, 0]]), "Wrong values for mode max"
assert np.allclose(dA_prev2[1, 1], [[0.08485462,  0.2787552],
                                    [1.26461098, -0.25749373],
                                    [1.17975636, -0.53624893]]), "Wrong values for mode average"
print("\033[92m All tests passed.")