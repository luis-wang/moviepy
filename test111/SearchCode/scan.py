#coding:utf8
"""
扫描代码
"""

from lxml import etree
import logging
import os
import fnmatch
import traceback
import sys
import shutil
import time
count = 0


def search(dir,ospec,nspec):
    """ 'D:\\','CtripCode','Result' """
    
    configs=['ConfigProfile.xml']
    if os.path.exists(dir+nspec):
        os.system('rd /s /q '+dir+nspec)
        
    for dirpath,dirnames,filenames in os.walk(dir+ospec,topdown=True):
        for filename in filenames:
            if filename in configs:
                src=os.path.join(dirpath,filename)
                dst=src.replace(ospec,nspec)
                ndir=os.path.dirname(dst)
                if os.path.exists(ndir):
                    shutil.copy(src,dst)
                else:
                    os.system('mkdir '+'"'+ndir+'"')
                    shutil.copy(src,dst)
    os.system('cd /d '+ndir+'&&attrib -R /S +A D:\\Result\\*')

def add_xml_comment_element(kid):
    "替换文本"
    pre = etree.Comment(text="source config value is " + etree.tostring(kid).strip())
    pre.tail = "\n"
    kid.addprevious(pre)
    pre1 = etree.Comment(text="suggested config value is:")
    pre1.tail = "\n"
    kid.addprevious(pre1)


def replace_text_and_add_comment_of_element(kid, asmx):
    global count
    add_xml_comment_element(kid)
    kid.text = asmx
    count = count + 1


def replace_fat_fws_lpt_section_hard_url_in_configprofile(element, envtype, replaced_env="{$g.EnvType}"):
    global count
    sh_env = ["dev", "test", "testx", "testy", 
              "testp", "testu", "testl", "uat", "fat"]
    
    nt_env = ["fat" + str(i) for i in xrange(51) ] + ["lpt" + str(i) for i in xrange(11) ]
    all_env = [i + ".sh.ctriptravel.com" for i in sh_env] + [i+ ".qa.nt.ctripcorp.com" for i in sh_env + nt_env] + ["fws.sh.ctriptravel.com", "lpt.sh.ctriptravel.com"]
    for kid in element.iterchildren(reversed=True):
        if kid.text is not None and kid.tag is not etree.Comment:
            for i in ('uploadimg.{$g.EnvType}.sh.ctriptravel.com','uploadimg.{$g.EnvType}.qa.nt.ctripcorp.com','uploadimg.{$g.EnvType}.ctrip.com','uploadimg.qa.nt.ctripcorp.com'):
                if kid.text.find(i)>0 and (envtype == 'fat' or envtype == 'fws'):
                    replace_text_and_add_comment_of_element(kid, kid.text.replace(i, "uploadimg.fws.qa.nt.ctripcorp.com"))
                if kid.text.find(i)>0 and (envtype == 'lpt'):
                    replace_text_and_add_comment_of_element(kid, kid.text.replace(i, "uploadimg.lpt.qa.nt.ctripcorp.com"))
            for i in all_env:
                if kid.text.lower().find((i + "/SOA.ESB/Ctrip.SOA.ESB.asmx").lower()) > 0 or kid.text.lower().find("{$g.EnvType}.qa.nt.ctripcorp.com/SOA.ESB/Ctrip.SOA.ESB.asmx".lower()) > 0:
                    if envtype == 'fat' or envtype == 'fws':
                        replace_text_and_add_comment_of_element(kid, "http://soa.fws.qa.nt.ctripcorp.com/SOA.ESB/Ctrip.SOA.ESB.asmx")
                    else:
                        replace_text_and_add_comment_of_element(kid, "http://soa.lpt.qa.nt.ctripcorp.com/SOA.ESB/Ctrip.SOA.ESB.asmx")
                if kid.text.lower().find('uploadimg.' + i) > 0 and (envtype == 'fat' or envtype == 'fws'):
                    replace_text_and_add_comment_of_element(kid, kid.text.replace(i, "fws.qa.nt.ctripcorp.com"))
                if kid.text.lower().find('uploadimg.' + i) > 0 and (envtype == 'lpt'):
                    replace_text_and_add_comment_of_element(kid, kid.text.replace(i, "lpt.qa.nt.ctripcorp.com"))
                if kid.text.lower().find(i) > 0:
                    replace_text_and_add_comment_of_element(kid, kid.text.replace(i, "%s.qa.nt.ctripcorp.com" % replaced_env))
            if etree.tostring(kid).lower().strip().find("LoggingServer.V2.IP".lower()) > 0 and kid.text.lower().find("collector.logging.fws.qa.nt.ctripcorp.com") < 0:
                replace_text_and_add_comment_of_element(kid, "collector.logging.fws.qa.nt.ctripcorp.com")
            if kid.text.lower().find(".qa.nt.ctripcorp.com") > 0 and kid.text.lower().find("{$g.EnvType}.qa.nt.ctripcorp.com".lower()) < 0 and \
                            kid.text.lower().find("fws.qa.nt.ctripcorp.com") < 0 and kid.text.lower().find("lpt.qa.nt.ctripcorp.com") < 0:
                replace_text_and_add_comment_of_element(kid, kid.text.replace("qa.nt.ctripcorp.com",  "%s.qa.nt.ctripcorp.com" % replaced_env))


