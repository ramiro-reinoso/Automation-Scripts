"""
This module imports BTICARD so the functions and globals can be used in Python Scripts
"""
import ctypes

try:
    BTI429ctype = ctypes.WinDLL ("C:\\Windows\\System32\\BTI429.dll")
except:
    BTI429ctype = ctypes.WinDLL ("C:\\Windows\\System32\\BTI42964.dll")
    
class MSGSTRUCT429(ctypes.Structure):
    _fields_=[
        ('addr', ctypes.c_ulong),       #User writes message configuration options
        ('data', ctypes.c_ulong),       #Card writes message flag 1
        ]

class PARAMFIELDS429(ctypes.Structure):
    _fields_=[
        ('highvolt', ctypes.c_int32),       #Absolute voltage of the first half of one-bit (in millivolts)
        ('lowvolt',  ctypes.c_int32),       #Absolute voltage of the second half of one-bit (in millivolts)
        ('nullvolt', ctypes.c_int32),       #Absolute voltage of the second half of one-bit (in millivolts)
        ('highrise', ctypes.c_int32),       #rise and fall time of the one-bit (in nanoseconds)
        ('lowrise',  ctypes.c_int32),       #Rise and fall time of the zero-bit (in nanoseconds)
        ('biasvolt', ctypes.c_int32),       #Common-mode bias of the entire signal (in millivolts)

        ]
        
"""
This is really a dictionary of bit masks but I feel it looks better with the decimal values in Python
"""
CHCFG429 = {
    'DEFAULT'        : 0,    #Select all default settings (XMT & RCV) (default)
    'HIGHSPEED'      : 1,                    #Select high speed (XMT & RCV)
    'AUTOSPEED'      : 2,                    #Select auto speed detection (RCV)
    'LOWSPEED'       : 0,                    #Select low speed (XMT & RCV) (default)
    'SELFTEST'       : 4,                    #Enable internal wraparound (XMT & RCV)
    'SELFTESTOFF'    : 0,                    #Disable internal wraparound (XMT & RCV) (default)
    'SYNC'           : 8,                    #Sync Enable (XMT & RCV)
    'SYNCOFF'        : 0,                    #Disable sync output (XMT & RCV) (default)
    'PARODD'         : 0,                    #Parity odd (XMT & RCV) (default)
    'PAREVEN'        : 16,                   #Parity even (XMT & RCV)
    'PARDATA'        : 32,                   #Parity bit as data (XMT & RCV)
    'ACTIVE '        : 0,                    #Enable channel activity (XMT & RCV) (default)
    'INACTIVE'       : 64,                   #Disable channel activity (XMT & RCV)
    'EXTTRIG'        : 128,                  #Enable external trigger for all messages (XMT)
    'EXTOFF '        : 0,                    #External trigger is enabled on message level (XMT) (default)
    'PARERR '        : 256,                  #Enable parity error for all messages (XMT)
    'NOERR  '        : 0,                    #Errors are enabled on message level (XMT) (default)
    'HIT    '        : 512,                  #Hit counter is enabled for all messages
    'NOHIT  '        : 0,                    #Hit counter is enabled on message level (default)
    'TIMETAG'        : 1024,                 #Enable time-tag for all message records
    'TIMETAGOFF'     : 0,                    #Time-tag is enabled on message level (default)
    'ELAPSE '        : 2048,                 #Enable elapse time for all messages
    'ELAPSEOFF'      : 0,                    #Elapse time is enabled on message level (default)
    'MAX    '        : 4096,                 #Enable max repetition rate monitoring for all messages
    'MIN    '        : 8192,                 #Enable min repetition rate monitoring for all messages
    'MAXMIN '        : 12288,                #Enable max and min repetition rate monitoring for all messages
    'MAXMINOFF'      : 0,                    #Repetition rate monitoring is enabled on message level (default)
    'SEQALL '        : 524288,               #Record entire channel in sequential record
    'SEQSEL '        : 0,                    #Sequential record recording is enabled at message level (default)
    'LOOPMAX'        : 1048576,              #Enable schedule maximum loop count
    'NOLOOPMAX'      : 0,                    #Disable schedule maximum loop count (default)
    'LOGHALT'        : 2097152,              #Enable event log on schedule halt
    'NOLOGHALT'      : 0,                    #No event log on schedule halt (default)
    'LOGPAUSE'       : 4194304,              #Enable event log on schedule pause
    'NOLOGPAUSE'     : 0,                    #No event log on schedule pause (default)
    'LOGERR '        : 8388608,              #Enable event log on decoder errors.
    'NOLOGERR'       : 0,                    #No event log on decoder errors (default)
    'PAUSE  '        : 16777216,             #Mark channel as paused
    'UNPAUSE'        : 0,                    #Mark channel as unpaused (default)
    'GAP1US'         : 16384,	             #Enable microsecond gaps
    'GAPBIT'         : 0,          	         #No microsecond gaps
    'PLAYBACK'       : 32768,                #Configure Tx Channel for Hardware Playback (FIFO mode)
    'SCHEDULE'       : 0                     #Configure Tx Channel to use Schedule (default)
}

