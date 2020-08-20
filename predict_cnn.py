# coding: utf-8

from __future__ import print_function

import os
import tensorflow as tf
import tensorflow.contrib.keras as kr
from numpy import unicode

from cnn_model import TCNNConfig, TextCNN
from data.cnews_loader import read_category, read_vocab

# try:
#     bool(type(unicode))
# except NameError:
#     unicode = str

base_dir = 'data/cnews'
vocab_dir = os.path.join(base_dir, 'cnews.vocab.txt')

save_dir = 'checkpoints/textcnn'
save_path = os.path.join(save_dir, 'best_validation')  # 最佳验证结果保存路径


class CnnModel:
    def __init__(self):
        self.config = TCNNConfig()
        self.categories, self.cat_to_id = read_category()
        self.words, self.word_to_id = read_vocab(vocab_dir)
        self.config.vocab_size = len(self.words)
        self.model = TextCNN(self.config)

        self.session = tf.Session()
        self.session.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
        saver.restore(sess=self.session, save_path=save_path)  # 读取保存的模型

    def predict(self, message):
        # 支持不论在python2还是python3下训练的模型都可以在2或者3的环境下运行
        content = unicode(message)
        data = [self.word_to_id[x] for x in content if x in self.word_to_id]
        # print(data)

        feed_dict = {
            self.model.input_x: kr.preprocessing.sequence.pad_sequences([data], self.config.seq_length),
            self.model.keep_prob: 1.0
        }

        y_pred_cls = self.session.run(self.model.y_pred_cls, feed_dict=feed_dict)
        return self.categories[y_pred_cls[0]]


if __name__ == '__main__':
    cnn_model = CnnModel()
    test_demo = ['speech takes on search enginesa scottish firm is looking to attract web surfers with a search engine that reads out results called speegle it has the look and feel of a normal search engine with the added feature of being able to read out the results scottish speech technology firm cec systems launched the site in november but experts have questioned whether talking search engines are of any real benefit to people with visual impairments the edinburgh based firm cec has married speech technology with ever popular internet search the ability to search is becoming increasingly crucial to surfers baffled by the huge amount of information available on the web according to search engine ask jeeves around of surfers visit search engines as their first port of call on the net people visiting speegle can select one of three voices to read the results of a query or summarise news stories from sources such as the bbc and reuters it is still a bit robotic and can make a few mistakes but we are never going to have completely natural sounding voices and it is not bad said speegle founder gordon renton the system is ideal for people with blurred vision or for those that just want to search for something in the background while they do something else we are not saying that it will be suitable for totally blind people although the royal national institute of the blind rnib is looking at the technology he added but julie howell digital policy manager at the rnib expressed doubts over whether speegle and similar sites added anything to blind people experience of the web there are a whole lot of options like this springing up on the web and one has to think carefully about what the market is going to be she said blind people have specialised screen readers available to them which will do the job these technologies do in a more sophisticated way she added the site uses a technology dubbed panavox which takes web text and converts it into synthesised speech in the past speech technology has only been compatible with broadband because of the huge files it downloads but cec says its compression technology means it will also work on slower dial up connections visitors to speegle may notice that the look and feel of the site bears more than a passing resemblance to the better known if silent search engine google google has no connection with speegle and the use of bright colours is simply to make the site more visible for those with visual impairments said mr renton it is not a rip off we are doing something that google does not do and is not planning to do and there is truth in the saying that imitation is the sincerest form of flattery he said speegle is proving popular with those learning english in countries such as japan and china the site is bombarded by people just listening to the words the repetition could be useful although they may all end up talking like robots said mr renton']
    for i in test_demo:
        print(cnn_model.predict(i))
