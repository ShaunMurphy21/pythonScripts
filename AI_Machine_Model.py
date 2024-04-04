import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from glob import glob
from PIL import Image
import time
from torch.utils.data import DataLoader, Dataset
import pyautogui
import os

valid_cases = glob(r'./backupTestCases/img/*_valid_*.png')
invalid_cases = glob(r'./backupTestCases/img/*_invalid_*.png')


class ImageDataset(Dataset):
    def __init__(self, image_paths, transform=None):
        self.image_paths = image_paths
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        img = datasets.folder.default_loader(img_path)  
        label = img_path.split("/")[-1].split("_")[1]  

        if label == "valid":
            label_num = 0
        elif label == "invalid":
            label_num = 1
        else:
            raise ValueError(f"Invalid label: {label}")
        
        if self.transform:
            img = self.transform(img)
        img_tensor = transforms.ToTensor()(img)  
        return img_tensor, torch.tensor(label_num)  



class SimpleClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        
        self.linear = nn.Linear(150 * 150 * 3, 2)  

    def forward(self, x):
        
        x = x.view(x.size(0), -1)  
        x = self.linear(x)
        return x

def train_model(model, dataset, dataloader, criterion, optimizer, num_epochs):
    """Trains the provided model on the given dataset."""

    for epoch in range(num_epochs):
        for inputs, labels in dataloader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            print(f"Epoch: {epoch+1}/{num_epochs}, Batch Loss: {loss.item():.4f}")


def predict_images(model, image_paths, transform):
    """Performs prediction on a list of image paths using the given model."""
    invalidList = []
    validList = []
    for path in image_paths:
        img = Image.open(path)
        img_tensor = transforms.ToTensor()(img).unsqueeze(0) 

        with torch.no_grad():
            outputs = model(img_tensor)

        prediction = torch.argmax(outputs, dim=1).item()
        predicted_class = ["valid", "invalid"][prediction]
        if predicted_class == 'invalid':
            print(path + ' : '+predicted_class)
        if predicted_class == 'valid':
            print(path + ' : '+predicted_class)
        
        
        
    print("Predictions complete")

valid_cases_dir = r'../img/testCases/*_valid_*.png'
invalid_cases_dir = r'../img/testCases/*_invalid_*.png'
prediction_cases_dir = r'../img/testCases/*.png'


transform = transforms.Compose([
transforms.Resize(150),
transforms.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1, hue=0.1),
transforms.RandomVerticalFlip(p=0.3),
transforms.RandomHorizontalFlip(p=0.2)  

])

choice = input('What would you like to do?\n1:Predict\n2:Train Model\n>>')

if choice == 'train':


    
    dataset = ImageDataset(glob(valid_cases_dir) + glob(invalid_cases_dir), transform=transform)
    dataloader = DataLoader(dataset, batch_size=16, shuffle=True)  

    
    model = SimpleClassifier()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)  
    
    train_model(model, dataset, dataloader, criterion, optimizer, num_epochs=20)  

    
    torch.save(model.state_dict(), "trained_model.pt")
elif choice == 'predict':
    
    predict_paths = glob(prediction_cases_dir)

    
    model = SimpleClassifier()
    model.load_state_dict(torch.load("trained_model.pt"))
    model.eval()

    
    predict_images(model, predict_paths, transform)


else:

    model = SimpleClassifier()
    model.load_state_dict(torch.load("trained_model.pt"))
    model.eval()
    pathName = r'../img/generalUse/{counter}predict.png'
    for i in range(0,1000):
        im = pyautogui.screenshot(region=(890,490, 150, 150))
        im.save(pathName.format(counter=i))
        predict_paths = glob(r'../img/generalUse/*.png')
        print(predict_paths)
        i = i + 1
        predict_images(model, predict_paths, transform)
        os.remove(pathName.format(counter=i-1))
        time.sleep(0.100)