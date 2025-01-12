# SmartChain : A Warehouse Optimization


PickOptima is a powerful simulation tool designed to analyze and optimize order-picking efficiency based on wave size. By providing adjustable parameters and visual insights, this tool helps businesses streamline their picking process to enhance operational productivity.

---

## Project Structure

```
PickOptima/
├── app.py  # Main application for visualization using Streamlit
├── utils/
│   ├── simulation/
│   │   ├── simulation_batch.py  # Simulates batch picking processes
│   └── batch/
│       ├── mapping_batch.py  # Handles mapping logic for orders
└── myenv/  # Virtual environment (not included in GitHub)
```

---

## Features

- **Dynamic Order Line Simulation:** 
  - Adjust the number of order lines for analysis.
  - Simulate the impact of varying wave sizes on picking efficiency.

- **Interactive Visualizations:**
  - Provides graphs and charts to visualize the performance metrics.

- **Customizable Parameters:**
  - Configure the simulation with minimum and maximum wave sizes.

- **Scalable Design:**
  - Modular architecture for easy customization and extension.

---

## Installation Guide

### 1. Prerequisites

- Python 3.8+
- Git

### 2. Clone the Repository

```bash
git clone https://github.com/MalyajNailwal/PickOptima.git
cd PickOptima
```

### 3. Set Up Virtual Environment

Create and activate a virtual environment:
```bash
python3 -m venv myenv
source myenv/bin/activate  # macOS/Linux
myenv\Scripts\activate  # Windows
```

### 4. Install Dependencies

Install required libraries:
```bash
pip install -r requirements.txt
```

---

## How to Run the Application

1. Activate the virtual environment (if not already active).
   ```bash
   source myenv/bin/activate  # macOS/Linux
   myenv\Scripts\activate  # Windows
   ```

2. Launch the Streamlit app:
   ```bash
   streamlit run app.py
   ```

3. Open the provided URL in your web browser to access the application.

---

## Usage

### **1. Simulation Inputs**
- **Order Line Scope:** Adjust the total number of order lines for analysis.
- **Wave Size Range:** Configure the minimum and maximum wave sizes.

### **2. Outputs**
- Visualizations showcasing the relationship between wave size and picking efficiency.
- Insights to optimize order-picking workflows.

---

## File Descriptions

### 1. **app.py**
The main Streamlit application that:
- Collects user inputs.
- Displays interactive graphs and outputs.
- Integrates functionalities from utility modules.

### 2. **simulation_batch.py**
Simulates batch order-picking processes based on user-defined parameters. Key methods include:
- `simulate_batch`: Generates simulation data.

### 3. **mapping_batch.py**
Handles mapping logic for orders, including:
- Generating mapping data for simulation.

---

## Technologies Used

- **Programming Language:** Python 3.8+
- **Framework:** Streamlit
- **Data Visualization:** Matplotlib, Plotly

---

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature-name"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.



