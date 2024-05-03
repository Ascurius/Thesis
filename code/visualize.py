import matplotlib.pyplot as plt


def query_comparison():
    # Data for plain query
    plain_rows = [1000, 10000, 100000, 1000000]
    plain_times = [0.000152, 0.001439, 0.015146, 0.223941]

    # Data for secure query
    secure_rows = [1000, 10000, 100000]
    secure_times = [0.04807, 1.36505, 17.435]

    # Data for SQL query
    sql_rows = [1000, 10000, 100000, 1000000]
    sql_times = [0.0055, 0.0058, 0.0110, 0.0144]

    plt.figure(figsize=(10, 6))

    # Plotting plain query
    plt.plot(plain_rows, plain_times, marker='o', label='Plain')

    # Plotting secure query
    plt.plot(secure_rows, secure_times, marker='o', label='Secure')

    # Plotting SQL query
    plt.plot(sql_rows, sql_times, marker='o', label='SQL')

    plt.title('Query Time Comparison')
    plt.xlabel('Number of Rows')
    plt.ylabel('Query Time (s)')
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig('query_time_comparison.png')

def secure_metrics():
    # Data for secure query resources
    rows = [1000, 10000, 100000]
    data_size = [2.58, 65.40, 762.34]  # Data size in MB
    rounds = [437999, 12719671, 150003463]  # Rounds
    time = [48.07, 1365.05, 17435]  # Time in seconds

    plt.figure(figsize=(10, 8))

    # Plotting data size
    plt.subplot(3, 1, 1)
    plt.plot(rows, data_size, marker='o', color='blue')
    plt.title('Secure Query Resources')
    plt.ylabel('Data Size (MB)')
    plt.xscale('log')
    plt.grid(True)

    # Plotting rounds
    plt.subplot(3, 1, 2)
    plt.plot(rows, rounds, marker='o', color='orange')
    plt.ylabel('Rounds')
    plt.xscale('log')
    plt.grid(True)

    # Plotting time
    plt.subplot(3, 1, 3)
    plt.plot(rows, time, marker='o', color='green')
    plt.xlabel('Number of Rows')
    plt.ylabel('Time (seconds)')
    plt.xscale('log')
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('secure_metrics.png')

secure_metrics()