import torch
from torchvision.models import vgg19

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

model = vgg19(weights="DEFAULT").features.to(device).eval()

print("Loaded VGG19 on", device)
