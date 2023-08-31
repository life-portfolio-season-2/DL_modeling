import torch
from tsai.all import ConvTranPlus, device


def predict(input_data, markets, thresh=0.5):
    C = 6
    O = 1
    period = 60

    model = ConvTranPlus(C,O,period,dim_ff=2048, fc_dropout=0.1, d_model=64).to(device)

    model.load_state_dict(torch.load('./ConvTranPlus_best.pt'))
    model.eval()

    x = torch.tensor(input_data, dtype=torch.float32, device=device)
    x = x.permute(0,2,1)

    with torch.no_grad():
        outputs = model(x).squeeze(1).sigmoid()

    pred = torch.where(outputs<thresh,0,1)
    pred = dict([(market, v.item()) for market, v in zip(markets, pred)])
    return pred