import os,sys
import shutil

# getCode('corp')
def getCode(project):
    corp=['CorpFlight','CorpHotel','CorpMobile','CorpStatistics','CorpUser','ResStatic','WebResource','CorpProcess','CorpTrain']
    NewBusiness=['AffiliateMarketing','EnglishSite','EnglishSite','EnglishSite','LvPing','Songguo','wingon']
    Flight=['Booking','BookingIntl','IntlAggregator','IntlProduct','Order','Product','Switch','Ticket','ResStatic']
    Hotel=['Arch','Booking','Group','HtlCasino','HtlInv','Order','Package','Product','ResStatic','Service','TS','Supplier','Vendor']
    Platform=['Balance','CRM','CTI','Delivery','Finance','Insurance','Marketing','Payment','Settlement','ResStatic','InfoSecurity','SPS']
    Vacations=['Arch','Booking','Lib','Order','Package','Product','ResStatic','Vendor','Car','Cruise','Interest','Mice','Outie','Support','Thingstodo','Tour','Visa']
    HHTravelSolutions=['HHTravel']
    TaoCan=['API','Booking','Common','Order','Product','ResStatic']

    projects = {'corp':corp,
                'NewBusiness':NewBusiness,
                'Flight':Flight,
                'Hotel':Hotel,
                'Platform':Platform,
                'Vacations':Vacations,
                'HHTravelSolutions':HHTravelSolutions,
                'TaoCan':TaoCan
    }
    localworkspace='D:\CtripCode'
    username='cn1\scmer'
    password='12345_qwert'
    for group in projects[project]:
        try:
            c1='cd /d '+localworkspace+'\\'+project+'\\'+group
            c2='tf get /V:T /overwrite /force /recursive /login:'+username+','+password+' $/'+group+'/MainLine'
            command = c1+'&'+c2
            print 'command = ',command
            os.system(command)
        except Exception,e:
            print 'Error: %s'%str(e)
            print 'program will exit!'
            sys.exit(1)

if __name__ == '__main__':
    getCode('corp')
    getCode('NewBusiness')
    getCode('Flight')
    getCode('Hotel')
    getCode('Platform')
    getCode('Vacations')
    getCode('HHTravelSolutions')
    getCode('TaoCan')
    
    
    
    