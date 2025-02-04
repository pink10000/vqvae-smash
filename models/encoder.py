
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from models.residual import ResidualStack


class Encoder(nn.Module):
    """
    This is the q_theta (z|x) network. Given a data sample x q_theta 
    maps to the latent space x -> z.

    For a VQ VAE, q_theta outputs parameters of a categorical distribution.

    Inputs:
    - in_dim : the input dimension
    - h_dim : the hidden layer dimension
    - res_h_dim : the hidden dimension of the residual block
    - n_res_layers : number of layers to stack

    """

    def __init__(self, in_dim, h_dim, n_res_layers, res_h_dim):
        super(Encoder, self).__init__()
        kernel = (2, 4)
        stride = (1, 1)
        self.conv_stack = nn.Sequential(
            nn.Conv2d(in_dim, h_dim // 2, 
                      kernel_size=kernel,
                      stride=stride, 
                      padding=1),
            nn.ReLU(),
            nn.Conv2d(h_dim // 2, h_dim, 
                      kernel_size=kernel,
                      stride=stride, 
                      padding=1),
            nn.ReLU(),
            nn.Conv2d(h_dim, h_dim, 
                      kernel_size=(kernel[0] - 1, kernel[1] - 1),
                      stride=stride, 
                      padding=1),
            ResidualStack(
                h_dim, h_dim, res_h_dim, n_res_layers)

        )

    def forward(self, x):
        return self.conv_stack(x)


if __name__ == "__main__":
    # random data
    x = np.random.random_sample((200, 1, 2, 200)) # TODO
    # print(x.shape)
    x = torch.tensor(x).float()

    # test encoder
    encoder = Encoder(1, 128, 3, 64)
    encoder_out = encoder(x)
    print('Encoder out shape:', encoder_out.shape)
