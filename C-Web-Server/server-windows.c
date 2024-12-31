#include <WinSock2.h>
#include <WS2tcpip.h>
#include <minwinbase.h>
#include <minwindef.h>
#include <stdio.h>
#include <stdbool.h>
#include <process.h>
#include <Windows.h>
#include <stdlib.h>
#include <iphlpapi.h>
#include <string.h>


#pragma comment(lib, "wsock32.lib")
#pragma comment (lib, "Ws2_32.lib")

#define PORT 8080
#define WEBSOCKET_PORT 8081
#define BUFFER_SIZE 4096
#define WATCH_DIRECTORY "."
#define MAX_PATH_LEN 512
#define FILE_WATCH_INTERVAL 50

// Colors
#define RESET   "\x1b[0m"
#define GREEN   "\x1b[32m"
#define YELLOW  "\x1b[33m"
#define BLUE    "\x1b[34m"
#define MAGENTA "\x1b[35m"
#define CYAN    "\x1b[36m"
#define RED     "\x1b[31m"

#define LOG_ERROR(msg, ...) { \
    printf(RED "[ERROR] " msg RESET "\n", ##__VA_ARGS__); \
    printf(YELLOW "Detailed error information can be found in server logs.\n" RESET); \
}

#define LOG_INFO(msg, ...) { \
    printf(CYAN "[INFO] " msg RESET "\n", ##__VA_ARGS__); \
}


// Global variables for synchronization
volatile bool g_server_running = true;
volatile bool g_file_changed = false;
CRITICAL_SECTION g_critical_section;
HANDLE g_file_change_thread = NULL;
SOCKET g_listen_socket = INVALID_SOCKET;
char g_current_directory[MAX_PATH];


// Function Prototypes
unsigned int __stdcall FileWatchThread(void* arg);
void get_local_ip(char* ip_buffer, size_t buffer_size);
void SendFile(SOCKET ClientSocket, const char* filepath);
void HandleFaviconRequest(SOCKET ClientSocket);
void SendHttpResponse(SOCKET ClientSocket, const char* content_type, const char* content, size_t content_length);
void HandleClientRequest(SOCKET ClientSocket, char* request);
void StartFileWatchThread();
void StopServer();
void SetupSocketServer();
void HandleClientConnections();


// Functions
// Get Local IP Address
void get_local_ip(char* ip_buffer, size_t buffer_size) {
    WSADATA wsaData;
    char hostname[256];
    struct hostent* host_entry;
    
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        strncpy(ip_buffer, "Unknown", buffer_size);
        return;
    }
    
    if (gethostname(hostname, sizeof(hostname)) == SOCKET_ERROR) {
        strncpy(ip_buffer, "Unknown", buffer_size);
        WSACleanup();
        return;
    }
    
    host_entry = gethostbyname(hostname);
    if (host_entry == NULL) {
        strncpy(ip_buffer, "Unknown", buffer_size);
        WSACleanup();
        return;
    }
    
    char* ip = inet_ntoa(*(struct in_addr*)*host_entry->h_addr_list);
    strncpy(ip_buffer, ip, buffer_size);
    
    WSACleanup();
}

