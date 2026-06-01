import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models, transforms
from PIL import Image

# ----------------------
# Device (M4 GPU via MPS)
# ----------------------
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
print("Using device:", device)

# ----------------------
# Image loading
# ----------------------
img_size = 512

loader = transforms.Compose([
    transforms.Resize((img_size, img_size)),
    transforms.ToTensor()
])

def load_image(path):
    image = Image.open(path).convert("RGB")
    image = loader(image).unsqueeze(0)
    return image.to(device)

content_img = load_image("content.jpg")
style_img = load_image("style.jpg")

# ----------------------
# VGG model
# ----------------------
vgg = models.vgg19(weights=models.VGG19_Weights.DEFAULT).features.to(device).eval()

# Freeze parameters
for param in vgg.parameters():
    param.requires_grad = False

# ----------------------
# Loss functions
# ----------------------
def gram_matrix(x):
    b, c, h, w = x.size()
    features = x.view(c, h * w)
    G = torch.mm(features, features.t())
    return G / (c * h * w)

content_layers = ['21']
style_layers = ['0', '5', '10', '19', '28']

def get_features(x, model):
    features = {}
    for name, layer in model._modules.items():
        x = layer(x)
        if name in content_layers:
            features['content'] = x
        if name in style_layers:
            if 'style' not in features:
                features['style'] = []
            features['style'].append(x)
    return features

# ----------------------
# Targets
# ----------------------
content_features = get_features(content_img, vgg)
style_features = get_features(style_img, vgg)

style_grams = [gram_matrix(f) for f in style_features['style']]

# ----------------------
# Input image (starts as content)
# ----------------------
input_img = content_img.clone().requires_grad_(True)

# ----------------------
# Optimization
# ----------------------
optimizer = optim.Adam([input_img], lr=0.03)

style_weight = 1e6
content_weight = 1

print("Starting optimization...")

for step in range(300):
    input_features = get_features(input_img, vgg)

    content_loss = torch.mean((input_features['content'] - content_features['content']) ** 2)

    style_loss = 0
    input_style_grams = [gram_matrix(f) for f in input_features['style']]

    for gm_in, gm_style in zip(input_style_grams, style_grams):
        style_loss += torch.mean((gm_in - gm_style) ** 2)

    total_loss = content_weight * content_loss + style_weight * style_loss

    optimizer.zero_grad()
    total_loss.backward()
    optimizer.step()

    if step % 50 == 0:
        print(f"Step {step}, Loss: {total_loss.item():.4f}")

# ----------------------
# Save output
# ----------------------
output = input_img.detach().cpu().squeeze()
output = transforms.ToPILImage()(output)
output.save("output.jpg")

print("Saved output.jpg")
