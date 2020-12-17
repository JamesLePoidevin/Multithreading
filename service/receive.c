/////////////////////////////////////////////////////////////////////////////
// Creation 11/12/2003                                               
// 
// 
//                              RECV.C
//                              ------
// 
// 
// Sylvain MARECHAL - sylvain.marechal1@libertysurf.fr
/////////////////////////////////////////////////////////////////////////////
// 
//  Simple server waiting for a connexion
//  Usage: recv 1234
// 
/////////////////////////////////////////////////////////////////////////////
#ifdef _WIN32
#include <winsock2.h>
#define	SOCKET_ERRNO	WSAGetLastError()
#define	ERRNO		GetLastError()
#else
#define	SOCKET_ERRNO	errno
#define	ERRNO		errno
#define closesocket	close
#endif
#include <io.h>
#include <fcntl.h>
#include <stdio.h>
#include <conio.h>
#include <errno.h>


/////////////////////////////////////////////////////////////////////////////
//
//        MAIN
/////////////////////////////////////////////////////////////////////////////
//
//  DESCRIPTION
//       --main--
//
//  Usage: recv 1234
//
//  ARGUMENTS
//        Argument1:  int argc
//        Argument2: char * argv[]  The port to listen
//  RETOUR/RESULTAT
//        int 
//  REMARQUE
//  Rev 11/12/2003 
//////////////////////////////////////////////////////////////////////////////
int main( int argc, char * argv[] )
{
    SOCKET hSocket, hAccept;
    struct sockaddr_in addr;
    int len = sizeof(addr);    
    char Buffer[1024]; int cb;
    int nPort;
    
    // Initialize winsock
    WSADATA stack_info ;
    WSAStartup(MAKEWORD(2,0), &stack_info) ;
    
    
    if( argc != 2 )
    {
	printf( "Usage: <%s> <port>\n", argv[0] );
	nPort = 2000;
    }
    else
    {
	nPort = atoi(argv[1]);
    }
    printf( "Listening port %d\n", nPort );

    // Listen port
    hSocket = socket( PF_INET, SOCK_STREAM, 0 );
    if( hSocket == INVALID_SOCKET )
    {
	printf( "socket() error %d\n", SOCKET_ERRNO );
	exit(1);
    }
    addr.sin_family = AF_INET ;
    addr.sin_addr.s_addr = htonl (INADDR_ANY);
    addr.sin_port = htons ((unsigned short)nPort );
    if ( bind( hSocket, (struct sockaddr *)&addr, sizeof(addr)) == SOCKET_ERROR )
    {
	printf( "bind() error %d\n", SOCKET_ERRNO );
	exit(1);
    }
    if ( listen( hSocket, 100) == SOCKET_ERROR )
    {
	printf( "listen() error %d\n", SOCKET_ERRNO );
	exit(1);
    }
    
    
    while( 1 )
    {
	// Wait accept
	hAccept = accept(hSocket, NULL, NULL);
	if( hAccept != INVALID_SOCKET )
	{	    
	    // Read
	    cb = recv( hAccept, Buffer, sizeof(Buffer), 0 );
	    if( cb <= 0 )
	    {
		printf( "recv() error %d\n", SOCKET_ERRNO );
		exit(1);
	    }
//Sleep( INFINITE );
	    printf( "Data received:'%s'\n", Buffer );
	    
	    // Send 
	    cb = send( hAccept, Buffer, cb, 0 );
	    if( cb == SOCKET_ERROR )
	    {
		printf( "send() error %d\n", SOCKET_ERRNO );
		exit(1);
	    }
	    closesocket( hAccept );
	}
    }
    closesocket( hSocket );
}