def replace_configprofile_nt_hard_url(file, released_env="{$g.EnvType}"):
    global count
    #envs = ["fat","fws","lpt"]
    envs = ["lpt",]
    doc = []
    try:
        doc = etree.parse(file)
    except:
        logger.error(file + " parse error")
        return

    # logger.info()
    for env in envs:
        profile_environments_add_target = doc.xpath("/profile/environments/add[@target='" + env + "']")
        
        if len(profile_environments_add_target) > 0:
            if 'nt' not in profile_environments_add_target[0].attrib['dataCenter']:
                profile_environments_add_target[0].attrib['dataCenter'] = 'sh,nt'
            target = profile_environments_add_target[0].attrib['name']
            if len(doc.xpath("/profile/"+target)) > 0:
                element = doc.xpath("/profile/" + target)[0]
                replace_fat_fws_lpt_section_hard_url_in_configprofile(element, env, released_env)
        else:
            logger.error(file + " doesn't have " + env + " item.")
            # print ("no target")
    if count > 0:
        logger.info(file + " , changed " + str(count) + " times.")
        outFile = open(file, 'w')
        doc.write(outFile, encoding='utf-8')

def replace_all_configprofiles(dir, topdown=True):
    global count
    for root,dirs,files in os.walk(dir, topdown):
        for name in files:
            count = 0
            try:
                replace_configprofile_nt_hard_url(os.path.join(root,name))
            except Exception as e:
                raise Exception(os.path.join(root,name) + e.message)


def extract_info_and_error_records_from_source_file(source_file, targe_file, search_words):
    global f, line, lines, w
    with open(source_file, 'r') as f:
        lines = [line.replace(search_words, "") for line in f if line.find(search_words) >= 0]
        
        
    with open(targe_file, 'w') as w:
        w.writelines(lines)

def remove_file(path):
    if os.path.exists(path):
        os.remove(path)

