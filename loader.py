import os
import json
import numpy as np
import torch
from torch.utils.data import Dataset
from torchvision.io import read_image
from torchvision import transforms
from torchvision.transforms.functional import resize
from torchvision.transforms.transforms import Grayscale

## MOVE IMAGE REJECTION AND PADDING TO SEPARATE FILE / DOCUMENT
## MOVE TRANSFORM DEFAULTS OUTSIDE OF CLASS AND TO WHERE YOU CALL IT


MAX_IMG_SZ = [300, 300]
NEW_IMG_SZ = [128, 128]

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
        if self.transform == "standard":
            padsz = self.pad_size(image)
            print(padsz)
            transformer = transforms.Compose([
                transforms.Pad(padding=padsz, fill=1),
                transforms.Grayscale(),
                transforms.Resize(size=NEW_IMG_SZ, antialias=True),
            ])
            self.transform = transformer
            image = self.transform(image)
        elif self.transform:
            image = self.transform(image)
        return image
    

    def pad_size(self, image) -> tuple:
        imsz = image.size()
        newsz = tuple(np.astype((MAX_IMG_SZ - np.array(imsz[1:])) / 2))
        return newsz


    def get_info(self, info_file, scraper_dir) -> list:
        
        file_path = os.path.join(scraper_dir, info_file)
        with open(file_path, "r") as f:
            json_info = f.read()
        
        info = json.loads(json_info)

        to_drop_black = [
            "JPMorgan Chase", "Sony", "BlackRock", "Volvo Group",
            "Panasonic", "Kering", "Ericsson", "Macquarie Group",
            "Norfolk Southern", "BASF", "Activision Blizzard", "Adidas",
            "Nissan Motor", "Advanced Micro Devices", "Renault", "BOE Technology Group",
            "Simon Property Group", "Assa Abloy", "Coal India", "T Rowe Price",
            "Marriott International", "L Brands", "Western Digital", "DaVita",
            "Autodesk", "Arrow Electronics", "Agilent Technologies", "Asustek Computer",
            "IDEXX Laboratories", "Zebra Technologies", "Bancolombia", "First Quantum Minerals",
            "Citrix Systems", "CrowdStrike", "DocuSign", "Palantir Technologies",
            "AECOM Technology", "CoStar Group", "JD Sports Fashion", "Marvell Technology Group",
            "Frost Bankers", "Nanto Bank", "Toll Brothers", "Unity Software"
        ]

        to_drop_building = [
            "China State Construction Engineering", "China Railway Construction", "Westinghouse Air Brake Technologies",
            "Nomura Research Institute", "Hotai Motor", "Taiwan Cement", "Chang Hwa Bank",
            "China Railway Signal & Communication", "DGB Financial Group"
        ]

        to_drop_larger300px = [
            'Etisalat', 'Sherwin-Williams', 'China Communications Construction', 'Hotai Motor', 'Delivery Hero'
        ]

        to_drop_all = to_drop_black
        to_drop_all.append(to_drop_building)
        to_drop_all.append(to_drop_larger300px)

        info_cleaned = [item for item in info if item['company_name'] not in to_drop_all]

        return info_cleaned
    