// Send File Content
void SendFile(SOCKET ClientSocket, const char* filepath) {
    // Special handling for favicon.ico
    if (strstr(filepath, "favicon.ico")) {
        HandleFaviconRequest(ClientSocket);
        return;
    }

    FILE* file = fopen(filepath, "rb");
    if (!file) {
        // Enhanced File Not Found Response
        const char* not_found = 
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/plain\r\n"
            "Content-Length: 12\r\n\r\n"
            "File Not Found";
        send(ClientSocket, not_found, strlen(not_found), 0);
        LOG_ERROR("File not found: %s", filepath);
        return;
    }

    // Get file size
    fseek(file, 0, SEEK_END);
    long file_size = ftell(file);
    rewind(file);

    // Comprehensive Content Type Detection
    const char* content_type = "application/octet-stream";
    const char* ext = strrchr(filepath, '.');
    if (ext) {
        if (strcmp(ext, ".html") == 0) content_type = "text/html; charset=utf-8";
        else if (strcmp(ext, ".css") == 0) content_type = "text/css; charset=utf-8";
        else if (strcmp(ext, ".js") == 0) content_type = "application/javascript; charset=utf-8";
        else if (strcmp(ext, ".png") == 0) content_type = "image/png";
        else if (strcmp(ext, ".jpg") == 0 || strcmp(ext, ".jpeg") == 0) content_type = "image/jpeg";
        else if (strcmp(ext, ".gif") == 0) content_type = "image/gif";
        else if (strcmp(ext, ".svg") == 0) content_type = "image/svg+xml; charset=utf-8";
        else if (strcmp(ext, ".json") == 0) content_type = "application/json; charset=utf-8";
    }

    // Memory allocation with error handling
    char* buffer = malloc(file_size);
    if (!buffer) {
        fclose(file);
        const char* server_error = 
            "HTTP/1.1 500 Internal Server Error\r\n"
            "Content-Type: text/plain\r\n"
            "Content-Length: 22\r\n\r\n"
            "Server Memory Error";
        send(ClientSocket, server_error, strlen(server_error), 0);
        LOG_ERROR("Memory allocation failed for file: %s", filepath);
        return;
    }

    // Read file
    size_t bytes_read = fread(buffer, 1, file_size, file);
    fclose(file);

    if (bytes_read != file_size) {
        free(buffer);
        const char* read_error = 
            "HTTP/1.1 500 Internal Server Error\r\n"
            "Content-Type: text/plain\r\n"
            "Content-Length: 19\r\n\r\n"
            "File Reading Error";
        send(ClientSocket, read_error, strlen(read_error), 0);
        LOG_ERROR("Failed to read complete file: %s", filepath);
        return;
    }

    // Prepare HTTP response
    char header[256];
    snprintf(header, sizeof(header), 
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: %s\r\n"
        "Content-Length: %ld\r\n"
        "Cache-Control: no-cache, no-store, must-revalidate\r\n"
        "Pragma: no-cache\r\n"
        "Expires: 0\r\n"
        "\r\n", content_type, file_size);

    // Send header and file content
    send(ClientSocket, header, strlen(header), 0);
    send(ClientSocket, buffer, bytes_read, 0);

    free(buffer);
    LOG_INFO("Served file: %s", filepath);
}

// Favicon Handling
void HandleFaviconRequest(SOCKET ClientSocket) {
    const char* favicon_response = 
        "HTTP/1.1 404 Not Found\r\n"
        "Content-Type: image/x-icon\r\n"
        "Content-Length: 0\r\n\r\n";
    send(ClientSocket, favicon_response, strlen(favicon_response), 0);
    LOG_INFO("Favicon not found, sending minimal response");
}

// File Watch Thread with Optimized Detection
unsigned int __stdcall FileWatchThread(void* arg) {
    HANDLE hDir;
    FILE_NOTIFY_INFORMATION* pNotify;
    char buffer[4096];  // Increased buffer size
    DWORD bytesReturned;
    DWORD lastTriggerTime = 0;

    hDir = CreateFile(
        g_current_directory,
        FILE_LIST_DIRECTORY,
        FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE,
        NULL,
        OPEN_EXISTING,
        FILE_FLAG_BACKUP_SEMANTICS,
        NULL
    );

    if (hDir == INVALID_HANDLE_VALUE) {
        LOG_ERROR("Could not open directory for watching");
        return 1;
    }

    while (g_server_running) {
        if (ReadDirectoryChangesW(
            hDir, 
            buffer, 
            sizeof(buffer), 
            TRUE,  // Watch subtree
            FILE_NOTIFY_CHANGE_LAST_WRITE | FILE_NOTIFY_CHANGE_FILE_NAME,
            &bytesReturned,
            NULL,
            NULL
        )) {
            pNotify = (FILE_NOTIFY_INFORMATION*)buffer;
            
            wchar_t* fileName = pNotify->FileName;
            size_t len = pNotify->FileNameLength / sizeof(wchar_t);
            fileName[len] = L'\0';

            // Rapid change debounce mechanism
            DWORD currentTime = GetTickCount();
            if (currentTime - lastTriggerTime > FILE_WATCH_INTERVAL) {
                if (wcsstr(fileName, L".html") || 
                    wcsstr(fileName, L".css") || 
                    wcsstr(fileName, L".js") ||
                    wcsstr(fileName, L".png") ||
                    wcsstr(fileName, L".jpg") ||
                    wcsstr(fileName, L".jpeg") ||
                    wcsstr(fileName, L".gif") ||
                    wcsstr(fileName, L".svg")) {
                    
                    printf(CYAN "File change detected: %ls\n" RESET, fileName);
                    
                    // Signal server restart with minimal delay
                    EnterCriticalSection(&g_critical_section);
                    g_file_changed = true;
                    StopServer();
                    SetupSocketServer();
                    LeaveCriticalSection(&g_critical_section);

                    lastTriggerTime = currentTime;
                }
            }
        }
        Sleep(FILE_WATCH_INTERVAL);  // Reduced interval for faster detection
    }

    CloseHandle(hDir);
    return 0;
}

