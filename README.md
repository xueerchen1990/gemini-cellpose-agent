# Gemini Cellpose Agent

Gemini Cellpose Agent is an automated tool designed to assist in cell research using the Gemini generative AI model. This agent can answer questions about cellpose, explain cell image segmentation, and even generate Python code to segment cell images.

[Demo Video](https://www.youtube.com/watch?v=8gkyAr_OUrQ)

## Features

- **Interactive Chat**: Engage in a conversational interface to ask questions about cellpose and cell image segmentation.
- **Code Generation**: Automatically generate Python code for cell image segmentation tasks.
- **Code Execution**: Execute generated Python code and handle errors with debugging options.
- **Image Handling**: Attach and process images for segmentation tasks.

## Installation

To install the Gemini Cellpose Agent, follow these steps:

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/xueerchen1990/gemini-cell-agent.git
   cd gemini-cell-agent
   ```

2. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   pip install .
   ```

3. **Set Up Environment Variables**:
   ```
   export GEMINI_API_KEY=your_gemini_api_key_here
   ```

## Usage

0. **Download Data**:
   - Download the `cellpose.txt` file and sample images from [Kaggle](https://www.kaggle.com/datasets/xueerchen/cellpose-github-repo-and-sample-images).

1. **Start the Chat Interface**:
   ```sh
   cd chainlit_demo
   chainlit run --port 7777 app.py -w
   ```

2. **Interact with the Agent**:
   - Open your web browser and navigate to [http://localhost:7777](http://localhost:7777) to access the demo.
   - Use the chat interface to ask questions or request code generation.

## Example Queries

- **What is cellpose?**
- **Explain how cell image segmentation works in cellpose.**
- **Write Python code to segment a cell image.**

## Project Structure

- **chainlit_demo/app.py**: Main application file for the chat interface.
- **gemini_cell_agent/utils.py**: Utility functions for handling environment variables, code execution, and image processing.
- **setup.py**: Setup script for packaging the project.

## License

This project is licensed under the MIT License.

## Contact

For any questions or support, please contact [Xueer Chen](mailto:xueer.chen.human@gmail.com).

## Acknowledgments

- Thanks to the developers of the Gemini generative AI model.
- Special thanks to the Chainlit team for the interactive chat interface.
