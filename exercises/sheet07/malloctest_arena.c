#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <inttypes.h>

typedef struct
{
    int64_t repeats;
    int64_t iterations;
    int64_t lower, upper;
} thread_args;

typedef struct
{
    void *arena;
    size_t arena_size;
    void *next;
} arena_allocator;

void *bump_alloc(arena_allocator *alloc, size_t size)
{
    if ((char *)alloc->next + size > (char *)alloc->arena + alloc->arena_size)
    {
        printf("Out of memory\n");
        return NULL;
    }
    void *ret = alloc->next;
    alloc->next = (char *)alloc->next + size;
    return ret;
}

void init_arena(arena_allocator *alloc, size_t size)
{
    alloc->arena = malloc(size);
    if (alloc->arena == NULL)
    {
        printf("Out of memory during init\n");
        exit(EXIT_FAILURE);
    }
    alloc->arena_size = size;
    alloc->next = alloc->arena;
}

void *benchmark_thread(void *args)
{
    thread_args *t_args = (thread_args *)args;

    arena_allocator alloc;
    init_arena(&alloc, t_args->upper * t_args->iterations);


    for (int64_t r = 0; r < t_args->repeats; ++r)
    {
        unsigned seed = 0;
        void **allocations = (void **)bump_alloc(&alloc, t_args->iterations * sizeof(void *));
        if (allocations == NULL)
        {
            printf("Could not allocate memory for allocations\n");
            exit(EXIT_FAILURE);
        }

        for (int64_t i = 0; i < t_args->iterations; ++i)
        {
            int64_t to_alloc = rand_r(&seed) % (t_args->upper - t_args->lower) + t_args->lower;
            allocations[i] = bump_alloc(&alloc, to_alloc);
            if (allocations[i] == NULL)
            {
                printf("Out of memory during allocation\n");
                exit(EXIT_FAILURE);
            }
        }
        // Reset the arena
        alloc.next = alloc.arena;
    }
    free(alloc.arena);
    return NULL;
}

int main(int argc, char **argv)
{
    int64_t num_threads = 100;
    if (argc != 6)
    {
        printf("USAGE: ./malloctest [num_threads] [num_repeats] [num_iterations] [lower] [upper]\n");
        return -1;
    }
    num_threads = atol(argv[1]);
    thread_args t_args;
    t_args.repeats = atol(argv[2]);
    t_args.iterations = atol(argv[3]);
    t_args.lower = atol(argv[4]);
    t_args.upper = atol(argv[5]);

    pthread_t *threads = (pthread_t *)calloc(num_threads, sizeof(pthread_t));

    for (int64_t i = 0; i < num_threads; ++i)
    {
        pthread_create(&threads[i], NULL, benchmark_thread, &t_args);
    }

    for (int64_t i = 0; i < num_threads; ++i)
    {
        pthread_join(threads[i], NULL);
    }
}
