from time import time
from multiprocessing import Pool, Process, cpu_count, Semaphore
import concurrent.futures
from random import randint


def factorize(number):
    result = []
    for i in number:
        f = [x for x in range(1, i + 1) if i % x == 0]
        result.append(f)
    return tuple(result)


def factorize_m(number: int, semaphore: Semaphore):
    with semaphore:
        return [x for x in range(1, number + 1) if number % x == 0]


def factorize_p(number: int):
    return [x for x in range(1, number + 1) if number % x == 0]

# a, b, c, d  = factorize(128, 255, 99999, 10651060)
#
# assert a == [1, 2, 4, 8, 16, 32, 64, 128]
# assert b == [1, 3, 5, 15, 17, 51, 85, 255]
# assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
# assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
#

if __name__ == '__main__':
    # n = [128, 255, 99999, 10651060]
    n = [randint(1, 9999999) for x in range(100)]
# metod 1 SINGLE
    start_single = time()
    print(factorize(n))
    print(f'single: {time() -  start_single}')
# metod 2 SEMAPHOR
    start_semaphore = time()
    # print(cpu_count()) # 8
    semaphore = Semaphore(cpu_count())
    processes = []
    for i in n:
        pr = Process(target=factorize_m, args=(i, semaphore))
        pr.start()
        processes.append(pr)

    [pr.join() for pr in processes]
    print(f'semaphore: {time() - start_semaphore}')
# metod 3 POOL
    start_pool = time()
    with Pool(processes=cpu_count()) as pool:
        pool.map(factorize_p, n)
    print(f'semaphore_pool: {time() - start_pool}')
# metod 4 POOL_EX
    start_pool_ex = time()
    with concurrent.futures.ProcessPoolExecutor(cpu_count()) as executor:
        for number in n:
            factorize_p(number)
    print(f'semaphore_pool_ex: {time() - start_pool}')