MSGCRT429 = {
    'DEFAULT'        : 0,                    #Default settings
    'NOSEQ'          : 0,                    #Message will not be recorded in sequential record (default)
    'SEQ'            : 1,                    #Message will be recorded in sequential record
    'NOLOG'          : 0,                    #Message will not generate event log (default)
    'LOG'            : 2,                    #Message will generate event log
    'NOSKIP'         : 0,                    #Message will not be skipped (default)
    'SKIP'           : 8,                    #Message will be skipped
    'NOTIMETAG'      : 0,                    #Message will not record time-tag (default)
    'TIMETAG'        : 16,                   #Message will record time-tag
    'NOELAPSE'       : 0,                    #Message will not record elapse time (default)
    'ELAPSE'         : 32,                   #Message will record elapse time
    'NOMAXMIN'       : 0,                    #Message will not record min/max time (default)
    'MAX'            : 64,                   #Message will record max time
    'MIN'            : 128,                  #Message will record min time
    'MAXMIN'         : 192,                  #Message will record min/max time
    'NOSYNC'         : 0,                    #No sync will be generated for message (default)
    'SYNC'           : 256,                  #Sync will be generated for message
    'NOERR'          : 0,                    #No error will be generated for message (default)
    'PARERR'         : 512,                  #Parity error will be generated for message
    'NOHIT'          : 0,                    #Message will not record hit count (default)
    'HIT'            : 1024,                 #Message will record hit count
    'NOEXTRIG'       : 0,                    #Message will not be externally triggered (default)
    'EXTRIG'         : 4096,                 #Message will be externally triggered
    'WIPE'           : 0,                    #Enables message clear (default)
    'NOWIPE'         : 2147483648,           #Disables message clear
    'WIPE0'          : 0,                    #Initialize data with zeros (default)
    'WIPE1'          : 1073741824            #Initialize data with ones
}

LISTCRT429 = {
    'DEFAULT'        : ctypes.c_int32(0),    #Default settings
	'FIFO'           : 0,                    #Enable FIFO mode (default)
	'PINGPONG'       : 1,                    #Enable ping-pong mode
	'CIRCULAR'       : 2,                    #Enable circular mode
	'RCV'            : 16,                   #User will read from list buffer
	'XMT'            : 32,                   #User will write to list buffer
	'ASYNC'          : 64,                   #Asynchronous mode
	'NOLOG'          : 0,                    #Do not generate event log when list buffer empty/full (default)
	'LOG'            : 256                   #Generate event log when list buffer empty/full
}

PARAMCFG429 = {
    'DEFAULT'        : ctypes.c_int32(0),    #Select all default settings (default)
	'AMPLON'         : 0,                    #Enables parametric amplitude control (default)
	'AMPLOFF'        : 1,                    #Disables parametric amplitude control
	'BITRATEON '     : 0,                    #Enables parametric bit rate control (default)
	'BITRATEOFF'     : 2,                    #Disables parametric bit rate control
	'WAVEON'         : 0,                    #Enables parametric waveform control (default)
	'WAVEOFF'        : 4,                    #Disables parametric waveform control
	'LINKOFF'        : 0,                    #Each channel operates independently (default)
	'LINK'           : 8,                    #This channel's output is linked to another channel
	'CMBIASOFF'      : 0,                    #Disables common-mode DC bias (default)
	'CMBIAS'         : 16                    #Enables common-mode DC bias
}     
 
