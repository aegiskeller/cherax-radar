import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import argparse

rain_index = [(180,180,255), (120,120,255), (20,20,255), (0, 216, 195), (0, 150, 144), (0, 102, 102), 
              (255, 255, 0), (255,200,0), (255,150,0), (255,100,0), (255,0,0), (200,0,0), (120,0,0), (40,0,0)]

def plot_rain_pixels(site):
    """
    This function reads the rain pixel results from the file and plots time vs. columns.
    The RGB values rain_index are used in tahe plot to be consistent with the original radar image
    The plot is saved as a PNG file.
    """
    # Read the data from the file
    file_path = f'rain_px_results_{site}.txt'
    data = pd.read_csv(file_path, header=None, names=['timestamp'] + ['radius']
                       + [f'int_{i}' for i in range(1, 15)])
    
    # Convert the timestamp column to datetime
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    #print(data.head())
    # Calculate the sum of rain pixel columns
    data['sum'] = data.iloc[:, 2:].sum(axis=1)
    
    # Calculate the moving average (5 time steps)
    data['moving_avg'] = data['sum'].rolling(window=5).mean()
    # Plot the data
    plt.figure(figsize=(8, 6))
    for i, col in enumerate(data.columns[2:15]):
        plt.plot(data['timestamp'], data[col], label=col, color=[c/255 for c in rain_index[i]])
        
    # Plot the moving average
    plt.plot(data['timestamp'], data['moving_avg'], label='Mv Avg', color='black', linewidth=2)

    plt.xlabel('Time')
    plt.ylabel('Fraction of Region with Rain Pixels')
    plt.title(f'Rain Pixel Count Over Time for {site}')
    plt.legend(bbox_to_anchor=(0.90, 1), loc='upper left')
    plt.grid(True)
    
    # Save the plot as a PNG file
    output_file = f'static/rain_px_plot_{site}.png'
    plt.savefig(output_file)
    return(f'Plot saved as {output_file}')

# Example usage
# plot_rain_pixels('example_site')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot rain pixel data.')
    parser.add_argument('site', type=str, help='The site identifier for the rain pixel data file.')
    args = parser.parse_args()
    
    plot_rain_pixels(args.site)
