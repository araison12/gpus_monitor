import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

EPOCHS_TO_TRAIN = 50000000000
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
if not torch.cuda.is_available():
    print(f'The current used device for this testing training is {device}. Please make sure that at least one Cuda device is used instead for this testing training.')
    assert False

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(2, 3, True)
        self.fc2 = nn.Linear(3, 1, True)

    def forward(self, x):
        x = F.sigmoid(self.fc1(x))
        x = self.fc2(x)
        return x


net = Net().to(device)
print(device)
inputs = list(
    map(
        lambda s: Variable(torch.Tensor([s]).to(device)),
        [[0, 0], [0, 1], [1, 0], [1, 1]],
    )
)
targets = list(
    map(lambda s: Variable(torch.Tensor([s]).to(device)), [[0], [1], [1], [0]])
)

criterion = nn.MSELoss()
optimizer = optim.SGD(net.parameters(), lr=0.01)

print("Training loop:")
for idx in range(0, EPOCHS_TO_TRAIN):
    for input, target in zip(inputs, targets):
        optimizer.zero_grad()  # zero the gradient buffers
        output = net(input)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()  # Does the update
    if idx % 5000 == 0:
        print(loss.item())
