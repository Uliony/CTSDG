"""VGG16FeatureExtractor"""

from mindspore import load_checkpoint
from mindspore import load_param_into_net
from mindspore import nn


class VGG16FeatureExtractor(nn.Cell):
    """VGG16FeatureExtractor"""
    def __init__(self):
        super().__init__()
        self.enc_1 = nn.SequentialCell([
            nn.Conv2d(3, 64, 3, pad_mode='pad', padding=1, has_bias=True),
            nn.ReLU(),
            nn.Conv2d(64, 64, 3, pad_mode='pad', padding=1, has_bias=True),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        ])
        self.enc_2 = nn.SequentialCell([
            nn.Conv2d(64, 128, 3, pad_mode='pad', padding=1, has_bias=True),
            nn.ReLU(),
            nn.Conv2d(128, 128, 3, pad_mode='pad', padding=1, has_bias=True),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        ])
        self.enc_3 = nn.SequentialCell([
            nn.Conv2d(128, 256, 3, pad_mode='pad', padding=1, has_bias=True),
            nn.ReLU(),
            nn.Conv2d(256, 256, 3, pad_mode='pad', padding=1, has_bias=True),
            nn.ReLU(),
            nn.Conv2d(256, 256, 3, pad_mode='pad', padding=1, has_bias=True),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        ])

    def construct(self, x):
        """construct"""
        enc_1_output = self.enc_1(x)
        enc_2_output = self.enc_2(enc_1_output)
        enc_3_output = self.enc_3(enc_2_output)
        return enc_1_output, enc_2_output, enc_3_output


def get_feature_extractor(cfg):
    """get feature extractor"""
    vgg_feat_extractor = VGG16FeatureExtractor()
    if cfg.pretrained_vgg:
        load_param_into_net(vgg_feat_extractor,
                            load_checkpoint(cfg.pretrained_vgg))
    return vgg_feat_extractor