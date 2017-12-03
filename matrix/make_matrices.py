import numpy as np
import os

m, n, k = 3, 8, 5

def main():
    with open("./m.csv", 'w') as f:
        f.write("{},{},{},{}\n".format('m_name', 'row', 'col', 'val'))
        for i in range(m):
            for j in range(n):
                #val = np.random.randint(0,5)
                val = i*10+j
                f.write("{},{},{},{}\n".format('a', i, j, val))

        for i in range(n):
            for j in range(k):
                #val = np.random.randint(0,5)
                val = i*10+j
                f.write("{},{},{},{}\n".format('b', i, j, val))



if __name__ == "__main__":
    main()