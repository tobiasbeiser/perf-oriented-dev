#define _XOPEN_SOURCE 500
#include <ftw.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>

#define TMP_DIR "io_loadgen_temp"
#define MAX_FILENAME_LENGTH 256
#define BUFFER_SIZE 1024

#define UNUSED(x) (void)(x)
int CANCELLED = 0;

// ----------------------------
// Source: https://stackoverflow.com/questions/5467725/how-to-delete-a-directory-and-its-contents-in-posix-c
int unlink_cb(const char *fpath, const struct stat *sb, int typeflag, struct FTW *ftwbuf)
{
    UNUSED(sb);
    UNUSED(typeflag);
    UNUSED(ftwbuf);
    int rv = remove(fpath);

    if (rv)
        perror(fpath);

    return rv;
}

int rmrf(char *path)
{
    return nftw(path, unlink_cb, 64, FTW_DEPTH | FTW_PHYS);
}
// ----------------------------

void cancelLoadGeneration(int signum)
{
    if (signum != SIGINT)
        return;
    printf("Load generation cancelled.\nCleaning up...\n");
    CANCELLED = 1;
}

void random_string(char *s, const int len)
{
    static const char charset[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    for (int i = 0; i < len; i++)
    {
        int r = rand() % (int)(sizeof(charset) - 1);
        s[i] = charset[r];
    }
    s[len - 1] = '\0';
}

void generate_load(int size, int files_per_dir, int enable_read, int enable_delete)
{
    long long size_in_bytes = size * 1024;
    int pid = getpid();
    char thread_tmp_dir[MAX_FILENAME_LENGTH];
    snprintf(thread_tmp_dir, MAX_FILENAME_LENGTH, "%d_%s", pid, TMP_DIR);


    mkdir(thread_tmp_dir, 0777);
    if (chdir(thread_tmp_dir) != 0)
    {
        perror("Error changing directory");
        exit(EXIT_FAILURE);
    }
    int i = 0;

    while (!CANCELLED)
    {
        char dirname[MAX_FILENAME_LENGTH];
        snprintf(dirname, MAX_FILENAME_LENGTH, "dir_%d", i);
        mkdir(dirname, 0777);

        for (int i = 0; i < files_per_dir; i++)
        {
            char filename[MAX_FILENAME_LENGTH];
            int written = snprintf(filename, MAX_FILENAME_LENGTH, "%s/file_%d", dirname, i);
            if (written < 0 || written >= MAX_FILENAME_LENGTH)
            {
                fprintf(stderr, "Error building file path");
            }

            FILE *file = fopen(filename, "a");
            if (file == NULL)
            {
                perror("Error opening file");
                exit(EXIT_FAILURE);
            }

            char *data = (char *)malloc(size_in_bytes);
            random_string(data, size_in_bytes);
            fwrite(data, 1, size_in_bytes, file);
            fclose(file);
        }

        if (enable_read)
        {
            for (int i = 0; i < files_per_dir; i++)
            {
                char filename[MAX_FILENAME_LENGTH];
                int written = snprintf(filename, MAX_FILENAME_LENGTH, "%s/file_%d", dirname, i);
                if (written < 0 || written >= MAX_FILENAME_LENGTH)
                {
                    fprintf(stderr, "Error building file path");
                }
                char fileContent[BUFFER_SIZE];
                FILE *file2 = fopen(filename, "r");
                fread(fileContent, 1, BUFFER_SIZE, file2);
                fclose(file2);
            }
        }
        if (enable_delete)
        {
             for (int i = 0; i < files_per_dir; i++)
            {
                char filename[MAX_FILENAME_LENGTH];
                int written = snprintf(filename, MAX_FILENAME_LENGTH, "%s/file_%d", dirname, i);
                if (written < 0 || written >= MAX_FILENAME_LENGTH)
                {
                    fprintf(stderr, "Error building file path");
                }
                remove(filename);
            }
            rmdir(dirname);
        }
    }
    chdir("..");
    rmrf(thread_tmp_dir);
    i++;
}

int main(int argc, char *argv[])
{

    if (argc != 5)
    {
        printf("Usage: %s <files_per_dir> <filesize (kb)> <enable_read> <enable_delete>\n", argv[0]);
        return EXIT_FAILURE;
    }
    signal(SIGINT, cancelLoadGeneration);
    int files_per_dir = atoll(argv[1]);
    int size = atoll(argv[2]);
    int enable_read = atoll(argv[3]);
    int enable_delete = atoll(argv[4]);

    printf("Generating load...\n");
    generate_load(size, files_per_dir, enable_read, enable_delete);
    printf("Load generation complete.\n");

    return EXIT_SUCCESS;
}