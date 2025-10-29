import matplotlib.pyplot as plt


def plot_profile(depth, temperature):
    fig, ax = plt.subplots()  
    ax.plot(temperature, depth)
    ax.set_xlabel("Temperature [C]")
    ax.set_ylabel("Depth [m]")
    plt.show()


