import torch
import torch.nn as nn
import torch.nn.functional as F


class Conv3DDetector(torch.nn.Module):
    
    def __init__(self):
        super(Conv3DDetector, self).__init__()
        # 1st 3D Conv layer
        self.conv3D_1 = nn.Conv3d(in_channels=3, out_channels=64, kernel_size=3, stride=1, padding=1)
        self.bn3D_1 = nn.BatchNorm3d(64)
        self.maxpool3D_1 = nn.MaxPool3d(kernel_size=(1, 2, 2), stride=(1, 2, 2))
        
        # 2nd 3D Conv layer
        self.conv3D_2 = nn.Conv3d(in_channels=64, out_channels=128, kernel_size=3, stride=1, padding=1)
        self.bn3D_2 = nn.BatchNorm3d(128)
        self.maxpool3D_2 = nn.MaxPool3d(kernel_size=2, stride=2)
        
        # 3rd 3D Conv layer
        self.conv3D_3a = nn.Conv3d(in_channels=128, out_channels=256, kernel_size=3, stride=1, padding=1)
        self.bn3D_3a = nn.BatchNorm3d(256)
        self.conv3D_3b = nn.Conv3d(in_channels=256, out_channels=256, kernel_size=3, stride=1, padding=1)
        self.bn3D_3b = nn.BatchNorm3d(256)
        self.maxpool3D_3 = nn.MaxPool3d(kernel_size=(1, 2, 2), stride=(1, 2, 2))
        
        # 4th 3D Conv layer
        self.conv3D_4a = nn.Conv3d(in_channels=256, out_channels=256, kernel_size=3, stride=1, padding=1)
        self.bn3D_4a = nn.BatchNorm3d(256)
        self.conv3D_4b = nn.Conv3d(in_channels=256, out_channels=256, kernel_size=3, stride=1, padding=1)
        self.bn3D_4b = nn.BatchNorm3d(256)
        self.maxpool3D_4 = nn.MaxPool3d(kernel_size=2, stride=2)
        
        # 5th 3D Conv layer
        self.conv3D_5a = nn.Conv3d(in_channels=256, out_channels=512, kernel_size=3, stride=1, padding=1)
        self.bn3D_5a = nn.BatchNorm3d(512)
        self.conv3D_5b = nn.Conv3d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=1)
        self.bn3D_5b = nn.BatchNorm3d(512)
        self.maxpool3D_5 = nn.MaxPool3d(kernel_size=(1, 2, 2), stride=(1, 2, 2))
        
        # Fully Connected layer
        self.output = nn.Linear(in_features=16384, out_features=1)
        self.output_act = nn.Sigmoid()
        
    def forward(self, x):
        out = F.relu(self.bn3D_1(self.conv3D_1(x)))
        out = self.maxpool3D_1(out)
        
        out = F.relu(self.bn3D_2(self.conv3D_2(out)))
        out = self.maxpool3D_2(out)
        
        out = F.relu(self.bn3D_3a(self.conv3D_3a(out)))
        out = F.relu(self.bn3D_3b(self.conv3D_3b(out)))
        out = self.maxpool3D_3(out)
        
        out = F.relu(self.bn3D_4a(self.conv3D_4a(out)))
        out = F.relu(self.bn3D_4b(self.conv3D_4b(out)))
        out = self.maxpool3D_4(out)
        
        out = F.relu(self.bn3D_5a(self.conv3D_5a(out)))
        out = F.relu(self.bn3D_5b(self.conv3D_5b(out)))
        out = self.maxpool3D_5(out)
        
        out = torch.flatten(out, start_dim=1)
        
        out = self.output(out)
        #out = nn.Softmax(dim=1)(out)
        out = self.output_act(out)
        
        return out