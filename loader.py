import os
import json
import torch
from torch.utils.data import Dataset
from torchvision.io import read_image


class LogoDataset(Dataset):

    def __init__(self, info_file, scraper_dir, transform=None) -> None:
        self.info = self.get_info(info_file=info_file, scraper_dir=scraper_dir)
        self.scraper_dir = scraper_dir
        self.transform = transform
    

    def __len__(self) -> int:
        return len(self.info)
    
    
    def __getitem__(self, idx) -> torch.Tensor:
        info = self.info[idx]
        img_path = os.path.join(self.scraper_dir, info["images"][0]["path"])
        image = read_image(img_path)
        if self.transform:
            image = self.transform(image)
        return image
    

    def get_info(self, info_file, scraper_dir) -> list:
        
        file_path = os.path.join(scraper_dir, info_file)
        with open(file_path, "r") as f:
            json_info = f.read()
        
        info = json.loads(json_info)

        return info
    
