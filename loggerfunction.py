# Logger file

# import the datetime library for logging date and time
import datetime

def logger(logmsg):
    print(str(datetime.datetime.now())+"\t"+logmsg)
    global logfile
    print(str(datetime.datetime.now())+"\t"+logmsg,file=logfile)


