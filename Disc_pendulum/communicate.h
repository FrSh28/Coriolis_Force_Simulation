/*Copyright (C) 2018 Yi-Fan Shyu
* 
* Permission is hereby granted, free of charge, to any person obtaining a copy
* of this software and associated documentation files (the "Software"), to deal
* in the Software without restriction, including without limitation the rights
* to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
* copies of the Software, and to permit persons to whom the Software is furnished
* to do so, subject to the following conditions:
* 
* The above copyright notice and this permission notice shall be included in all
* copies or substantial portions of the Software.
* 
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
* FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
* COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
* IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
* WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

#include <cstring>
#include <windows.h>
#include <iostream>
using namespace std;
#define output "\\\\.\\pipe\\discpendulum_wr"	//"\\.\pipe\discpendulum_wr"
#define input "\\\\.\\pipe\\discpendulum_rd"	//"\\.\pipe\discpendulum_rd"
#define MaxBuf 500
HANDLE wr = NULL, rd = NULL;
const int timeout = 3;
STARTUPINFO si;
PROCESS_INFORMATION pi;
void close(bool ClientStart = true);

bool create()
{
	//create named pipe
	wr = CreateNamedPipe(output, PIPE_ACCESS_OUTBOUND,
					PIPE_WAIT|PIPE_TYPE_MESSAGE|PIPE_READMODE_MESSAGE|PIPE_REJECT_REMOTE_CLIENTS,
					1, MaxBuf, MaxBuf, 0, NULL);
	rd = CreateNamedPipe(input, PIPE_ACCESS_INBOUND,
					PIPE_WAIT|PIPE_TYPE_MESSAGE|PIPE_READMODE_MESSAGE|PIPE_REJECT_REMOTE_CLIENTS,
					1, MaxBuf, MaxBuf, 0, NULL);
	if(wr == INVALID_HANDLE_VALUE && rd == INVALID_HANDLE_VALUE)
		return false;
	
	//connect to client
	if(!ConnectNamedPipe(wr, NULL) && GetLastError() != ERROR_PIPE_CONNECTED)
		close();
	if(!ConnectNamedPipe(rd, NULL) && GetLastError() != ERROR_PIPE_CONNECTED)
		close();
	
	return true;
}

bool write_to_client(char message[])
{
	DWORD wrlen = 0;
	FlushFileBuffers(wr);
	int times = 0;
	while(times < timeout)
	{
		if(WriteFile(wr, message, MaxBuf, &wrlen, 0))
			return true;
		times++;
	}
	return false;
}
	
bool read_from_client(char message[])
{
	DWORD rdlen = 0;
	int times = 0;
	while(times < timeout)
	{
		if(ReadFile(rd, message, MaxBuf, &rdlen, 0))
			return true;
		times++;
	}
	return false;
}

void close(bool ClientStart)
{
	FlushFileBuffers(wr);
	//close pipe
	DisconnectNamedPipe(wr);
	CloseHandle(wr);
	DisconnectNamedPipe(rd);
	CloseHandle(rd);
}

void reconnect()
{
	DisconnectNamedPipe(wr);
	DisconnectNamedPipe(rd);
	if(!ConnectNamedPipe(wr, NULL) && GetLastError() != ERROR_PIPE_CONNECTED)
		close();
	if(!ConnectNamedPipe(rd, NULL) && GetLastError() != ERROR_PIPE_CONNECTED)
		close();
}