def replace_hard_url_of_appsetting_config(file, envtype='fat', released_env='fat50'):
    global count
    try:
        doc = etree.parse(file)
    except:
        logger.error(file+" parse error")
        return
    if len(doc.xpath("/appSettings")) > 0:
        element = doc.xpath("/appSettings")[0]
        sh_env = ["dev", "test", "testx", "testy", "testp", "testu", "testl", "uat", "fat"]
        nt_env = ["fat" + str(i) for i in xrange(51) ] + ["lpt" + str(i) for i in xrange(11) ]
        all_env = [i + ".sh.ctriptravel.com" for i in sh_env] + [i+ ".qa.nt.ctripcorp.com" for i in sh_env + nt_env] + ["fws.sh.ctriptravel.com", "lpt.sh.ctriptravel.com"]
        if  released_env + ".qa.nt.ctripcorp.com" in all_env:
            all_env.remove(released_env + ".qa.nt.ctripcorp.com")
        for kid in element.iterchildren(reversed=True):
            if kid.tag is not etree.Comment and kid.attrib['value'] is not None:
                for i in all_env:
                    if kid.attrib['value'].lower().find((i + "/SOA.ESB/Ctrip.SOA.ESB.asmx").lower()) > 0 or kid.attrib['value'].lower().find("{$g.EnvType}.qa.nt.ctripcorp.com/SOA.ESB/Ctrip.SOA.ESB.asmx".lower()) > 0:
                        if envtype == 'fat' or envtype == 'fws':
                            add_xml_comment_element(kid)
                            kid.attrib['value'] = "http://soa.fws.qa.nt.ctripcorp.com/SOA.ESB/Ctrip.SOA.ESB.asmx"
                            count = count + 1
                        else:
                            add_xml_comment_element(kid)
                            kid.attrib['value'] = "http://soa.lpt.qa.nt.ctripcorp.com/SOA.ESB/Ctrip.SOA.ESB.asmx"
                            count = count + 1
                    if kid.attrib['value'].lower().find(i) > 0:
                        add_xml_comment_element(kid)
                        kid.attrib['value'] = kid.attrib['value'].replace(i, "%s.qa.nt.ctripcorp.com" % released_env)
                        count = count + 1
                if etree.tostring(kid).lower().strip().find("LoggingServer.V2.IP".lower()) > 0 and kid.attrib['value'].lower().find("collector.logging.fws.qa.nt.ctripcorp.com") < 0:
                    add_xml_comment_element(kid)
                    kid.attrib['value'] = "collector.logging.fws.qa.nt.ctripcorp.com"
                    count = count + 1
                if kid.attrib['value'].lower().find(".qa.nt.ctripcorp.com") > 0 and kid.attrib['value'].lower().find(released_env + ".qa.nt.ctripcorp.com") < 0 and \
                                kid.attrib['value'].lower().find("{$g.EnvType}.qa.nt.ctripcorp.com".lower()) < 0 and \
                                kid.attrib['value'].lower().find("fws.qa.nt.ctripcorp.com") < 0 and kid.attrib['value'].lower().find("lpt.qa.nt.ctripcorp.com") < 0:
                    add_xml_comment_element(kid)
                    kid.attrib['value'] = kid.attrib['value'].replace("qa.nt.ctripcorp.com",  "%s.qa.nt.ctripcorp.com" % released_env)
                    count = count + 1

    if count > 0:
        logger.info(file + " , changed " + str(count) + " times.")
        outFile = open(file,'w')
        doc.write(outFile,encoding='utf-8')

def replace_hard_url_in_all_files_match_pattern(pattern, rootPath):
    for root, dirs, files in os.walk(rootPath):
        for filename in fnmatch.filter(files, pattern):
             replace_hard_url_of_appsetting_config(os.path.join(root, filename))

def format_exception(e):
    exception_list = traceback.format_stack()
    exception_list = exception_list[:-2]
    exception_list.extend(traceback.format_tb(sys.exc_info()[2]))
    exception_list.extend(traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))

    exception_str = "Traceback (most recent call last):\n"
    exception_str += "".join(exception_list)
    # Removing the last \n
    exception_str = exception_str[:-1]

    return exception_str

def deal_txt():
    file=open(r'D:\iislog\error-fat.txt')
    newfile=open(r'D:\result\error-fat.log','w')
    for line in file:
        newfile.write(line.strip().split('ConfigProfile.xml')[0]+'ConfigProfile.xml'+'\n')
    file.close()
    newfile.close()

    file=open(r'D:\iislog\error-lpt.txt')
    newfile=open(r'D:\result\error-lpt.log','w')
    for line in file:
        newfile.write(line.strip().split('ConfigProfile.xml')[0]+'ConfigProfile.xml'+'\n')
    file.close()
    newfile.close()

    file=open(r'D:\iislog\error-fws.txt')
    newfile=open(r'D:\result\error-fws.log','w')
    for line in file:
        newfile.write(line.strip().split('ConfigProfile.xml')[0]+'ConfigProfile.xml'+'\n')
    file.close()
    newfile.close()

    file=open(r'D:\iislog\changed.txt')
    newfile=open(r'D:\result\changed.log','w')
    for line in file:
        newfile.write(line.strip().split('ConfigProfile.xml')[0]+'ConfigProfile.xml'+'\n')
    file.close()
    newfile.close()