COND429 = {
	'ALWAYS'         : 0,                    #Unconditional
	'DIO1ACT'        : 1,                    #Condition on digital I/O #1 active
	'DIO1NACT'       : 2,                    #Condition on digital I/O #1 not active
	'DIO2ACT'        : 4,                    #Condition on digital I/O #2 active
	'DIO2NACT'       : 8,                    #Condition on digital I/O #2 not active
	'DIO3ACT'        : 16,                   #Condition on digital I/O #3 active
	'DIO3NACT'       : 32,                   #Condition on digital I/O #3 not active
	'DIO4ACT'        : 64,                   #Condition on digital I/O #4 active
	'DIO4NACT'       : 128,                  #Condition on digital I/O #4 not active
	'DIO5ACT'        : 256,                  #Condition on digital I/O #5 active
	'DIO5NACT'       : 512,                  #Condition on digital I/O #5 not active
	'DIO6ACT'        : 1024,                 #Condition on digital I/O #6 active
	'DIO6NACT'       : 2048,                 #Condition on digital I/O #6 not active
	'DIO7ACT'        : 4096,                 #Condition on digital I/O #7 active
	'DIO7NACT'       : 8192,                 #Condition on digital I/O #7 not active
	'DIO8ACT'        : 16384,                #Condition on digital I/O #8 active
	'DIO8NACT'       : 32768                 #Condition on digital I/O #8 not active
}

MSGACT429 = {	
	'CHMASK'         : 65280,                #Channel number mask value
	'CHSHIFT'        : 8,                    #Channel number shift value
	'SPD'            : 128,                  #Bus speed
	'ERR'            : 64,                   #Error bit
	'GAP'            : 32,                   #Gap error bit
	'PAR'            : 16,                   #Parity error bit
	'LONG'           : 8,                    #Long word error bit
	'BIT'            : 4,                    #Bit time error bit
	'TO'             : 2,                    #Time out error bit
	'HIT'            : 1                     #Always set
}

INFO429 = {	
	'PARAM'          : 1,                  #Channel supports parametric control
	'PWAVE'          : 2,                  #Channel supports parametric waveform (DAC)
	'CMBIAS'         : 3,                  #Channel supports common-mode DC bias
	'OUTSTATE'       : 4,                  #Channel supports Leg lifting/shorting
	'PLAYBACK'       : 5,                  #Channel supports hardware playback mode
	'PBITCOUNT'      : 6,                  #Channel supports parametric bitcounts
	'SCHDATA'        : 7,                  #Channel supports SchedData
	'GAP1US'         : 8                   #Channel supports microsecond gaps
}

SCHEDMODE = {
	'DEFAULT'        : 0,                  #Select all default settings
	'METHOD_NORMAL'  : 0,                  #Choose the normal scheduling method
	'METHOD_QUICK'   : 1,                  #Choose the quick scheduling method
	'METHOD_BOTH'    : 2,                  #Use all methods: use the quick method first, if fail, then use the normal method, finally use the Legacy method
	'METHOD_LEGACY'  : 4,                  #Use all methods: use the Legacy l43 method first, if fail, then quick method, if fail, then use the normal method
	'METHOD_MASK'    : 15,                 #Mask for method setting
	'MILLISEC'       : 0,                  #Specify periods in milliseconds
	'MICROSEC'       : 16,                 #Specify periods in microseconds
	'REMOTE'         : 0,                  #Perform calculations remotely, if applicable
	'LOCAL'          : 32,                 #Perform calculations locally, if applicable
	'SKIPRANGECHECK' : 0,                  #Skips range checking of a message when the min period equals the max period. Attempts to meet the rate, but schedule will succeed even if the messages with same min/max cannot transmit at a specified period
	'RANGECHECK'     : 64,                 #Performs range checking on all messages. SchedBuild fails if any messages are out of range.
	                                      #Deprecated options
	'DEFAULT_ALGOR'  : 0,                  #Choose the default algorithm
	'QUICK_ALGOR'    : 1,                  #Choose the quick algorithm
	'BOTH_ALGOR'     : 2,                  #Use all algorithms: Use the quick algorithm first, if fail, then use the normal algorithm, finally use the Legacy algorithm
	'ALGOR_MASK'     : 15                  #Mask for algorithm setting
}

OUTSTATE429 = {
	'NOCHANGE'       : 0,	               #Keep leg in its current state (default)
	'SIGNAL'         : 1,		           #Connect the leg to normal transmit signal
	'OPEN'           : 2,		           #Leave the leg open
	'GROUND'         : 4			       #Short the leg to ground
}


def BCDGetData(msg, msb,lsb):
    """
    BCDGetData function. 
    """
    data = BTI429ctype.BTI429_BCDGetData(msg,msb,lsb)
    return data

def BCDGetMant(msg,sigdig):
    """
    BCDGetMant function. 
    """
    data = BTI429ctype.BTI429_BCDGetMant(msg,sigdig)
    return data

