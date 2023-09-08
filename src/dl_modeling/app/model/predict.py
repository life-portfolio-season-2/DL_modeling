import torch
from torch.utils.data import DataLoader
from tsai.all import ConvTranPlus, device


def predict(input_data, pks):
    C = 7
    O = 1
    period = 1

    model = ConvTranPlus(C,O,period).to(device)

    # model.load_state_dict(torch.load('./ConvTranPlus_best.pt'))
    model.eval()

    x = torch.tensor(input_data, dtype=torch.float32, device=device)
    x = x.permute(0,2,1)

    dataloader = DataLoader(x, batch_size=128)

    outputs = []
    with torch.no_grad():
        for data in dataloader:
            output = model(data).squeeze(1).sigmoid()
            outputs.append(output)

    outputs = torch.concat(outputs, dim=0)
    pred = dict([(market, v.item()) for market, v in zip(pks, outputs)])
    return pred