def Analy_log():
    changed=open(r'D:\iislog\changed.txt')
    error=open(r'D:\iislog\error.txt')
    report=open(r'D:\result\report.txt','w+')
    last_d=time.strftime('%Y%m%d',time.localtime(time.time()))
    report.write('Date:'+last_d+'\n')
    report.write('FileName:ConfigProfile.xml'+'\n')
    corp=flight=hotel=NewBusiness=vacations=platform=HHTravelSolutions=0
    for line in error:
        if line.strip().split('\\')[2]=='Corp':
            corp=corp+1
        if line.strip().split('\\')[2]=='Flight':
            flight=flight+1
        if line.strip().split('\\')[2]=='Hotel':
            hotel=hotel+1
        if line.strip().split('\\')[2]=='NewBusiness':
            NewBusiness=NewBusiness+1
        if line.strip().split('\\')[2]=='Vacations':
            vacations=vacations+1
        if line.strip().split('\\')[2]=='Platform':
            platform=platform+1
        if line.strip().split('\\')[2]=='HHTravelSolutions':
            HHTravelSolutions=HHTravelSolutions+1
    report.write('Crash:'+'corp:'+str(corp)+' flight:'+str(flight)+' hotel:'+str(hotel)+' NewBusiness:'+ str(NewBusiness)+
           ' vacations:'+str(vacations)+' platform:'+str(platform)+' HHTravelSolutions:'+str(HHTravelSolutions)+'\n')

    for line in changed:
        if line.strip().split('\\')[2]=='corp':
            corp=corp+1
        if line.strip().split('\\')[2]=='Flight':
            flight=flight+1
        if line.strip().split('\\')[2]=='Hotel':
            hotel=hotel+1
        if line.strip().split('\\')[2]=='NewBusiness':
            NewBusiness=NewBusiness+1
        if line.strip().split('\\')[2]=='Vacations':
            vacations=vacations+1
        if line.strip().split('\\')[2]=='Platform':
            platform=platform+1
        if line.strip().split('\\')[2]=='HHTravelSolutions':
            HHTravelSolutions=HHTravelSolutions+1
    report.write('Error:'+'corp:'+str(corp)+' flight:'+str(flight)+' hotel:'+str(hotel)+' NewBusiness:'+ str(NewBusiness)+
                 ' vacations:'+str(vacations)+' platform:'+str(platform)+' HHTravelSolutions:'+str(HHTravelSolutions)+'\n')
    changed.close()
    error.close()
    report.close()	
	
    os.system('7z a D:\\iislog\\result.7z D:\\Result')
	
def DivideLog():
    fat=open(r'D:\iislog\error-fat.txt','w')
    lpt=open(r'D:\iislog\error-lpt.txt','w')
    fws=open(r'D:\iislog\error-fws.txt','w')
    for line in open(r'D:\iislog\error.txt'):
        if line.strip().find('fat')>0:
            fat.write(line)
        if line.strip().find('lpt')>0:
            lpt.write(line)
        if line.strip().find('fws')>0:
            fws.write(line)
    fat.close()
    lpt.close()
    fws.close()
	
if __name__ == '__main__':
    search('D:\\','CtripCode','Result')
    try:
        log_path = r'D:/iislog/log.log'
        remove_file(log_path)
        logger=logging.getLogger()
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler('D:/iislog/log.log')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        replace_all_configprofiles(r'D:\Result')
    except Exception as e:
        print "Printing only the traceback above the current stack frame"
        print "".join(traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))
        print
        print "Printing the full traceback as if we had not caught it here..."
        print format_exception(e)
    remove_file(r'D:\iislog\changed.txt')
    
    #只是分离出info 和 error的值 
    extract_info_and_error_records_from_source_file(log_path, r'D:\iislog\changed.txt', 'INFO - ')
    remove_file(r'D:\iislog\error.txt')
    extract_info_and_error_records_from_source_file(log_path, r'D:\iislog\error.txt', 'ERROR - ')
    remove_file(r'D:\iislog\result.7z')
    DivideLog()
    deal_txt()
    Analy_log()