// Handle Client Request
void HandleClientRequest(SOCKET ClientSocket, char* request) {
    char* path = strstr(request, "GET ");
    if (!path) return;

    // Extract path
    path += 4;
    char* end = strstr(path, " HTTP");
    if (end) *end = '\0';

    // Decode URL (simple version)
    if (strcmp(path, "/") == 0) {
        path = "/index.html";
    }

    // Construct full file path
    char filepath[MAX_PATH];
    snprintf(filepath, sizeof(filepath), "%s%s", g_current_directory, path);

    // Send the file
    SendFile(ClientSocket, filepath);
}

void StartFileWatchThread() {
    InitializeCriticalSection(&g_critical_section);
    g_file_change_thread = (HANDLE)_beginthreadex(
        NULL, 
        0, 
        FileWatchThread, 
        NULL, 
        0, 
        NULL
    );
}

// Stop Server
void StopServer() {
    g_server_running = false;
    
    if (g_listen_socket != INVALID_SOCKET) {
        closesocket(g_listen_socket);
        g_listen_socket = INVALID_SOCKET;
    }
    
    WSACleanup();
}

// Setup Socket Server
void SetupSocketServer() {
    WSADATA wsaData;
    struct sockaddr_in server_addr;
    int iResult;

    g_server_running = true;
    
    iResult = WSAStartup(MAKEWORD(2,2), &wsaData);
    if (iResult != 0) {
        fprintf(stderr, "WSAStartup failed: %d\n", iResult);
        return;
    }

    // Create socket
    g_listen_socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (g_listen_socket == INVALID_SOCKET) {
        fprintf(stderr, "Socket creation failed: %d\n", WSAGetLastError());
        WSACleanup();
        return;
    }

    // Setup server address
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(PORT);

    // Bind socket
    iResult = bind(g_listen_socket, (struct sockaddr*)&server_addr, sizeof(server_addr));
    if (iResult == SOCKET_ERROR) {
        fprintf(stderr, "Bind failed: %d\n", WSAGetLastError());
        closesocket(g_listen_socket);
        WSACleanup();
        return;
    }

    // Listen
    if (listen(g_listen_socket, SOMAXCONN) == SOCKET_ERROR) {
        fprintf(stderr, "Listen failed: %d\n", WSAGetLastError());
        closesocket(g_listen_socket);
        WSACleanup();
        return;
    }

    SetConsoleOutputCP(CP_UTF8);


    // Print server details
    printf(GREEN "╔══════════════════════════════════════╗" RESET "\n");
    printf(GREEN "║          " CYAN "Web Server Started" GREEN "          ║" RESET "\n");
    printf(GREEN "╚══════════════════════════════════════╝" RESET "\n\n");

    // Get local IP
    char local_ip[50];
    get_local_ip(local_ip, sizeof(local_ip));

    printf(YELLOW "Server Details:" RESET "\n");
    printf("  " MAGENTA "➤ " BLUE "HTTP Endpoint" RESET "      :  " GREEN "http://localhost:%d" RESET "\n", PORT);
    printf("  " MAGENTA "➤ " BLUE "Local IP" RESET "           :  " GREEN "%s" RESET "\n", local_ip);
    printf("  " MAGENTA "➤ " BLUE "WebSocket Server" RESET "   :  " GREEN "ws://localhost:%d" RESET "\n", WEBSOCKET_PORT);
    printf("  " MAGENTA "➤ " BLUE "Watching Directory" RESET " :  " CYAN "%s" RESET "\n\n", g_current_directory);
}

// Handle Client Connections
void HandleClientConnections() {
    while (g_server_running) {
        SOCKET ClientSocket = accept(g_listen_socket, NULL, NULL);
        if (ClientSocket == INVALID_SOCKET) {
            fprintf(stderr, "Accept failed: %d\n", WSAGetLastError());
            break;
        }

        char recvbuf[BUFFER_SIZE];
        int recvResult = recv(ClientSocket, recvbuf, BUFFER_SIZE, 0);

        if (recvResult > 0) {
            recvbuf[recvResult] = '\0';  // Null-terminate
            HandleClientRequest(ClientSocket, recvbuf);
        }

        closesocket(ClientSocket);
    }
}


int main() {

    if (GetCurrentDirectoryA(sizeof(g_current_directory), g_current_directory) == 0) {
        fprintf(stderr, "Could not get current directory\n");
        return 1;
    }

    // Ensure path ends with backslash
    size_t len = strlen(g_current_directory);
    if (g_current_directory[len-1] != '\\') {
        g_current_directory[len] = '\\';
        g_current_directory[len+1] = '\0';
    }

    // Start file watching thread
    StartFileWatchThread();

    // Initial server setup
    SetupSocketServer();

    // Handle client connections
    HandleClientConnections();

    // Cleanup
    if (g_file_change_thread) {
        WaitForSingleObject(g_file_change_thread, INFINITE);
        CloseHandle(g_file_change_thread);
    }
    DeleteCriticalSection(&g_critical_section);

    return 0;
}
