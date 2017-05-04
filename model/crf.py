import pandas as pd
import numpy as np
import sys
import os
import re
import math
import unicodedata
import codecs
import pickle
import subprocess # For calling CRFSuite

class CRF_model(object):
    def __init__(self):
        print(">> Initialize CRF")
        # Initial directory and model name
        self.CRFSUITE = 'crfsuite'
        self.LIBCRFPATH = "/usr/local/lib"        
        self.model_file_name = './feature/model.crf'
        self.model_file_name_pkl = './feature/model.crf.pkl'
        
        # Initial miscellaneous specail characters and punctuation marks.
        self.punct = [u'!', u',', u'.', u':', u';', u'?']  # TO DO : Add "...".
        self.quotes = [u'"', u"'"]
        self.brackets = [u'(', u')', u'[', u']', u'{', u'}']
        self.mathsyms = [u'%', u'*', u'+', u'-', u'/', u'=', u'>', u'<']
    
    def _init(self):
        # Initial relevant
        self.sents_ = []
    
    def break_paragraph(self, paragraph):
        # Assume every dot is sentence
        # print(paragraph)
        paragraph = paragraph.capitalize()
        sentences = paragraph.split('.')
        sentences_ = []
        count = -1
        # print(sentences)
        for sentence in sentences:
            # print(sentence)
            if len(sentence) == 0: 
                continue
            
            if sentence != '' and sentence[0].islower() and sentence[0].isalpha():
                # print('Here')
                sentence = sentence.strip()
                # print(sentences_[count][0] + ' .' + sentence) 
                sentences_[count][0] = sentences_[count][0] + ' . ' + sentence
            else:
                # print('Here1')
                count += 1
                sentences_.append([sentence])
        
        for index in range(len(sentences_)):
            if type(sentences_[index][0]) is str:
                sentences_[index][0] = sentences_[index][0].strip()
        # print(sentences_)
        # print(">> Done breaking")
        return sentences_
    
    def cleaning(self, sents):
        for sent in sents:
            self.sent_ = []
            for word in sent:
                # First, check if acronym or abbreviation, i.e. Z., Y.Z., X.Y.Z. etc.
                if re.search('(.\.)+\Z', word) and word.isupper():
                    self.sent_.append(word) # Checked.
                    continue
                
                # Second, check if it is data.
                # DD.MM.YY.
                if re.search('\A[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{2}\.\Z', word):
                    self.sent_.append(word) # Checked.
                    continue

                # DD.MM.YYYY
                if re.search('\A[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{4}\.\Z', word):
                    self.sent_.append(word) # Checked.
                    continue
                
                # If not, separate out punctuation mark at end of word.
                for char in self.punct:
                    rm = re.search('\\' + char + '+\Z', word)
                    if rm:
                        word = re.sub('\\' + char + '+\Z', '', word) + ' ' + char
                        break
                self.sent_.extend(word.split())	
            
            self.sents_.append(self.sent_)

        # print(">> Done cleaning")
    
    def process(self):
        f = codecs.open('./tmp.1', mode = 'w', encoding = 'utf-8')
        # print(self.sents_)
        for line in self.sents_:
            for syl in line:
                f.write(syl + '\n')
            f.write('\n')
        f.close()
        
        # print("> Extracting model feature")
        f = open(self.model_file_name_pkl, 'rb')
        # SC for window
        sc = pickle.load(f) # Words with smoothed log probs
        pname = pickle.load(f)
        puncts = pickle.load(f)
        words_ = pickle.load(f)
        first_names = pickle.load(f)
        middle_names = pickle.load(f)
        last_names = pickle.load(f)
        location_names = pickle.load(f)
        f.close()
        
        # print(">> process features")
        fout = codecs.open('./tmp.1a', mode = 'w', encoding = 'utf-8')
        nSents = len(self.sents_)

        # print(self.sents_)
        for sentNo in range(0, nSents):

            syls = self.sents_[sentNo]
            nSyls = len(syls)

            syls_ = ['BOS2', 'BOS1']
            syls_.extend(syls)
            syls_.extend(['EOS1', 'EOS2'])

            # print(">> syls")
            # print(syls)

            # print(">> syls_")
            # print(syls_)

            # print(">> Processing")

            for sylNo in range(0, nSyls):
                sylNo_ = sylNo + 2 # Offset in syls_.
                text = 'c'
                attrib_no = 0 # Attribute index
                if 1:
                    for attrib in sc:
                        ngram = syls_[sylNo_ + attrib[0]]
                        for offset in attrib[1:]:
                            ngram = ngram + '_' + syls_[sylNo_ + offset]
                        
                        text = text + '\t' + 'f' + str(attrib_no) + '=' + ngram
                        attrib_no += 1
                
                if 1:
                    for attrib in sc:
                        ngram = syls_[sylNo_ + attrib[0]]
                        for offset in attrib[1:]:
                            ngram = ngram + '_' + syls_[sylNo_ + offset]
                        if ngram in words_:
                            text = text + '\t' + 'f' + str(attrib_no) + '=1'
                        else:
                            text = text + '\t' + 'f' + str(attrib_no) + '=0'
                        attrib_no += 1

                if 1:
                    # First name.
                    for offset in pname:
                        if syls_[sylNo_ + offset] in first_names:
                            text = text + '\t' + 'f' + str(attrib_no) + '=1'
                        else:
                            text = text + '\t' + 'f' + str(attrib_no) + '=0'
                        attrib_no += 1

                    # Middle name.
                    for offset in pname:
                        if syls_[sylNo_ + offset] in middle_names:
                            text = text + '\t' + 'f' + str(attrib_no) + '=1'
                        else:
                            text = text + '\t' + 'f' + str(attrib_no) + '=0'
                        attrib_no += 1

                    # Last name.
                    for offset in pname:
                        if syls_[sylNo_ + offset] in last_names:
                            text = text + '\t' + 'f' + str(attrib_no) + '=1'
                        else:
                            text = text + '\t' + 'f' + str(attrib_no) + '=0'
                        attrib_no += 1

                    # Location name.
                    for attrib in sc:
                        ngram = syls_[sylNo_ + attrib[0]]
                        for offset in attrib[1:]:
                            ngram = ngram + '_' + syls_[sylNo_ + offset]
                        if ngram in location_names:
                            text = text + '\t' + 'f' + str(attrib_no) + '=1'
                        else:
                            text = text + '\t' + 'f' + str(attrib_no) + '=0'
                        attrib_no += 1

                if 1:
                    
                    # Regular expressions:
                    # Numbers, percentages and money.
                    if re.search('[+-]?\d+([,.]\d+)*%*', syls_[sylNo_]):
                        text = text + '\t' + 'f' + str(attrib_no) + '=1'
                    else:
                        text = text + '\t' + 'f' + str(attrib_no) + '=0'
                    attrib_no += 1

                    # Short and long dates.
                    if re.search('\d+[/-:]\d+', syls_[sylNo_]) or re.search('\d+[/-:]\d+[/-:]\d+', syls_[sylNo_]):
                        text = text + '\t' + 'f' + str(attrib_no) + '=1'
                    else:
                        text = text + '\t' + 'f' + str(attrib_no) + '=0'
                    attrib_no += 1	
                
                    # Initial capital.
                    if syls_[sylNo_][0].isupper():
                        text = text + '\t' + 'f' + str(attrib_no) + '=1'
                    else:
                        text = text + '\t' + 'f' + str(attrib_no) + '=0'
                    attrib_no += 1

                    # All capitals.
                    if syls_[sylNo_].isupper():
                        text = text + '\t' + 'f' + str(attrib_no) + '=1'
                    else:
                        text = text + '\t' + 'f' + str(attrib_no) + '=0'
                    attrib_no += 1

                    # Punctuation and special characters.
                    if syls_[sylNo_] in puncts:
                        text = text + '\t' + 'f' + str(attrib_no) + '=1'
                    else:
                        text = text + '\t' + 'f' + str(attrib_no) + '=0'
                    attrib_no += 1
                
                fout.write(text + '\n')

            fout.write('\n')

        fout.close()

        # Tokenize using CRFSuite
        cmd = "export LD_LIBRARY_PATH=" + self.LIBCRFPATH
        cmd = cmd + "; " + self.CRFSUITE + " tag -m " + self.model_file_name + " tmp.1a > tmp.2"
        cmd = cmd + "; paste tmp.1 tmp.2 > tmp.3"
        cmd = cmd + "; rm tmp.1 tmp.2"
        status = subprocess.call(cmd, shell = True)	

        # print("Done training")

        # print(">> Printing process...")
        fin = codecs.open('./tmp.3', mode = 'r', encoding = 'utf-8', errors = 'ignore')
        sent = []
        word = ''
        write = 0 # To write sentence.

        token_list = []

        for line in fin:
            line = line.split()
            if len(line) == 0: # End of sentence. 
                if word != '':
                    sent.append(word) # Write current word.
                    word = '' # Flush word buffer.

                if write == 1:
                    # token_list.append(' '.join(sent))
                    token_list.extend(sent)
                    sent = [] # Flush sentence buffer.
                    write = 0
                continue

            write = 1
            # print(line)
            if len(line) == 1: 
                continue

            syl, tag = line            
            if tag == 'O':
                if word != '':
                    sent.append(word) # Write current word to sentence.
                    word = '' # Flush.
                sent.append(syl) # Add the current syl (not as token).
                continue

            if tag == 'B_W': # Begin word.
                if word != '':
                    sent.append(word) # Write current word.
                word = syl # Begin new word.
                continue

            if tag == 'I_W': # Inside word.
                word = word + ' ' + syl
            
        if word != '':
            sent.append(word)

        if write == 1:
            # token_list.append(' '.join(sent))
            token_list.extend(sent)
            sent = [] # Flush sentence buffer
            write = 0

        fin.close()

        status = subprocess.call('rm ./tmp.3 ./tmp.1a', shell = True)	        
        return token_list

    def train(self, posts):            
        count = -1
        token_list = pd.DataFrame([], columns = ['word', 'paragraphNo'])
        post = posts
        # for post in posts:
        #     self._init()

        #     count += 1
        #     print("processing " + str(count))
        #     sents = self.break_paragraph(post)

        #     # print(sents)
        #     self.cleaning(sents)

        #     tokenization = self.process()

        #     # Create list of paragraphNo
        #     paragraphNo = []
        #     for number in range(len(tokenization)):
        #         paragraphNo.append([count])

        #     # Transform array to numpy array
        #     tokenization = np.array(tokenization)
        #     paragraphNo = np.array(paragraphNo)
            
        #     # Transform the shape of tokenization
        #     nTokenization = len(tokenization)
        #     tokenization = tokenization.reshape(nTokenization, 1)
        #     # print(tokenization.shape)

        #     #Transform the shape of paragraphNo
        #     nParagraph = len(paragraphNo)
        #     paragraphNo = paragraphNo.reshape(nParagraph, 1)
        #     # print(paragraphNo.shape)

        #     mergeList = np.concatenate((tokenization, paragraphNo), axis = 1)
        #     # print(mergeList)

        #     temp = pd.DataFrame(mergeList, columns = ['word', 'paragraphNo'])
        #     token_list = token_list.append(temp, ignore_index = True)

        self._init()

        count += 1
        print("processing " + str(count))
        sents = self.break_paragraph(post)

        # print(sents)
        self.cleaning(sents)

        tokenization = self.process()

        # Create list of paragraphNo
        paragraphNo = []
        for number in range(len(tokenization)):
            paragraphNo.append([count])

        # Transform array to numpy array
        tokenization = np.array(tokenization)
        paragraphNo = np.array(paragraphNo)
        
        # Transform the shape of tokenization
        nTokenization = len(tokenization)
        tokenization = tokenization.reshape(nTokenization, 1)
        # print(tokenization.shape)

        #Transform the shape of paragraphNo
        nParagraph = len(paragraphNo)
        paragraphNo = paragraphNo.reshape(nParagraph, 1)
        # print(paragraphNo.shape)

        mergeList = np.concatenate((tokenization, paragraphNo), axis = 1)
        # print(mergeList)

        temp = pd.DataFrame(mergeList, columns = ['word', 'paragraphNo'])
        token_list = token_list.append(temp, ignore_index = True)

        return token_list

