'''
Copyright 2018 Yi-Fan Shyu. Some rights reserved.
CC BY-NC-SA
'''
import os, threading, Queue

rd_path, wr_path = "\\\\.\\pipe\\foucault_wr", "\\\\.\\pipe\\foucault_rd"

inbuf = Queue.Queue()
outbuf = Queue.Queue()

def readfunc(inbuf, rd):
    while True:
        if inbuf.qsize() < 10:
            m = os.read(rd, 500)
            if m != "":
                inbuf.put(m)
    
def writefunc(outbuf, wr):
    while True:
        try:
            mess = outbuf.get()
            os.write(wr, mess)
        except Queue.Empty:
            pass
        
def connect():
    rd = os.open(rd_path, os.O_RDONLY)
    wr = os.open(wr_path, os.O_WRONLY)

    thr_rd = threading.Thread(target = readfunc, args = (inbuf, rd))
    thr_rd.daemon = True
    thr_rd.start()
    thr_wr = threading.Thread(target = writefunc, args = (outbuf, wr))
    thr_wr.daemon = True
    thr_wr.start()

def read():
    while True:
        try:
            return str(inbuf.get(False))
        except Queue.Empty:
            continue

def write(mess):
    if mess != "":
        outbuf.put(mess)



