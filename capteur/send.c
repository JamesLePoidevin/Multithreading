/////////////////////////////////////////////////////////////////////////////
// Creation 11/12/2003                                               
// 
// 
//                              SEND.C
//                              ------
// 
// 
// Sylvain MARECHAL - sylvain.marechal1@libertysurf.fr
/////////////////////////////////////////////////////////////////////////////
// 
//  Simple client
//  Usage: send localhost 1234
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
#include <string.h>


/////////////////////////////////////////////////////////////////////////////
//
//        SOCKADDR TCPFORMATADRESS
/////////////////////////////////////////////////////////////////////////////
//
//  DESCRIPTION
//       --sockaddr TcpFormatAdress--
//  ARGUMENTS
//        Argument1:  char * host
//        Argument2: u_short port
//  RETOUR/RESULTAT
//        static struct 
//  REMARQUE
//  Rev 11/12/2003 
//////////////////////////////////////////////////////////////////////////////
static struct sockaddr TcpFormatAdress( char * host, u_short port )
{
    struct sockaddr_in addr;
    struct sockaddr addrRet;
    struct hostent FAR *lphost ;
    u_long IP;
    
    
    memset((char*)&addr, 0, sizeof(addr));
    /*	Soit on fournit une adresse IP, soit on fournit un nom	*/
    if ((IP = inet_addr(host)) == (u_long)INADDR_NONE)
    {
	if ((lphost  = gethostbyname(host))==NULL)
	{
            memset( (char * )&addrRet, 0, sizeof(addrRet) );
	    return  addrRet;
	}
	addr.sin_family = lphost->h_addrtype;
#ifdef _WIN16 /* A définir dans le projet WIN16	*/
	_fmemcpy (&addr.sin_addr, lphost->h_addr, lphost->h_length);
#else /*	WIN32, UNIX*/
	memcpy (&addr.sin_addr, lphost->h_addr, lphost->h_length);
#endif
    }
    else
    {
        addr.sin_family = AF_INET;
        addr.sin_addr.s_addr = IP;
    }
    
    /*  Port destination    */    
    addr.sin_port = htons((u_short)port );    
    
    memcpy( (char *)&addrRet, (char *)&addr, sizeof(addrRet) );
    return addrRet;
}


/////////////////////////////////////////////////////////////////////////////
//
//        MAIN
/////////////////////////////////////////////////////////////////////////////
//
//  DESCRIPTION
//       --main--
//
//  Usage: send localhost 1234
//
//  ARGUMENTS
//        Argument1:  int argc
//        Argument2: char ** argv   The address where to connect
//  RETOUR/RESULTAT
//        int 
//  REMARQUE
//  Rev 11/12/2003 
//////////////////////////////////////////////////////////////////////////////
int main( int argc, char ** argv )
    {
    SOCKET hSocket;
    struct sockaddr_in addr; int len = sizeof(addr);
    struct sockaddr addrConnect;
    char BufSend[] = "coucou"; int cb;
    char BufRecv[1024];
    int nPort;
    char * pszHost;

    // Initialize winsock
    WSADATA stack_info ;
    WSAStartup(MAKEWORD(2,0), &stack_info) ;

    if( argc != 3 )
    {
	printf( "Usage: <%s> <host> <port>\n", argv[0] );
	pszHost = "127.0.0.1";
	nPort = 2000;
    }
    else
    {
	pszHost = argv[1];
	nPort = atoi(argv[2]);
    }
    printf( "Connecting to %s:%d\n", pszHost, nPort );
    

    /* socket TCP */
    hSocket = socket( PF_INET, SOCK_STREAM, 0 );
    if( hSocket == INVALID_SOCKET )
    {
	printf( "socket() error (%d)\n", SOCKET_ERRNO );
	return -1;
    }

    /*  bind */
    addr.sin_family = AF_INET ;
    addr.sin_addr.s_addr = htonl (INADDR_ANY);
    addr.sin_port = htons ((unsigned short)0 );
    if ( bind( hSocket, (struct sockaddr *)&addr, sizeof(addr)) == SOCKET_ERROR )
    {
	printf( "socket() error (%d)\n", SOCKET_ERRNO );
	return -1;
    }


    /* Transform the host/port into a struct sockaddr*/
    addrConnect = TcpFormatAdress( pszHost, (u_short)nPort );

    /*  blocking mode  */
    if( connect( hSocket, &addrConnect, sizeof(addrConnect) ) == SOCKET_ERROR )
    {
	printf( "connect() error (%d)\n", SOCKET_ERRNO );
	return -1;
    }

    cb = send( hSocket, BufSend, sizeof(BufSend), 0 );
//closesocket( hSocket );
//Sleep( INFINITE );
    cb = recv( hSocket, BufRecv, sizeof(BufRecv), 0 );
    printf( "Data received:'%s'\n", BufRecv );
    
    /* Wait to see*/
    Sleep( INFINITE );

    return 0;
}
