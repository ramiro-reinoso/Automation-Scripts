
"""
    BTI1553 DRIVER EXAMPLE 1  (05/23/2019)
    Copyright (c) 2001-2019
    Ballard Technology, Inc.
    www.astronics.com
    Ballard.Support@astronics.com
    ALL RIGHTS RESERVED

    NAME:   EXAMP1.py -- Simulating the BC - Unscheduled Messages
"""

"""
    This example configures Card Number 0 as a BC to transmit
    the receive command 0843H with data words 1234H, 5678H,
    and 9ABCH.  If the message is completed successfully, it
    displays the responding RT's status word.  Otherwise it
    displays the value of any errors.
"""

import time
import BTICARD
import BTI429

CARDNUM         = 0
MAX_CORES       = 1
MAX_CHANNELS    = 2

def open_card():
    """
    Open the card with the specified card number.
    An error value is returned which is tested
    to determine if an error occurred.
    """
    errval, handle = BTICARD.CardOpen(CARDNUM)
    if (errval != 0):
        description = BTICARD.ErrDescStr(errval, handle)
        print(f'Error:  Either card number {CARDNUM} is not present, or')
        print(f'        an error occurred {errval} opening the card.')
        print(f'{ description }')    
    else:
        description = BTICARD.CardTypeStr(handle)
        description = description.decode("utf-8")
        print(f'BTICard_CardTypeStr =  { description }')
        description = BTICARD.CardProductStr(handle)
        description = description.decode("utf-8")
        print(f'BTICard_CardProductStr =  { description }') 
        result = BTICARD.CardGetInfo(BTICARD.INFOTYPE['SERIALNUM'],0,handle)
        print(f'BTICard_CardGetInfo serial number =  { result }') 

    return handle 

def open_core(hCard):
    """
    Find the first USB429 core and channel.
    """
    for corenum in range(MAX_CORES):
        errval, hCore = BTICARD.CoreOpen(hCard ,corenum)
        if (errval!=0):
            print(f'Could not Open Core: {corenum} Error Value: {errval}')
            break
        print(f'Using USB-429 core # {corenum}')

        for channum in range(MAX_CHANNELS):
                rc = BTI429.ChIsRcv(channum,hCore)
                if rc:
                    print(f'Using USB-429 channel # {channum}')
                    return hCore, channum
    return hCore, -1 


def card_reset( hCard, hCore, channum ):
    """
    Configure the channel for bus controller mode.
    """
    BTICARD.CardReset(hCard)

    errval = BTI429.ChConfig(BTI429.CHCFG429['DEFAULT'], channum, hCore)

    if (errval < 0):
        print(f"Error:  An error was encountered errval={errval} in BTI429 Config")

    return errval

def openARINC249Card():
    hCard =  open_card()

    if (hCard != 0):
        hCore, channum  = open_core(hCard)
        print("Receive channel successfully found")
        if ( -1!=channum ):
            errval = card_reset(hCard, hCore, channum)
            if (errval < 0):
                description = BTICARD.ErrDescStr(errval, hCore)
                print(f'BTICard_ErrDescStr =  { description.decode("utf-8") }') 
                BTICARD.CardClose(hCard)
                return -99

            """
            Reset the card
            """
            errval = BTICARD.CardReset(hCore)

            if errval != 0:
                print("Error resetting the card")
                BTICARD.CardClose(hCard)
                return -99
            else:
                print("Card reset was successful")
            
            errval = BTI429.ChConfig(BTI429.CHCFG429['AUTOSPEED'],channum,hCore)
            if errval != 0:
                print("Error setting the channel to AUTOSPEED the card")
                BTICARD.CardClose(hCard)
                return -99

            #Start operation of the card.
            
            if(BTICARD.CardStart(hCore) != 0):
                print("ERROR starting the core.")
                return -99
            else:
                print("Core successfully started.")
    
            time.sleep(2)
            return hCard, channum, hCore
    else:
        BTICARD.CardClose(hCard)
        return -99   



def readARINCaltitude(channum,hCore):

            # msg = BTI429.MSGSTRUCT429()
            # msg.addr = BTI429.FilterDefault(BTI429.MSGCRT429['DEFAULT'],channum,hCore)
            altitude = BTI429.MSGSTRUCT429()
            altitude.addr  = BTI429.FilterSet(BTI429.MSGCRT429['DEFAULT'],0o165,0xFFFFFFFF,channum,hCore)
#            maintenance = BTI429.MSGSTRUCT429()
#            maintenance.addr = BTI429.FilterSet(BTI429.MSGCRT429['DEFAULT'],0o270,0xFFFFFFFF,channum,hCore)

            for i in range(100):
                # msg.data = BTI429.MsgDataRd(msg.addr,hCore)
                altitude.data = BTI429.MsgDataRd(altitude.addr,hCore)
                # Clear the parity bit (later check the parity if necessary)
                altitude.data = altitude.data & 0x7FFFFFFF

                match (altitude.data >> 29):
                    case 0:
                        print("Positive Altitude")
                        sign = 1
                    case 1:
                        print("No Computed Data (NCD)")
                        return -99
                    case 2:
                        print("Functional Test")
                        return -99
                    case 3:
                        print("Negative altitude")
                        sign = -1

                altBCD = (altitude.data >> 10) & 0x7FFFF

                alt = (altBCD & 0xF) / 10
                alt = alt + ((altBCD >> 4) & 0xF)
                alt = alt + ((altBCD >> 8) & 0xF) * 10
                alt = alt + ((altBCD >> 12) & 0xF) * 100
                alt = alt + ((altBCD >> 16) & 0xF) * 1000

                alt = sign * alt


                #maintenance.data = BTI429.MsgDataRd(maintenance.addr,hCore)
                # print(hex(msg.data))
                #print(hex(altitude.data))
                #print(hex(altBCD))
                return alt
                #print(hex(maintenance.data))

            

def closeARINC249Card(hCard, hCore):
            """
            Stop the card.
            """
            BTICARD.CardStop(hCore)

            """
            The card MUST be closed before exiting the program.
            """

            BTICARD.CardClose(hCard)
            

