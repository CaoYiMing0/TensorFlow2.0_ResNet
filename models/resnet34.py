import tensorflow as tf
from models.residual_block import BasicBlock
from config import NUM_CLASSES


class ResNet34(tf.keras.layers.Layer):

    def __init__(self, num_classes=NUM_CLASSES):
        super(ResNet34, self).__init__()

        self.preprocess = tf.keras.Sequential([
            tf.keras.layers.Conv2D(filters=64,
                                   kernel_size=(7, 7),
                                   strides=2,
                                   padding='same'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Activation(tf.keras.activations.relu),
            tf.keras.layers.MaxPool2D(pool_size=(3, 3),
                                      strides=2)
        ])

        self.layer1 = self.build_res_block_1(filter_num=64,
                                      blocks=3)
        self.layer2 = self.build_res_block_1(filter_num=128,
                                      blocks=4,
                                      stride=2)
        self.layer3 = self.build_res_block_1(filter_num=256,
                                      blocks=6,
                                      stride=2)
        self.layer4 = self.build_res_block_1(filter_num=512,
                                      blocks=3,
                                      stride=2)

        self.avgpool = tf.keras.layers.GlobalAveragePooling2D()
        self.fc = tf.keras.layers.Dense(units=num_classes)

    def call(self, inputs, training=None):
        pre = self.preprocess(inputs)
        l1 = self.layer1(pre)
        l2 = self.layer1(l1)
        l3 = self.layer1(l2)
        l4 = self.layer1(l3)
        avgpool = self.avgpool(l4)
        out = self.fc(avgpool)

        return out

    def build_res_block_1(self, filter_num, blocks, stride=1):
        res_block = tf.keras.Sequential()
        res_block.add(BasicBlock(filter_num, stride))

        for _ in range(1, blocks):
            res_block.add(BasicBlock(filter_num, stride=1))

        return res_block