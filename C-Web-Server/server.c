// server.c

#include <asm-generic/socket.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>             // For Core socket APIs
#include <netinet/in.h>            // Address Structure
#include <arpa/inet.h>             //  For inet_ntoa()
#include <unistd.h>
#include <fcntl.h>                 // File opening (open() function)
#include <sys/stat.h>              // Stats (stat() function)
#include <pthread.h>
#include <sys/inotify.h>
#include <signal.h>
#include <libwebsockets.h>

#define PORT 8000
#define WEBSOCKET_PORT 8001
#define BUFFER 4096
#define INOTIFY_EVENTS_SIZE (sizeof(struct inotify_event) + NAME_MAX + 1)


// Global variables for server management
volatile sig_atomic_t keep_running = 1;
volatile int file_changed = 0;

char *read_file(const char *filename, size_t *length);
const char *get_mime_type(const char *filename);
void *file_watch_thread(void *filename);
void *websocket_server_thread(void *arg);
static int websocket_callback(struct lws *wsi, enum lws_callback_reasons reason,
                              void *user, void *in, size_t len);


// File reading
char *read_file(const char *filename, size_t *length) {

	FILE *file = fopen(filename, "r");
	if (!file) {
		printf("Failed to open file");
		return NULL;
	}

	struct stat st;
	if (stat(filename, &st) != 0) {
		perror("Stat failed");
		fclose(file);
		return NULL;
	}

	*length = st.st_size;
    char *content = malloc(*length + 1); // Allocate memory for file contents
    if (!content) {
        perror("malloc failed");
        fclose(file);
        return NULL;
    }

    // Read file into buffer
    fread(content, 1, *length, file);
    content[*length] = '\0'; // Null-terminate the string
    fclose(file);
    return content;
}

// File MIME type
const char *get_mime_type(const char *filename) {

	const char *ext = strrchr(filename, '.');   // getting the extension
	if (!ext) {
		return "application/octet-stream";
	}

	if (strcmp(ext, ".html") == 0) return "text/html";
    if (strcmp(ext, ".css") == 0) return "text/css";
    if (strcmp(ext, ".js") == 0) return "application/javascript";
    if (strcmp(ext, ".png") == 0) return "image/png";
    if (strcmp(ext, ".jpg") == 0 || strcmp(ext, ".jpeg") == 0) return "image/jpeg";
    if (strcmp(ext, ".gif") == 0) return "image/gif";
    return "application/octet-stream"; // Default for unknown types
}

// file watching thread
void *file_watch_thread(void *filename) {
	const char *file_to_watch = (const char *)filename;
	int fd = inotify_init();
	if (fd < 0) {
		perror("inotify_init error");
		pthread_exit(NULL);
	}

	int wd = inotify_add_watch(fd, file_to_watch, IN_MODIFY);
	if (wd < 0) {
		perror("inotify_add_watch");
		close(fd);
		pthread_exit(NULL);
	}
	printf("Watching file for changes: %s\n", file_to_watch);

	char buffer[INOTIFY_EVENTS_SIZE];
	while (keep_running) {
        int length = read(fd, buffer, INOTIFY_EVENTS_SIZE);
        if (length < 0) {
            if (errno != EAGAIN) {
                perror("inotify read");
            }
            break;
        }

        file_changed = 1;
        printf("File changed: %s\n", file_to_watch);
    }

    inotify_rm_watch(fd, wd);
    close(fd);
    pthread_exit(NULL);
}

// WebSocket Callback
static int websocket_callback(struct lws *wsi, enum lws_callback_reasons reason,
                              void *user, void *in, size_t len) {
    switch (reason) {
        case LWS_CALLBACK_ESTABLISHED:
            printf("WebSocket connection established.\n");
            break;
        case LWS_CALLBACK_SERVER_WRITEABLE:
            if (file_changed) {
                unsigned char message[LWS_PRE + 2];
                unsigned char *p = &message[LWS_PRE];
                p[0] = 'r'; // Reload signal
                lws_write(wsi, p, 1, LWS_WRITE_TEXT);
                file_changed = 0;
            }
            break;
        default:
            break;
    }
    return 0;
}

// WebSocket Protocols
static struct lws_protocols protocols[] = {
    {
        "live-reload",
        websocket_callback,
        0,
        0
    },
    { NULL, NULL, 0, 0 }
};

// WebSocket Server Thread
void *websocket_server_thread(void *arg) {
    struct lws_context_creation_info info = {0};
    info.port = WEBSOCKET_PORT;
    info.protocols = protocols;
    info.gid = -1;
    info.uid = -1;

    struct lws_context *context = lws_create_context(&info);
    if (!context) {
        fprintf(stderr, "WebSocket context creation failed\n");
        pthread_exit(NULL);
    }

    printf("WebSocket server running on ws://localhost:%d\n", WEBSOCKET_PORT);

    while (keep_running) {
        lws_service(context, 50);
    }

    lws_context_destroy(context);
    pthread_exit(NULL);
}