def BCDGetSign(msg):
    """
    BCDGetSign function. 
    """
    data = BTI429ctype.BTI429_BCDGetSign(msg)
    return data

def BCDGetSSM(msg):
    """
    BCDGetSSM function. 
    """
    data = BTI429ctype.BTI429_BCDGetSSM(msg)
    return data

def BCDGetValue(msg, sigdig, resolstr):
    """
    BCDGetValue function. 
    """
    data = BTI429ctype.BTI429_BCDGetValue(msg,sigdig,resolstr)
    return data

def BCDPutData(msg, value, msb, lsb):
    """
    BCDPutData function. 
    """
    updatedMsg = BTI429ctype.BTI429_BCDPutData(msg, value, msb, lsb)
    return updatedMsg

def BCDPutMant(msg, value, sigdig, sign):
    """
    BCDPutMant function. 
    """
    updatedMsg = BTI429ctype.BTI429_BCDPutMant(msg, value, sigdig, sign)
    return updatedMsg

def BCDPutSign(msg, sign):
    """
    BCDPutSign function. 
    """
    updatedMsg = BTI429ctype.BTI429_BCDPutSign(msg, sign)
    return updatedMsg

def BCDPutSSM(msg, value):
    """
    BCDPutSSM function. 
    """
    updatedMsg = BTI429ctype.BTI429_BCDPutSSM(msg, value)
    return updatedMsg

def BCDPutValue(dblValue, msg, sigdig, dblResolution):
    """
    BCDPutValue function. 
    """
    updatedMsg = BTI429ctype.BTI429_BCDPutValue(dblValue, msg, sigdig, dblResolution)
    return updatedMsg

def BNRAngularGetValue(msg, sigbit, bPlusMinus180):
    """
    BNRAngularGetValue function. 
    """
    data = BTI429ctype.BTI429_BNRAngularGetValue(msg, sigbit, bPlusMinus180)
    return ctypes.c_double(data)

def BNRAngularPutValue(dblValue, msg, sigbit):
    """
    BNRAngularPutValue function. 
    """
    updatedMsg = BTI429ctype.BTI429_BNRAngularPutValue(dblValue,msg,sigbit)
    return ctypes.c_ulong(updatedMsg)

def BNRGetData(msg, msb, lsb):
    """
    BNRGetData function. 
    """
    data = BTI429ctype.BTI429_BNRGetData(ctypes.c_ulong(msg),ctypes.c_ushort(msb),ctypes.c_ushort(lsb))
    return ctypes.c_ulong(data)

def BNRGetMant(msg, sigbit):
    """
    BNRGetMant function. 
    """
    data = BTI429ctype.BTI429_BNRGetMant(ctypes.c_ulong(msg),ctypes.c_ushort(sigbit))
    return ctypes.c_ulong(data)

def BNRGetSign(msg):
    """
    BNRGetSign function. 
    """
    data = BTI429ctype.BTI429_BNRGetSign(ctypes.c_ulong(msg))
    return ctypes.c_ushort(data)

def BNRGetSSM(msg):
    """
    BNRGetSSM function. 
    """
    data = BTI429ctype.BTI429_BNRGetSSM(ctypes.c_ulong(msg))
    return ctypes.c_ushort(data)

def BNRGetValue(msg, sigbit, dblResolution):
    """
    BNRGetValue function. 
    """
    data = BTI429ctype.BTI429_BNRGetValue(ctypes.c_ulong(msg),ctypes.c_ushort(sigbit),ctypes.c_double(dblResolution))
    return ctypes.c_double(data)

def BNRPutData(msg, value, msb, lsb):
    """
    BNRPutData function. 
    """
    updatedMsg = BTI429ctype.BTI429_BNRPutData(ctypes.c_ulong(msg),ctypes.c_ulong(value),ctypes.c_ushort(msb),ctypes.c_ushort(lsb))
    return ctypes.c_ulong(updatedMsg)

def BNRPutMant(msg, value, sigbit, twos):
    """
    BNRPutMant function. 
    """
    updatedMsg = BTI429ctype.BTI429_BNRPutMant(ctypes.c_ulong(msg),ctypes.c_ulong(value),ctypes.c_ushort(sigbit),ctypes.c_ushort(twos))
    return ctypes.c_ulong(updatedMsg)

def BNRPutSign(msg, twos):
    """
    BNRPutSign function. 
    """
    updatedMsg = BTI429ctype.BTI429_BNRPutSign(ctypes.c_ulong(msg),ctypes.c_ushort(twos))
    return ctypes.c_ulong(updatedMsg)

