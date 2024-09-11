import torch
import torch.nn as nn
import torchvision.transforms as transforms
import timm
from PIL import Image
import pytorch_lightning as pl
from torchmetrics.classification import Accuracy, F1Score, Precision, Recall
from torch.optim.lr_scheduler import ReduceLROnPlateau
import io

#Carga de modelo
class inception_v3(pl.LightningModule):
    def __init__(self, num_classes = 2, lr = 1e-3, pretrained=True):
        super().__init__()

        self.num_classes = num_classes
        self.lr = lr
        self.results = {"val_loss":[], "val_f1":[], "train_loss":[], "train_f1":[]}
        ########
        self.backbone = timm.create_model("inception_v3", pretrained = pretrained)
        if pretrained:
          # freeze  weights
            for param in self.backbone.parameters():
              param.requires_grad = False

        self.numfeat = self.backbone.get_classifier().in_features

        block = nn.Sequential(
            nn.Linear(self.numfeat, 1024),
            nn.Dropout(0.5),
            nn.Linear(1024, 512),
            nn.Dropout(0.5),
            nn.Linear(512, self.num_classes))

        self.backbone.fc = block
        ##########

        self.loss = nn.CrossEntropyLoss()

        # 4 Metrics
        self.train_f1 = F1Score(task="multiclass", num_classes=self.num_classes)
        self.valid_f1 = F1Score(task="multiclass", num_classes=self.num_classes)
        self.test_f1  = F1Score(task="multiclass", num_classes=self.num_classes)

    def forward(self, x):
      output = self.backbone(x)
      #print(output.logits)
      return output

    def training_step(self, batch, batch_idx):
        images, targets = batch
        outputs = self(images)
        loss = self.loss(outputs, targets)
        preds = torch.argmax(outputs, dim=1)

        self.train_f1(preds, targets)

        self.log('train_loss', loss)
        self.log('train_f1', self.train_f1)
        return loss

    def on_training_epoch_end(self):
        train_f1 =self.train_f1.compute()
        self.log('avg_train_f1',train_f1)
        self.results["train_f1"].append(train_f1)

        print(f"avg_train_f1: {train_f1}, ", end=" ")

    def validation_step(self, batch, batch_idx):
        images, targets = batch
        outputs = self(images)

        loss = self.loss(outputs, targets)

        preds = torch.argmax(outputs, dim=1)
        self.valid_f1(preds, targets)
        self.log('val_loss', loss)
        self.log('val_f1', self.valid_f1)

        return loss

    def on_validation_epoch_end(self):
        avg_val_f1 = self.valid_f1.compute()
        self.log('avg_val_f1',avg_val_f1)
        self.results["val_f1"].append(avg_val_f1)
        print(f"avg_val_f1: {avg_val_f1}")

    def test_step(self, batch, batch_idx):
        images, targets = batch
        outputs = self(images)

        loss = self.loss(outputs, targets)
        preds = torch.argmax(outputs, dim=1)

        self.test_f1(preds, targets)
        self.log('test_loss', loss)
        self.log('test_f1', self.test_f1)
        return loss

    def on_test_epoch_end(self):
        self.log('avg_test_f1', self.test_f1.compute())

    def configure_optimizers(self):
        #optimizer = torch.optim.Adam(self.parameters(), lr=(self.lr or self.learning_rate))
        #optimizer = torch.optim.SGD(self.parameters(), lr=self.lr, momentum=0.9)
        optimizer = torch.optim.Adam(self.parameters(), lr=self.lr)

        lr_scheduler = {
           "scheduler":ReduceLROnPlateau(optimizer, mode = "max", factor=0.1, patience=4,verbose=True),
           "monitor":"val_f1",
           "interval":"epoch"
        }

        return {"optimizer":optimizer, "lr_scheduler":lr_scheduler}

    def get_mean_std(self):
      return self.backbone.default_cfg["mean"], self.backbone.default_cfg["std"]

model = inception_v3(num_classes = 40, lr = 1e-3)
PATH = './inception_v3.pt'
model.load_state_dict(torch.load(PATH, map_location=torch.device('cpu')))
model.eval()    


#image -> tensor
    
def transform_image(image_bytes):
    transform = transforms.Compose([transforms.Resize(size = (224, 224)),
                                    transforms.CenterCrop(size = 224),
                                    transforms.ToTensor(),
                                    transforms.Normalize(model.get_mean_std()[0], model.get_mean_std()[1])])
    image = Image.open(io.BytesIO(image_bytes))
    image = transform(image)
    image = image.unsqueeze(0)
    return image

#predict



def get_prediction(image_tensor):
    images = image_tensor
    outputs = model(images)
    _,predicted = torch.max(outputs.data,1)
    return predicted


