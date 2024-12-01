# Chainlit Demo: Cellpose Agent Powered by Gemini 1.5 Flash

This folder contains a Chainlit demo of the Cellpose agent powered by Gemini 1.5 Flash.

## Instructions to Run the Demo

1. **Download Data**:
   - Download the `cellpose.txt` file and sample images from [Kaggle](https://www.kaggle.com/datasets/xueerchen/cellpose-github-repo-and-sample-images).

2. **Install Dependencies**:
   - Run the following command to install the necessary dependencies:
     ```sh
     pip install ..
     ```

3. **Run the Demo**:
   - Execute the following command to start the Chainlit server:
     ```sh
     chainlit run --port 7777 app.py -w
     ```

4. **Access the Demo**:
   - Open your web browser and navigate to [http://localhost:7777](http://localhost:7777) to access the demo.