def BNRPutSSM(msg, value):
    """
    BNRPutSSM function. 
    """
    updatedMsg = BTI429ctype.BTI429_BNRPutSSM(ctypes.c_ulong(msg),ctypes.c_ushort(value))
    return ctypes.c_ulong(updatedMsg)

def BNRPutValue(dblValue, msg, sigbit, dblResolution):
    """
    BNRPutValue function. 
    """
    updatedMsg = BTI429ctype.BTI429_BNRPutValue(ctypes.c_double(dblValue),ctypes.c_ulong(msg),ctypes.c_ushort(sigbit),ctypes.c_double(dblResolution))
    return ctypes.c_ulong(updatedMsg)

def ChClear(channum, hCore):
    """
    ChClear function. 
    """
    errval = BTI429ctype.BTI429_ChClear(ctypes.c_int32(channum),ctypes.c_int32(hCore))
    return ctypes.c_int32(errval).value

def ChConfig(configval, channum, hCore):
    """
    ChConfig function. 
    """
    errval = BTI429ctype.BTI429_ChConfig(ctypes.c_uint64(configval),ctypes.c_uint64(channum),ctypes.c_uint64(hCore))
    return ctypes.c_uint64(errval).value

def ChGetCount(rcvcount, xmtcount, hCore):
    """
    ChGetCount function. 
    """
    BTI429ctype.BTI429_ChGetCount(ctypes.POINTER(ctypes.c_int)(rcvcount),ctypes.POINTER(ctypes.c_int)(xmtcount),ctypes.c_int32(hCore))
    return 

def ChGetInfo(infotype, channum, hCore):
    """
    ChGetInfo function. 
    """
    chaninfo = BTI429ctype.BTI429_ChGetInfo(ctypes.c_ushort(infotype),ctypes.c_int32(channum),ctypes.c_int32(hCore))
    return ctypes.c_ulong(chaninfo)

def ChIs429(channum, hCore):
    """
    ChIs429 function. 
    """
    TrueFalse = BTI429ctype.BTI429_ChIs429(ctypes.c_int32(channum),ctypes.c_int32(hCore))
    """ return ctypes.c_bool(TrueFalse).value  """
    return ctypes.c_bool(TrueFalse)

def ChIsRcv(channum, hCore):
    """
    ChIsRcv function. 
    """
    TrueFalse = BTI429ctype.BTI429_ChIsRcv(ctypes.c_uint64(channum),ctypes.c_uint64(hCore))
    """ return ctypes.c_bool(TrueFalse).value  """
    return ctypes.c_bool(TrueFalse)

def ChIsXmt(channum, hCore):
    """
    ChIsXmt function. 
    """
    TrueFalse = BTI429ctype.BTI429_ChIsXmt(ctypes.c_int32(channum),ctypes.c_int32(hCore))
    """ return ctypes.c_bool(TrueFalse).value  """
    return ctypes.c_bool(TrueFalse)

def ChPause(channum, hCore):
    """
    ChPause function. 
    """
    BTI429ctype.BTI429_ChPause(ctypes.c_int32(channum),ctypes.c_int32(hCore))
    return 

def ChPauseCheck():
    """
    ChPauseCheck function. 
    """
    value = BTI429ctype.BTI429_ChPauseCheck()
    return ctypes.c_int32(value)

def ChResume(channum, hCore):
    """
    ChResume function. 
    """
    BTI429ctype.BTI429_ChResume(ctypes.c_int32(channum),ctypes.c_int32(hCore))
    return 

def ChStart(channum, hCore):
    """
    ChStart function. 
    """
    TrueFalse = BTI429ctype.BTI429_ChStart(ctypes.c_int32(channum),ctypes.c_int32(hCore))
    """ return ctypes.c_bool(TrueFalse).value  """
    return ctypes.c_bool(TrueFalse)

def ChStop(channum, hCore):
    """
    ChStop function. 
    """
    TrueFalse = BTI429ctype.BTI429_ChStop(ctypes.c_int32(channum),ctypes.c_int32(hCore))
    """ return ctypes.c_bool(TrueFalse).value  """
    return ctypes.c_bool(TrueFalse)

def ChSyncDefine(enableflag, syncmask, pinpolarity, channum, hCore):
    """
    ChSyncDefine function. 
    """
    errval = BTI429ctype.BTI429_ChSyncDefine(ctypes.c_bool(enableflag),ctypes.c_ushort(syncmask),ctypes.c_ushort(pinpolarity),ctypes.c_int32(channum),ctypes.c_int32(hCore))
    return ctypes.c_int32(errval).value