// Signal Handler
void handle_signal(int sig) {
    keep_running = 0;
    printf("\nReceived signal %d. Shutting down...\n", sig);
}

int is_favicon_request(const char *requested_file) {
    return (strcmp(requested_file, "favicon.ico") == 0);
}

int main() {

	// Signal handling
    signal(SIGINT, handle_signal);
    signal(SIGTERM, handle_signal);

    // Thread management
    pthread_t watcher_thread, ws_thread;

    // Create threads for file watching and WebSocket
    if (pthread_create(&watcher_thread, NULL, file_watch_thread, "index.html") != 0) {
        perror("Failed to create file watcher thread");
        exit(EXIT_FAILURE);
    }

    if (pthread_create(&ws_thread, NULL, websocket_server_thread, NULL) != 0) {
        perror("Failed to create WebSocket server thread");
        exit(EXIT_FAILURE);
    }

	int server_fd, new_socket;
	struct sockaddr_in address;
	int opt = 1;
	int addrlen = sizeof(address);
	char buffer[1024] = {0};
		
	// socket file descriptor
	if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
		perror("Socket Failed");
		exit(EXIT_FAILURE);
	}

	// Socket options
	if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt)) < 0) {
		perror("setsockopt failed");
		close(server_fd);
		exit(EXIT_FAILURE);
	}

	// Address configuration
	address.sin_family = AF_INET;                   // IPv4
    address.sin_addr.s_addr = INADDR_ANY;
	address.sin_port = htons(PORT);

	// Socket bind to port and address
	if (bind(server_fd, (struct sockaddr *)&address, sizeof(address))<0) {
		perror("Bind failed");
        close(server_fd);
        exit(EXIT_FAILURE);
	}

	// Incoming connections
	if (listen(server_fd, 3) <0) {
		perror("Listen failed");
    	    close(server_fd);
        exit(EXIT_FAILURE);
	}

	printf("Server running on http://localhost:%d\n", PORT);

	// Injecting JS auto reload
	const char *reload_script = 
		"<script>"
		"const ws = new WebSocket('ws://localhost:8001');"
		"ws.onmessage = (event) => {"
        "   if (event.data === 'r') location.reload();"
        "};"
        "</script>";

	// Incoming connections
	while (keep_running) {

		if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t *)&addrlen)) < 0) {
		perror("Accept failed");
            continue;
		}
		read(new_socket, buffer, sizeof(buffer) - 1);
        printf("Request:\n%s\n", buffer);

		// Parsing the requested file via HTTP GET
		char *method = strtok(buffer, " ");
        char *requested_file = strtok(NULL, " ");
        if (!method || !requested_file || strcmp(method, "GET") != 0) {
            close(new_socket);
            continue;
        }

		if (requested_file[0] == '/') {
            requested_file++;
        }
        if (strlen(requested_file) == 0) {
            requested_file = "index.html";
		}

		if (is_favicon_request(requested_file)) {
	
    		const char *favicon_response = 
       		"HTTP/1.1 204 No Content\r\n"
    	    "Content-Length: 0\r\n\r\n";
    
    		// Print a minimal warning
    		printf("Warning: Favicon request ignored\n");
    
    		write(new_socket, favicon_response, strlen(favicon_response));
    		close(new_socket);
    		continue;  // Skip to next iteration of the main loop
		}


		// Load `index.html`
        size_t file_length;
        char *file_content = read_file(requested_file, &file_length);

        if (file_content) {

			const char *mime_type = get_mime_type(requested_file);
            // Append reload script to HTML files
            if (strcmp(mime_type, "text/html") == 0) {
                char *enhanced_content = malloc(file_length + strlen(reload_script) + 1);
                strcpy(enhanced_content, file_content);
                strcat(enhanced_content, reload_script);

                char header[256];
                snprintf(header, sizeof(header),
                         "HTTP/1.1 200 OK\n"
                         "Content-Type: %s\n"
                         "Content-Length: %zu\n\n",
                         mime_type, strlen(enhanced_content));

                write(new_socket, header, strlen(header));
                write(new_socket, enhanced_content, strlen(enhanced_content));

                free(enhanced_content);
            } else {
                // Regular response for non-HTML files
                char header[256];
                snprintf(header, sizeof(header),
                         "HTTP/1.1 200 OK\n"
                         "Content-Type: %s\n"
                         "Content-Length: %zu\n\n",
                         mime_type, file_length);

                write(new_socket, header, strlen(header));
                write(new_socket, file_content, file_length);
            }

            free(file_content);
        } else {
            const char *error_response =
                "HTTP/1.1 404 Not Found\n"
                "Content-Type: text/html\n\n"
                "<html><body><h1>404 Not Found</h1></body></html>";
            write(new_socket, error_response, strlen(error_response));
        }

        // Close the connection
        close(new_socket);
    }

    // Cleanup
	pthread_join(watcher_thread, NULL);
    pthread_join(ws_thread, NULL);
    close(server_fd);
    return 0;
}

