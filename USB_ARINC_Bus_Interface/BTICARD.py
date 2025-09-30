"""
This module imports BTICARD so the functions and globals can be used in Python Scripts
"""
import ctypes

try:
    BTICardctype = ctypes.WinDLL ("C:\\Windows\\System32\\BTICARD.dll")
except:
    BTICardctype = ctypes.WinDLL ("C:\\Windows\\System32\\BTICARD64.dll")

INFOTYPE = {
    'PLAT'      : 1,               #Returns the platform type
    'PROD'      : 2,               #Returns the product type
    'GEN'       : 3,               #Returns the generation number
    '1553COUNT' : 4,               #Returns the 1553 channel count
    '1553SIZE'  : 5,               #Returns the 1553 channel size
    '429COUNT'  : 6,               #Returns the 429 channel count
    '429SIZE'   : 7,               #Returns the 429 channel size
    '717COUNT'  : 8,               #Returns the 717 channel count
    '717SIZE'   : 9,               #Returns the 717 channel size
    '708COUNT'  : 10,              #Returns the 708 channel count
    '708SIZE'   : 11,              #Returns the 708 channel size
    'VERSION'   : 12,              #Returns the version number
    'DATE'      : 13,              #Returns the version date
    'CHINFO'    : 14,              #Returns the channel info
    '422COUNT'  : 15,              #Returns the 422 port count
    '422SIZE'   : 16,              #Returns the 422 port size
    'CSDBCOUNT' : 17,              #Returns the CSDB channel count
    'CSDBSIZE'  : 18,              #Returns the CSDB channel size
    'DIOCOUNT'  : 19,              #Returns the DIO bank count
    'DIOSIZE'   : 20,              #Returns the DIO bank size
    'HWGEN'     : 21,              #Returns the Hardware Generation
    'EBRCOUNT'  : 22,              #Returns the EBR channel count
    'EBRSIZE'   : 23,              #Returns the EBR channel size
    'CARDTYPE'  : 24,              #Returns the card type
    'SERIALNUM' : 25,              #Returns the serial number
    'VERSIONEX' : 26               #Returns the version number including minor-minor
}

def CardOpen(CARDNUM):
    """
    Basic Card Open function. Uses BTICARD_CardOpen to find the Card and returns errval and
    handle on success or errval on failure.
    """
    handle = ctypes.c_uint64()
    errval = BTICardctype.BTICard_CardOpen(ctypes.POINTER(ctypes.c_uint64)(handle),ctypes.c_ushort(CARDNUM))
    if (errval != 0):
        return ctypes.c_int32(errval).value, 0
    else:
        return errval, handle.value
        
def CoreOpen(hCard, corenum):
    """
    Basic Core Open function. Uses BTICARD_CoreOpen to find the Core and returns errval and
    handle on success or errval on failure.
    """
    hCore = ctypes.c_uint64()
    errval = BTICardctype.BTICard_CoreOpen( ctypes.POINTER(ctypes.c_uint64)(hCore),
    ctypes.c_int32(corenum),
    ctypes.c_uint64(hCard))
    if (ctypes.c_int32(errval).value!=0):
        return errval, 0
    else:
        return errval, hCore.value

def CardReset(hCard):
    """
    Basic Card Reset function. Uses BTICard_CardReset to run an opened Card and returns errval.
    The return is a negative value if an error occurs or zero if successful.
    """
    errval = BTICardctype.BTICard_CardReset(ctypes.c_uint64(hCard))
    return ctypes.c_int32(errval).value

def CardStart(hCard):
    """
    Basic Card Start function. Uses BTICard_CardStart to run an opened Card and returns errval.
    The return is a negative value if an error occurs or zero if successful.
    """
    errval = BTICardctype.BTICard_CardStart(ctypes.c_uint64(hCard))
    return ctypes.c_int32(errval).value
    
def CardStop(hCard):
    """
    Basic Card Stop function. Uses BTICard_CardStop to close the running Card and returns errval.
    The return is a negative value if an error occurs or zero if successful.
    """
    errval = BTICardctype.BTICard_CardStop(ctypes.c_uint64(hCard))
    return ctypes.c_int32(errval).value
    
def CardClose(hCard):
    """
    Basic Card Close function. Uses BTICard_CardClose to close the open Card and returns errval.
    The return is a negative value if an error occurs or zero if successful.
    """
    errval = BTICardctype.BTICard_CardClose(ctypes.c_uint64(hCard))
    return ctypes.c_int32(errval).value
    
def ErrDescStr(errval, hCard):
    """
    Basic Card Close function. Uses BTICard_CardClose to close the open Card and returns errval.
    The return is a negative value if an error occurs or zero if successful.
    """
    description = BTICardctype.BTICard_ErrDescStr(ctypes.c_int32(errval),ctypes.c_uint64(hCard))
    return ctypes.c_char_p(description).value
    
def CardTypeStr(hCard):
    """
    Card Type String function. Uses BTICard_CardClose to close the open Card and returns errval.
    The return is a negative value if an error occurs or zero if successful.
    """
    description = ctypes.c_char_p()
    description = BTICardctype.BTICard_CardTypeStr(ctypes.c_uint64(hCard))
    return ctypes.c_char_p(description).value
        
def CardProductStr(hCard):
    """
    Card Product String function. this calls BTICard_CardProductStr with a core handle.
    The return is a pointer to a character string describing the Device specified by hCore.
    """
    description = ctypes.c_char_p()
    description = BTICardctype.BTICard_CardProductStr(ctypes.c_uint64(hCard))
    return ctypes.c_char_p(description).value
        
def CardGetInfo(infotype, channel, hCard):
    """
    Card Product String function. this calls BTICard_CardGetInfo with a bitmask (infotype), a channel number and a core handle.
    The return is the information specified by infotype.
    """
    results = BTICardctype.BTICard_CardGetInfo(ctypes.c_int32(infotype),ctypes.c_int32(channel),ctypes.c_uint64(hCard))
    return ctypes.c_ulong(results).value
