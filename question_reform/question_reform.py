import crosslingual_coreference
from crosslingual_coreference import Predictor

import py_vncorenlp

from underthesea import ner
from underthesea import dependency_parse
from underthesea import word_tokenize
from underthesea import text_normalize

import pandas as pd

sw = pd.read_csv("stopwords.csv")

# choose minilm for speed/memory and info_xlm for accuracy
predictor = Predictor(
    language="en_core_web_sm", device=-1, model_name="minilm"
)
# en_core_web_sm
# xx_sent_ud_sm
## xx_ent_wiki_sm
def replace_ent(clusters, sentence):
  i=1
  #  newsen = sentence
  # recl = clusters[::-1]
  for cluster in clusters:
      print (f"Cluster {i}")
      for item in cluster[::-1]:
          start, end = item
          print(f'start: {start}, end: {end}')
          print(sentence[start:end])
          # newsen = sentence[:start]+cluster[0]+sentence[:end]
          # print(f'new sentence: {newsen}')
      print()
      i=i+1
    

def pre_proc(sent):
   for w in sw:
      sent.replace(w, "")
   print(sent)
   norm = text_normalize(sent)
  #  tok = word_tokenize(norm, format="text")
   return norm



def get_ent(sent):
   t = ['N', 'Np', 'Nc', 'Nb', 'Nu', 'Ny']
   ent = [e[0] for e in ner(sent) if e[1] in t]
   print(ent)
   return ent

### TEST WITH SENTENCE ###
def test():
    text = (
        "Do not forget about Momofuku Ando! He created instant noodles in Osaka. At"
        " that location, Nissin was founded. Many students survived by eating these"
        " noodles, but they don't even know him."
    )
    text0 = "Izuna đã phải chật vật không ngủ để — học ngôn ngữ Imanity, và em ấy cũng đã đọc được lượng sách nhiều đến thế này luôn."
    text1 = "Steph mỉm cười với cái cách hành xử gắng gượng quá sức của Izuna. Cô đã tìm thấy một chút xíu hi vọng mỏng như sợi chỉ giữa cái nhiệm vụ không hồi kết này. Steph tự vỗ vào má của cô để đánh thức chính mình."
    text2 = "Đó là chứng bệnh không rõ nguyên nhân, cũng chưa có cách chữa trị. Đầu tiên, tên người bệnh sẽ biến mất khỏi mọi giấy tờ, các thiết bị điện tử và trong mọi kí ức, kể cả trong trí nhớ của chính họ. Sau đó, khuôn mặt họ biến mất trong tranh vẽ và ảnh chụp."
    text3 = "Rồi họ mất màu, toàn thân chỉ còn hai sắc đơn như phim đen trắng."
    text4 = "Cô Hà đi chợ để làm gì? Cô ấy thấy gì ở đó? Cô ấy có thấy vịt ở đó không? Cô ấy có mua gì không? Cô ấy có mua nó không? chú Tâm có gặp cô ấy không?" 
    text5 = "Where is Mary's home? Is it beautiful?"


    com = text0 + '\n' + text1
    com2 = text2 + '\n' + text3
    
    # res0 = predictor.predict(text)["resolved_text"]
    # clusters0 = predictor.predict(text)["clusters"]
    # print(text + '\n')
    # print(res0)
    # print(ner(text))
    # print()
    # print(predictor.pipe([text])[0]["resolved_text"])
    
    recom = pre_proc(com)
    res1 = predictor.predict(recom)["resolved_text"]
    clusters1 = predictor.predict(recom)["clusters"]
    print(com + '\n')
    print(res1)
    print(ner(recom))
    # print(replace_ent(clusters1, com))
    # print(dependency_parse(com))
    print(get_ent(recom))
    print()
    # print(predictor.pipe([com])[0]["resolved_text"])



    recom2 = pre_proc(com2)
    res2 = predictor.predict(recom2)["resolved_text"]
    clusters2 = predictor.predict(recom2)["clusters"]
    print(com2 + '\n')
    print(res2)
    print(ner(recom2))
    # print(replace_ent(clusters2, com2))
    # print(dependency_parse(com2))
    print(get_ent(recom2))
    print()
    # print(predictor.pipe([com2])[0]["resolved_text"])
    

    retext4 = pre_proc(text4)
    res3 = predictor.predict(retext4)["resolved_text"]
    clusters3 = predictor.predict(retext4)["clusters"]
    print(text4 + '\n')
    print(res3)
    print(ner(retext4))
    # print(replace_ent(clusters3, text4))
    # print(dependency_parse(text4))
    print(get_ent(retext4))
    print()
    # print(predictor.pipe([text])[0]["resolved_text"])


    #EXAMINE CLUSTERS
    # i=1
    # for cluster in clusters:
    #     print (f"Cluster {i}")
    #     for item in cluster:
    #         start, end = item
    #         print(f'start: {start}, end: {end}')
    #         print(com2[start:end])
    #     print()
    #     i=i+1
    
