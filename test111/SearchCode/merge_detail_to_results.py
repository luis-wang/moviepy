#coding:utf8
'''
[新需求]:
之前的扫描结果是在changed.txt中只保存有哪些改变了的文件名称，
此模块的作用是一行行读取changed.txt,
然后把文件中详细改变了的位置重新写了一个新文件。
'''
import os,sys

def main():
    changed_log_file = r'D:\iislog\changed.txt'
    #changed_log_file = r'changed.txt'
    new_file = open(r'D:\iislog\changed_detail.txt','w')
    
    
    if not os.path.exists(changed_log_file):
        print u'要分析的文件%s不存在!!'%changed_log_file
        return
    
    filelog = open(changed_log_file,'r')
    lines = filelog.readlines()
    
    for line in lines:
        line = line.strip()
        if line:
            print u'正在分析:',line
            new_file.write('FileName:' + line + '\n') 
    
            #取得每一行中包含的文件名
            line_fname = line.split(',')[0]
            if not os.path.exists(line_fname):
                print u'不存在路径：',line_fname
                continue
            
            flines = open(line_fname, 'r').readlines()
            suggested_config_pos = 0
            
            for i,l in enumerate(flines):
                l = l.strip()
                
                if l:
                    if i>0 and suggested_config_pos == i:
                        print u'l3 = ', i,l
                        new_file.write('\t' + l + '\n\n') 
                    #找到修改的 ‘source config value is’
                    if 'source config value is' in l:
                        print u'l1 = ', i,l
                        new_file.write('\t' + l + '\n') 
                    if 'suggested config value is' in l:
                        print u'l2 = ',i,l
                        new_file.write('\t' + l + '\n') 
                        suggested_config_pos = i+1  #下一行就是建议的值
                    else:
                        suggested_config_pos = 0
    
    filelog.close()
    new_file.close()
            
          




if __name__ == '__main__':
    main()
    pass












