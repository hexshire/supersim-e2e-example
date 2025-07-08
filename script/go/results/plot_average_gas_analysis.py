#!/usr/bin/env python3
import os
import json
import glob
import numpy as np
import matplotlib.pyplot as plt

def generate_gas_analysis_chart():
    # Directory containing the JSON files
    results_dir = os.path.dirname(os.path.realpath(__file__))

    # Find all gas analysis JSON files
    json_files = glob.glob(os.path.join(results_dir, 'gas_analysis_*.json'))

    if not json_files:
        print("No gas_analysis JSON files found.")
        return

    # Dictionary to store aggregated data
    # Key: nested_messages, Value: {'relay': [], 'claim': []}
    aggregated_data = {}

    # Loop through each JSON file and aggregate the data
    for file_path in json_files:
        with open(file_path, 'r') as f:
            data = json.load(f)
            for key, values in data.items():
                nested_messages = int(key)
                if nested_messages not in aggregated_data:
                    aggregated_data[nested_messages] = {'relay': [], 'claim': []}

                aggregated_data[nested_messages]['relay'].append(values['relay'])
                aggregated_data[nested_messages]['claim'].append(values['claim'])

    # Sort the data by the number of nested messages
    sorted_keys = sorted(aggregated_data.keys())

    nested_messages = sorted_keys
    relay_means = [np.mean(aggregated_data[key]['relay']) for key in sorted_keys]
    claim_means = [np.mean(aggregated_data[key]['claim']) for key in sorted_keys]
    relay_std = [np.std(aggregated_data[key]['relay']) for key in sorted_keys]
    claim_std = [np.std(aggregated_data[key]['claim']) for key in sorted_keys]

    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    # Target range
    target_min, target_max = 0, 15

    # Plot 1: Relay Gas Delta
    ax1.errorbar(nested_messages, relay_means, yerr=relay_std,
                 marker='o', linewidth=2, markersize=8, capsize=5,
                 color='#2E86AB', label='Relay Delta (Mean ± StdDev)')
    ax1.axhspan(target_min, target_max, alpha=0.3, color='green', label='Target Range (0-15)')
    ax1.set_xlabel('Number of Nested Messages')
    ax1.set_ylabel('Gas Delta (units)')
    ax1.set_title('Average Relay Gas Delta vs Nested Messages')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    ax1.set_ylim(min(relay_means) - max(relay_std) - 10, max(relay_means) + max(relay_std) + 10)

    # Add annotations for values
    for x, y, std in zip(nested_messages, relay_means, relay_std):
        ax1.annotate(f'{y:.0f}±{std:.0f}', (x, y), textcoords="offset points",
                    xytext=(0,10), ha='center', fontsize=9)

    # Plot 2: Claim Gas Delta
    ax2.errorbar(nested_messages, claim_means, yerr=claim_std,
                 marker='s', linewidth=2, markersize=8, capsize=5,
                 color='#A23B72', label='Claim Delta (Mean ± StdDev)')
    ax2.axhspan(target_min, target_max, alpha=0.3, color='green', label='Target Range (0-15)')
    ax2.set_xlabel('Number of Nested Messages')
    ax2.set_ylabel('Gas Delta (units)')
    ax2.set_title('Average Claim Gas Delta vs Nested Messages')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    ax2.set_ylim(min(claim_means) - max(claim_std) - 50, max(claim_means) + max(claim_std) + 50)

    # Add annotations for values
    for x, y, std in zip(nested_messages, claim_means, claim_std):
        ax2.annotate(f'{y:.0f}±{std:.0f}', (x, y), textcoords="offset points",
                    xytext=(0,10), ha='center', fontsize=9)

    plt.tight_layout()

    # Save the chart
    output_png_path = os.path.join(results_dir, 'gas_analysis_average_chart.png')
    output_pdf_path = os.path.join(results_dir, 'gas_analysis_average_chart.pdf')
    plt.savefig(output_png_path, dpi=300, bbox_inches='tight')
    plt.savefig(output_pdf_path, bbox_inches='tight')

    print("📊 Average Gas Analysis Charts Generated!")
    print("Files saved:")
    print(f"  - {os.path.basename(output_png_path)}")
    print(f"  - {os.path.basename(output_pdf_path)}")

if __name__ == '__main__':
    generate_gas_analysis_chart()