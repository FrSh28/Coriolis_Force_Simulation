'''
 Copyright (C) 2018 Yi-Fan Shyu
 
 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is furnished
 to do so, subject to the following conditions:
 
 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.
 
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
 WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import os, threading, Queue

rd_path, wr_path = "\\\\.\\pipe\\discpendulum_wr", "\\\\.\\pipe\\discpendulum_rd"

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

