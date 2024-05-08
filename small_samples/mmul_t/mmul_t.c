#include <stdio.h>
#include <stdlib.h>

#define S 2048
#define N S
#define M S
#define K S

#define MIN(X,Y) ((X)<(Y)?(X):(Y))
#define MAX(X,Y) ((X)>(Y)?(X):(Y))

#define TYPE double
#define MATRIX TYPE**

// A utility function
MATRIX createMatrix(unsigned x, unsigned y) {
	TYPE* data = malloc(x * y * sizeof(TYPE));

	TYPE** index = malloc(x * sizeof(TYPE*));
	index[0] = data;
	for (unsigned i = 1; i < x; ++i) {
		index[i] = &(data[i*y]);
	}
	return index;
}

void freeMatrix(MATRIX matrix) {
	free(matrix[0]);
	free(matrix);
}


int main(int argc, char*argv[]) {


	int TILE_HEIGHT, TILE_WIDTH;

	if (argc != 3)
	{
		fprintf(stderr, "Usage: %s TILE_HEIGHT TILE_WIDTH\n", argv[0]);
		exit(EXIT_FAILURE);
	}
	

	if (sscanf (argv[1], "%i", &TILE_HEIGHT) != 1) {
    	fprintf(stderr, "error - not an integer");
		exit(EXIT_FAILURE);
	}
	if (sscanf (argv[2], "%i", &TILE_WIDTH) != 1) {
    	fprintf(stderr, "error - not an integer");
		exit(EXIT_FAILURE);
	}



	// create the matrices
	MATRIX A = createMatrix(N, M);
	MATRIX B = createMatrix(M, K);
	MATRIX C = createMatrix(N, K);

	// initialize the matrices

	// A contains real values
	for (int i=0; i<N; i++) {
		for (int j=0; j<M; j++) {
			A[i][j] = i*j;
		}
	}

	// B is the identity matrix
	for (int i=0; i<M; i++) {
		for (int j=0; j<K; j++) {
			B[i][j] = (i==j)?1:0;
		}
	}




		// conduct multiplication
	for (int i = 0; i < N; i += TILE_HEIGHT) {
		for (int j = 0; j < K; j += TILE_WIDTH) {
			for (int ii = i; ii < (i + TILE_HEIGHT < N ? i + TILE_HEIGHT : N); ii++) {
				for (int jj = j; jj < (j + TILE_WIDTH < K ? j + TILE_WIDTH : K); jj++) {
					TYPE sum = 0;
					for (int k = 0; k < M; k++) {
                    	sum += A[ii][k] * B[k][jj];
                	}
            	    C[ii][jj] = sum;
        	    }
    	    }
	    }
	}

	// verify result
	int success = 1;	
	for (int i=0; i<N; i++) {
		for (int j=0; j<MIN(M,K); j++) {
			if (A[i][j] != C[i][j]) {
				success = 0;
			}
		}
		for (int j=MIN(M,K); j<MAX(M,K); j++) {
			if (C[i][j] != 0) {
				success = 0;
			}
		}
	}

	// print verification result
	printf("Verification: %s\n", (success)?"OK":"ERR");

	freeMatrix(A);
	freeMatrix(B);
	freeMatrix(C);

	return success ? EXIT_SUCCESS : EXIT_FAILURE;
}