### END TEST ###
    
    
def update(input, hist, q):
  # Q = 'Q:'
  # A = 'A:'
  # cont = Q+' '+input+'\n' if q else A+' '+input+'\n'
  cont = input + '\n'
  hist += cont
  ref_hist = predictor.predict(hist)["resolved_text"]
  return ref_hist

def test_input():
  user = "1"
  hist = ""
  brk = ['.', '?', '!']
  chat = []
  entity = []
  while True:
    user = input("> ")

    if user == "":
      break

    if user[-1] not in brk:
      user += '.'
    pre_proc(user)
    e = get_ent(user)
    temp = hist +' '+ user
    ref = predictor.predict(temp)["resolved_text"]
    chat.append(ref)
    for i in e:
      if i not in entity:
         entity.append(i)
         hist = temp

    print(f'hist: {chat}')
    print(f'reform hist: {hist}')
    # print(f'hist: {hist}')
    print(entity)
    print('\n\n')
    
    
if __name__ == "__main__":
    test_input()
    # test()
    
    
### EXAMPLE QUESTIONS ###
## BỘ 1 ##
# hist: Q:cô Hà hôm nay có đi chợ không
# Q:cô ấy có mua gì về cho bé An không?
# Q:bé có nhà không?
# Q:cô có mang gì về cho tôi không
# Q:bé ấy có nhà không?
# Q:bé An có được cô Hà mua cho thứ gì không?
# Q:bé có cảm ơn cô không?
# Q:bé ấy có vui không?

## BỘ 2 ##
# reform hist: Q: chợ Hà Đông ở đâu?
# Q: ở đó có gì?
# Q: đi như thế nào?
# Q: đi tới đó như thế nào?

# [chợ Hà Đông ở đâu? ở đó có gì? đi tới đó như thế nào?] --> coref
# [chợ Hà Đông ở đâu? ở chợ Hà Đông có gì? đi tới chợ Hà Đông như thế nào?]

### NOTE ###


### DONE ###
# giải quyết đc vấn đề inconsistent khi model liên tục reform trên cùng lịch sử
# giảm được tài nguyên tgian khi làm coref(khi có lsu chat dài)

### TODO ###
# làm cách nào để thêm đại từ vào các câu bị rút gọn đại từ
# làm cách nào để bắt được các từ khoá trong câu câu(có thể thử tf-idf)

### BÁO ĐANG ĐỌC ###
# https://tailieu.vn/doc/coreference-resolution-in-vietnamese-electronic-medical-records-2106822.html#:~:text=This%20paper%20tackles%20the%20problem%20of%20coreference%20resolution,verbs%20and%20other%20noun%20or%20adjective%20mentions%20possible.
# https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1194/reports/custom/15735157.pdf
# https://github.com/wjbmattingly/fewshot-text/blob/main/youtube-crosslingual.ipynb
