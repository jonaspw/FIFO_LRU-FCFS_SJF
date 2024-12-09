import random

class FIFO:
    def __init__(self, capacity):
        # Inicjalizacja klasy FIFO
        self.capacity = capacity
        # Kolejka stron w algorytmie FIFO
        self.page_queue = []

    def page_fault(self, page):
        # Obsługa błędów strony w algorytmie FIFO
        if page not in self.page_queue:
            if len(self.page_queue) >= self.capacity:
                # Jeżeli kolejka osiągnęła maksymalną pojemność, usuń najstarszy element
                self.page_queue.pop(0)
            # Dodaj nową stronę na koniec kolejki
            self.page_queue.append(page)
            return True  # Zwróć True, jeśli wystąpił błąd strony
        return False  # Zwróć False, jeśli strona już istnieje w kolejce


class LRU:
    def __init__(self, capacity):
        # Inicjalizacja klasy LRU
        self.capacity = capacity
        # Kolejność stron w algorytmie LRU
        self.page_order = []

    def page_fault(self, page):
        # Obsługa błędów strony w algorytmie LRU
        if page not in self.page_order:
            if len(self.page_order) >= self.capacity:
                # Jeżeli kolejka osiągnęła maksymalną pojemność, usuń najstarszy element
                self.page_order.pop(0)
            # Dodaj nową stronę na koniec kolejki
            self.page_order.append(page)
            return True  # Zwróć True, jeśli wystąpił błąd strony
        else:
            # Jeżeli strona już istnieje, usuń ją z aktualnej pozycji i dodaj na koniec
            self.page_order.remove(page)
            self.page_order.append(page)
            return False  # Zwróć False, ponieważ strona już istnieje w kolejce


def generate_data_and_save(num_cells, sequence_length, filename):
    # Generowanie danych losowych i zapis do pliku
    data = [random.randint(1, num_cells) for _ in range(sequence_length)]
    with open(filename, 'w') as file:
        file.write("Generated Data:\n")
        file.write(','.join(map(str, data)))

    return data


def simulate_algorithm(algorithm, pages):
    # Symulacja algorytmu stronicowania
    page_faults = 0
    results = []

    for page in pages:
        if algorithm.page_fault(page):
            page_faults += 1
        # Zapisz wyniki po każdym kroku symulacji
        results.append(list(algorithm.page_order) if isinstance(algorithm, LRU) else list(algorithm.page_queue))

    return results, page_faults


def save_results_to_file(results, page_faults, filename):
    # Zapisz wyniki symulacji do pliku
    with open(filename, 'w') as file:
        file.write(f"Number of Page Faults: {page_faults}\n\n")
        for i, result in enumerate(results):
            file.write(f"Step {i + 1}: {result}\n")


if __name__ == "__main__":
    # Przykładowe dane wejściowe
    num_cells = 9
    sequence_length = 20
    pojemnosc = 9

    # Generowanie danych i zapis do pliku
    sekwencja_stron = generate_data_and_save(num_cells, sequence_length, 'generated_data.txt')

    # Symulacja algorytmu FIFO
    algorytm_fifo = FIFO(pojemnosc)
    wyniki_fifo, bledy_fifo = simulate_algorithm(algorytm_fifo, sekwencja_stron)
    save_results_to_file(wyniki_fifo, bledy_fifo, 'wyniki_fifo.txt')

    # Symulacja algorytmu LRU
    algorytm_lru = LRU(pojemnosc)
    wyniki_lru, bledy_lru = simulate_algorithm(algorytm_lru, sekwencja_stron)
    save_results_to_file(wyniki_lru, bledy_lru, 'wyniki_lru.txt')
