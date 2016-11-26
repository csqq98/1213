#-*- encoding:utf-8 -*-
'''
Created on Nov 30, 2014
@author: letian
'''
import jieba.posseg as pseg
import codecs
import nltk

class WordSegmentation(object):
    ''' 分词 '''
    
    def __init__(self, stop_words_file=None):
        '''
        stop_words_file: 保存停止词的文件路径，每行一个停止次
        '''
        # 'CC', 'RB', 'IN', 'NN', 'JJ', 'VBZ', 'DT', 'EX', 'NNS', 'DT', 'IN', 'VBN','NNS', 'MD'//'NN', 'NNS', 'NNP', 'NNPS', 'PRP$'
        self.default_speech_tag_filter = ['NNS',  'NN', 'NNS', 'NNP', 'NNPS',
                                          'N', ]
        self.stop_tokens = "，。！？：；“”\"/\\`!#%^&*()_+-={}[]|;:'‘’<>?,.～·—「；：《》（）、― ―".decode('utf-8')
        self.stop_words = set()
        if type(stop_words_file) is str:
            for word in codecs.open(stop_words_file, 'r', 'utf-8', 'ignore'):
                self.stop_words.add(word.strip())
    
    def segment(self, text, lower=True, with_stop_words=True, speech_tag_filter=False):
        '''
        speech_tag_filter: 若为bool变量且为True，则使用默认的self.default_speech_tag_filter过滤，
                           若为list类型，则使用speech_tag_filter过滤
                           否则，不过滤
        with_stop_words:  若为True，则利用停止词集合来过滤（去掉停止词），否则什么都不做
        
        lower = True：     是否将单词小写（针对英文）
        '''
        jieba_result = nltk.sent_tokenize(text)
        a = []
        for sent in jieba_result:
            a.append(nltk.word_tokenize(sent))
        tags = []
        for tokens in a:
            tags.append(nltk.pos_tag(tokens))
        kong = tags[0]
        d = []
        if type(speech_tag_filter) == bool and speech_tag_filter == True:
            d = [w[0] for w in kong if w[1] in self.default_speech_tag_filter]
        elif type(speech_tag_filter) == list:
            d = [w[0] for w in kong if w[1] in speech_tag_filter]
        else:
            d = [w for w in d]
        res = d

        return res
        
    def segment_sentences(self, sentences, lower=True, with_stop_words=True, speech_tag_filter=False):
        '''

        '''
        
        res = []
        for sentence in sentences:
            res.append(self.segment(text=sentence, 
                                    lower=lower, 
                                    with_stop_words=with_stop_words, 
                                    speech_tag_filter=speech_tag_filter))
        return res
        
class SentenceSegmentation(object):
    ''' 分句 '''
    
    def __init__(self, delimiters='?!;？！。；…\n'):
        '''
        delimiters: 用来拆分句子
        '''
        self.delimiters = unicode(delimiters)

            
    def __split(self, text, delimiters):
        res = [unicode(text)]
        for sep in delimiters:
            text, res = res, []
            for seq in text:
                res += seq.split(sep)
        res = [s.strip() for s in res if len(s.strip()) > 0]
        return res 
    
    def segment(self, text):
        return self.__split(text, self.delimiters)
        
class Segmentation(object):
    
    def __init__(self, stop_words_file = None, delimiters='?!;？！。；…\n'):
        '''
        stop_words_file: 停止词文件
        delimiters: 用来拆分句子
        '''
        self.ws = WordSegmentation(stop_words_file)
        self.ss = SentenceSegmentation(delimiters)
        
    def segment(self, text, lower = False, speech_tag_filter = True):
        sentences = self.ss.segment(text)
        words_no_filter = self.ws.segment_sentences(sentences=sentences, 
                                                    lower = lower, 
                                                    with_stop_words = False,
                                                    speech_tag_filter = False)
        words_no_stop_words = self.ws.segment_sentences(sentences=sentences, 
                                                    lower = lower, 
                                                    with_stop_words = True,
                                                    speech_tag_filter = False)

        words_all_filters = self.ws.segment_sentences(sentences=sentences, 
                                                    lower = lower, 
                                                    with_stop_words = True,
                                                    speech_tag_filter = speech_tag_filter)

        return sentences, words_no_filter, words_no_stop_words, words_all_filters
    
        

# if __name__ == '__main__':
#
#     ss = SentenceSegmentation()
#     seg = Segmentation(stop_words_file='../stopword.data')
#     text = codecs.open('../text/01.txt', 'r', 'utf-8', 'ignore').read()
#     text = "视频里，我们的杰宝热情地用英文和全场观众打招呼并清唱了一段《Heal The World》。我们的世界充满了未知数。"
#     sentences, words_no_filter, words_no_stop_words, words_all_filters = seg.segment(text=text,
#                                                                                         lower=True,
#                                                                                         speech_tag_filter=True)
#     for s in sentences:
#         print s
#
#     print
#     for ss in words_no_filter:
#         print ' '.join(ss)
#
#     print
#     for ss in words_no_stop_words:
#         print '/'.join(ss)
#
#     print
#     for ss in words_all_filters:
#         print '%'.join(ss)