def ChTriggerDefine(enableflag, trigmask, trigval, pinpolarity, channum, hCore):
    """
    ChTriggerDefine function. 
    """
    errval = BTI429ctype.BTI429_ChTriggerDefine(ctypes.c_bool(enableflag),ctypes.c_ushort(trigmask),ctypes.c_ushort(trigval),ctypes.c_ushort(pinpolarity),ctypes.c_int32(channum),ctypes.c_int32(hCore))
    return ctypes.c_int32(errval).value

def DriverInfoStr():
    """
    DriverInfoStr function. 
    """
    strVal = BTI429ctype.BTI429_DriverInfoStr()
    return ctypes.POINTER(ctypes.c_buffer)(strVal).value

def FilterClear(baseaddr, hCore):
    """
    FilterClear function. 
    """
    errval = BTI429ctype.BTI429_FilterClear(ctypes.c_ulong(baseaddr), ctypes.c_int32(hCore))
    return ctypes.c_int32(errval).value

def FilterDefault(configval, channum, hCore):
    """
    FilterDefault function. 
    """
    addr = BTI429ctype.BTI429_FilterDefault(ctypes.c_uint64(configval),ctypes.c_uint64(channum),ctypes.c_uint64(hCore))

    """return ctypes.POINTER(MSGADDR)(addr)"""
#    return ctypes.cast(addr,ctypes.POINTER(ctypes.c_ulong))
    return addr

def FilterRd(labelval, sdival, channum, hCore):
    """
    FilterRd function. 
    """
    addr = BTI429ctype.BTI429_FilterRd(ctypes.c_int32(labelval),ctypes.c_int32(sdival),ctypes.c_int32(channum),ctypes.c_int32(hCore))
    """return ctypes.POINTER(MSGADDR)(addr)"""
    return ctypes.POINTER(ctypes.c_ulong)(addr)

def FilterSet(configval, labelval, sdimask, channum, hCore):
    """
    FilterRd function. 
    """
    addr = BTI429ctype.BTI429_FilterSet(ctypes.c_uint64(configval),ctypes.c_uint64(labelval),ctypes.c_uint64(sdimask),ctypes.c_uint64(channum),ctypes.c_uint64(hCore))
    """return ctypes.POINTER(MSGADDR)(addr)"""
    return addr

def FilterWr(msgaddr, labelval, sdival, channum, hCore):
    """
    FilterWr function. 
    """
    errval = BTI429ctype.BTI429_FilterWr(ctypes.c_ulong(msgaddr),ctypes.c_int32(labelval),ctypes.c_int32(sdival),ctypes.c_int32(channum),ctypes.c_int32(hCore))
    return ctypes.c_int32(errval).value

def FldGetData(msgval):
    """
    FldGetData function. 
    """
    data = BTI429ctype.BTI429_FldGetData(ctypes.c_ulong(msgval))
    return ctypes.c_ulong(data)

def FldGetLabel(msgval):
    """
    FldGetLabel function. 
    """
    label = BTI429ctype.BTI429_FldGetLabel(ctypes.c_ulong(msgval))
    return ctypes.c_ushort(label)

def FldGetParity(msgval):
    """
    FldGetParity function. 
    """
    parityVal = BTI429ctype.BTI429_FldGetParity(ctypes.c_ulong(msgval))
    return ctypes.c_ushort(parityVal)

def FldGetSDI(msgval):
    """
    FldGetSDI function. 
    """
    sdiVal = BTI429ctype.BTI429_FldGetSDI(ctypes.c_ulong(msgval))
    return ctypes.c_ushort(sdiVal)

def FldGetValue(msgval, startbit, endbit):
    """
    FldGetValue function. 
    """
    value = BTI429ctype.BTI429_FldGetValue(ctypes.c_ulong(msgval),ctypes.c_ushort(startbit),ctypes.c_ushort(endbit))
    return ctypes.c_ulong(value)

def FldPutData(msgval, data):
    """
    FldPutData function. 
    """
    updatedMsg = BTI429ctype.BTI429_FldPutData(ctypes.c_ulong(msgval),ctypes.c_ulong(data))
    return ctypes.c_ulong(updatedMsg)

def MsgDataRd(msgaddr,hCore):
    data = BTI429ctype.BTI429_MsgDataRd(ctypes.c_uint64(msgaddr),ctypes.c_uint64(hCore))
    return data

