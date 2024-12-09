# Importowanie niezbędnych bibliotek
import numpy as np
from prettytable import PrettyTable
import matplotlib.pyplot as plt

# Funkcja do generowania losowych procesów z określonymi parametrami
def generate_processes(num_processes, mean_execution_time, std_dev_execution_time, arrival_time_range):
    processes = []
    # Generowanie losowych czasów przybycia
    arrival_times = np.random.uniform(*arrival_time_range, num_processes // 1)
    #arrival_times = np.tile(np.random.uniform(*arrival_time_range, num_processes // 25), 25)

    # Generowanie losowych czasów wykonania
    execution_times = np.random.uniform(1, mean_execution_time, num_processes)

    for i in range(num_processes):
        if i < len(arrival_times):  # Sprawdzanie, aby nie przekroczyć dostępnych czasów przybycia
            processes.append(Process(i + 1, arrival_times[i], max(1, execution_times[i])))

    return processes

# Klasa reprezentująca pojedynczy proces
class Process:
    def __init__(self, process_id, arrival_time, execution_time):
        self.process_id = process_id
        self.arrival_time = arrival_time
        self.execution_time = execution_time
        self.execution_completed = None
        self.waiting_time = None
        self.turnaround_time = None

# Algorytm szeregowania Shortest Job First (SJF)
def sort_by_sjf(processes):
    sorted_processes = []

    # Sortowanie według czasów przybycia procesów, od najkrótszego czasu przybycia.
    processes.sort(key=lambda x: (x.arrival_time, x.execution_time))

    # Zmienna zlicza łączny czas wyjściowy procesów.
    exit_timer = processes[0].arrival_time + processes[0].execution_time

    # Pierwszy proces jest dodawany samodzielnie.
    sorted_processes.append(processes[0])

    # Usuwamy proces z listy, aby pominąć go przy następnym sortowaniu.
    processes.pop(0)

    # Sortujemy listę według czasów wykonywania, a w przypadku remisu według czasów przybycia procesów.
    processes.sort(key=lambda x: (x.execution_time, x.arrival_time))

    # Pętla wykonuje się, aż pozbędziemy się wszystkich procesów z pierwotnej listy.
    while processes:
        # Przechodzimy po kolei przez wszystkie elementy listy.
        for process in processes:
            # Wykonuje się jeśli czas przybycia procesu jest mniejszy lub równy czasowi wyjścia minionego procesu.
            if exit_timer >= process.arrival_time:
                # Dodajemy proces na listę.
                sorted_processes.append(process)
                # Następnie dodajemy czasy wykonania procesu i czasy wyjścia procesów.
                exit_timer += process.execution_time
                # Usuwamy proces z listy.
                processes.remove(process)
                break

    return sorted_processes

def sjf(processes):
    sorted_processes = sort_by_sjf(processes)
    current_time = 0

    for process in sorted_processes:
        if process.arrival_time > current_time:
            current_time = process.arrival_time
        process.waiting_time = current_time - process.arrival_time
        process.execution_completed = current_time + process.execution_time
        process.turnaround_time = process.waiting_time + process.execution_time
        current_time = process.execution_completed

    table = PrettyTable()
    table.field_names = ["Numer Procesu", "Czas Przybycia", "Czas Wykonania", "Czas Oczekiwania", "Czas Turnaround", "Czas Zakończenia"]

    for process in sorted_processes:
        table.add_row([process.process_id, process.arrival_time, process.execution_time,
                       process.waiting_time, process.turnaround_time, process.execution_completed])

    average_waiting_time = sum(process.waiting_time for process in sorted_processes) / len(sorted_processes)
    average_turnaround_time = sum(process.turnaround_time for process in sorted_processes) / len(sorted_processes)
    average_completion_time = sum(process.execution_completed for process in sorted_processes) / len(sorted_processes)
    return table, average_waiting_time, average_turnaround_time, average_completion_time



# Algorytm szeregowania First-Come, First-Served (FCFS)
def fcfs(processes):
    # Sortowanie procesów względem czasu przybycia
    processes.sort(key=lambda x: x.arrival_time)
    current_time = 0

    for process in processes:
        if process.arrival_time > current_time:
            current_time = process.arrival_time
        # Obliczanie czasu oczekiwania, czasu zakończenia i czasu turnaround dla procesu
        process.waiting_time = current_time - process.arrival_time
        process.execution_completed = current_time + process.execution_time
        process.turnaround_time = process.waiting_time + process.execution_time
        current_time = process.execution_completed

    # Tworzenie tabeli wynikowej do wizualizacji rezultatów
    table = PrettyTable()
    table.field_names = ["Numer Procesu", "Czas Przybycia", "Czas Wykonania", "Czas Oczekiwania", "Czas Turnaround", "Czas Zakończenia"]

    for process in processes:
        table.add_row([process.process_id, process.arrival_time, process.execution_time,
                       process.waiting_time, process.turnaround_time, process.execution_completed])

    # Obliczenie średnich czasów
    average_waiting_time = sum(process.waiting_time for process in processes) / len(processes)
    average_turnaround_time = sum(process.turnaround_time for process in processes) / len(processes)
    average_completion_time = sum(process.execution_completed for process in processes) / len(processes)
    return table, average_waiting_time, average_turnaround_time, average_completion_time

# Funkcja do eksportowania wyników do pliku tekstowego
def export_to_file(table, waiting_time, turnaround_time, completion_time, filename):
    with open(filename, 'w') as file:
        file.write(str(table))
        file.write(f"\nŚredni Czas Oczekiwania: {waiting_time}")
        file.write(f"\nŚredni Czas Turnaround: {turnaround_time}")
        file.write(f"\nŚredni Czas Zakończenia: {completion_time}")

# Funkcja do porównywania wyników FCFS i SJF dla różnej liczby procesów
# Funkcja do porównywania wyników FCFS i SJF dla różnej liczby procesów
def plot_comparison(num_processes_list, fcfs_times, sjf_times, title, y_label, filename):
    bar_width = 0.35
    index = np.arange(len(num_processes_list))

    plt.figure(figsize=(15, 8))  # Zmieniony rozmiar figury

    # Wykres 1: Porównanie Średniego Czasu Oczekiwania
    plt.subplot(3, 1, 1)
    plt.bar(index - bar_width/2, fcfs_times, bar_width, label='FCFS')
    plt.bar(index + bar_width/2, sjf_times, bar_width, label='SJF')
    plt.title('Porównanie Średniego Czasu Oczekiwania')
    plt.xlabel('Liczba Procesów')
    plt.ylabel('Średni Czas Oczekiwania')
    plt.xticks(index, num_processes_list)
    plt.legend()
    plt.grid(axis='y')

    # Wykres 2: Porównanie Średniego Czasu Turnaround
    plt.subplot(3, 1, 2)
    plt.bar(index - bar_width/2, fcfs_times, bar_width, label='FCFS')
    plt.bar(index + bar_width/2, sjf_times, bar_width, label='SJF')
    plt.title('Porównanie Średniego Czasu Obrotu')
    plt.xlabel('Liczba Procesów')
    plt.ylabel('Średni Czas Turnaround')
    plt.xticks(index, num_processes_list)
    plt.legend()
    plt.grid(axis='y')

    # Wykres 3: Porównanie Średniego Czasu Zakończenia
    plt.subplot(3, 1, 3)
    plt.bar(index - bar_width/2, fcfs_times, bar_width, label='FCFS')
    plt.bar(index + bar_width/2, sjf_times, bar_width, label='SJF')
    plt.title('Porównanie Średniego Czasu Zakończenia')
    plt.xlabel('Liczba Procesów')
    plt.ylabel('Średni Czas Zakończenia')
    plt.xticks(index, num_processes_list)
    plt.legend()
    plt.grid(axis='y')

    plt.tight_layout()  # Poprawa rozmieszczenia elementów
    plt.savefig(filename)
    plt.show()

# Główna funkcja do przeprowadzenia symulacji dla różnej liczby procesów
def main():
    num_processes_list = [25, 75, 125]
    mean_execution_time = 100

    fcfs_waiting_times = []
    sjf_waiting_times = []
    fcfs_turnaround_times = []
    sjf_turnaround_times = []
    fcfs_completion_times = []
    sjf_completion_times = []

    for num_processes in num_processes_list:
        # Generowanie losowych procesów
        processes = generate_processes(num_processes, mean_execution_time, 5, arrival_time_range=(25, 25))


        # FCFS
        fcfs_table, fcfs_waiting_time, fcfs_turnaround_time, fcfs_completion_time = fcfs(processes)
        # Eksport wyników FCFS do pliku
        export_to_file(fcfs_table, fcfs_waiting_time, fcfs_turnaround_time, fcfs_completion_time, f"fcfs_results_{num_processes}.txt")
        # Dodanie wyników do listy dla późniejszego porównania
        fcfs_waiting_times.append(fcfs_waiting_time)
        fcfs_turnaround_times.append(fcfs_turnaround_time)
        fcfs_completion_times.append(fcfs_completion_time)
        # SJF
        sjf_table, sjf_waiting_time, sjf_turnaround_time, sjf_completion_time = sjf(processes)
        # Eksport wyników SJF do pliku
        export_to_file(sjf_table, sjf_waiting_time, sjf_turnaround_time, sjf_completion_time, f"sjf_results_{num_processes}.txt")
        # Dodanie wyników do listy dla późniejszego porównania
        sjf_waiting_times.append(sjf_waiting_time)
        sjf_turnaround_times.append(sjf_turnaround_time)
        sjf_completion_times.append(sjf_completion_time)

    # Porównanie wyników dla różnej liczby procesów
    plot_comparison(num_processes_list, fcfs_waiting_times, sjf_waiting_times,
                    'Porównanie Średniego Czasu Oczekiwania', 'Średni Czas Oczekiwania', 'waiting_time_comparison.png')

    plot_comparison(num_processes_list, fcfs_turnaround_times, sjf_turnaround_times,
                    'Porównanie Średniego Czasu Turnaround', 'Średni Czas Turnaround', 'turnaround_time_comparison.png')

    plot_comparison(num_processes_list, fcfs_completion_times, sjf_completion_times,
                    'Porównanie Średniego Czasu Zakończenia', 'Średni Czas Zakończenia', 'completion_time_comparison.png')

if __name__ == "__main__":
    main()