# if __name__ == '__main__':
#     CRF = CRF_model()
#     CRF.train(["Chủ nhân website muốn duy trì domain .com phải trả 6,42 USD ( tăng 7 % ) , còn .net sẽ tốn 3,85 USD ( tăng 10 % ) mỗi năm . Hãng điều hành tên miền VeriSign sẽ thu thêm 29 triệu USD/năm từ 62 triệu trang .com và 9,1 triệu trang .net . Sự thay đổi này sẽ bắt đầu vào ngày 15/10 năm nay và chỉ áp dụng với tên đăng ký mới hoặc gia hạn . Những tên miền đã đóng phí duy trì 10 năm hay 100 năm vẫn theo giá cũ . VeriSign cho biết nhu cầu đăng ký tên miền ngày càng tăng . Hiện , máy chủ DNS của họ nhận 30 tỷ yêu cầu mỗi ngày , gấp 30 lần so với năm 2000 . VeriSign phải khởi động dự án mang tên Titan để mở rộng dung lượng của hệ thống , đáp ứng được 4 nghìn tỷ thắc mắc/ngày vào năm 2010 . Tăng dung lượng máy chủ cũng là một biện pháp đối phó với nguy cơ tấn công từ chối dịch vụ . Nếu để xảy ra tình trạng này , toàn bộ các trang mà VeriSign quản lý sẽ `` chết đứng '' . \n T. H. ( theo AP ) T. H. Nhân"])
