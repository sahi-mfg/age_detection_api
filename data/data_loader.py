import os
import torch
from glob import glob
from PIL import Image
from torch.utils.data import random_split, Dataset, DataLoader
from torchvision import transforms as T

torch.manual_seed(2023)


class CustomDataset(Dataset):
    def __init__(self, root, data, threshold=0.35, transformations=None):
        self.transformations, self.data, self.threshold = transformations, data, threshold
        self.im_paths = [im_path for im_path in sorted(glob(f"{root}/{data}/*/*")) if "jpg" in im_path]

        self.cls_names, self.cls_counts, count = {}, {}, 0
        for idx, im_path in enumerate(self.im_paths):
            class_name = self.get_class(im_path)
            if class_name not in self.cls_names:
                self.cls_names[class_name] = count
                self.cls_counts[class_name] = 1
                count += 1
            else:
                self.cls_counts[class_name] += 1

    def get_class(self, path):
        return os.path.dirname(path).split("/")[-1]

    def __len__(self):
        return len(self.im_paths)

    def __getitem__(self, idx):
        im_path = self.im_paths[idx]
        im = Image.open(im_path)
        gt = self.cls_names[self.get_class(im_path)]

        if self.transformations is not None:
            im = self.transformations(im)
        rand = torch.rand(1)
        if rand > self.threshold:
            if self.data == "train":
                im = T.functional.rotate(img=im, angle=90)
        elif rand > self.threshold and rand < 2 * self.threshold:
            if self.data == "train":
                im = T.functional.rotate(img=im, angle=-90)

        return im, gt


def get_dataloaders(root, train_tfs, test_tfs, bs, data, split=[0.9, 0.1], ns=4):
    ds = CustomDataset(root=root, data="train", transformations=train_tfs)
    test_ds = CustomDataset(root=root, data="test", transformations=test_tfs)

    all_len = len(ds)
    train_len = int(all_len * split[0])
    train_ds, val_ds = random_split(dataset=ds, lengths=[train_len, all_len - train_len])

    train_dataloader, val_dataloader, test_dataloader = (
        DataLoader(train_ds, batch_size=bs, shuffle=True, num_workers=ns),
        DataLoader(val_ds, batch_size=bs, shuffle=False, num_workers=ns),
        DataLoader(test_ds, batch_size=1, shuffle=False, num_workers=ns),
    )

    return train_dataloader, val_dataloader, test_dataloader, ds.cls_names
