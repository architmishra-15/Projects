#ifndef SERVER_H
#define SERVER_H

// Macros
#define PORT 8000
#define WEBSOCKET_PORT 8001
#define BUFFER 4096
#define INOTIFY_EVENTS_SIZE (sizeof(struct inotify_event) + NAME_MAX + 1)

// Standard Libraries
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

// Network Libraries
#include <sys/socket.h>    // Core socket APIs
#include <netinet/in.h>    // Address Structure
#include <arpa/inet.h>     // For inet_ntoa()
#include <asm-generic/socket.h>

// File and System Libraries
#include <unistd.h>
#include <fcntl.h>         // File opening (open() function)
#include <sys/stat.h>      // Stats (stat() function)
#include <sys/inotify.h>   // File monitoring
#include <signal.h>        // Signal handling
#include <pthread.h>       // Multithreading
#include <termios.h>       // Terminal control

#endif // SERVER_H
