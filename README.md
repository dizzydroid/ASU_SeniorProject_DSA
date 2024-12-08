# **nodescope** | XML Editor and Visualizer

<div id="header" align="center">
 <img src="assets/nodescope_asu.png">
</div>


## **Table of Contents**
- [**nodescope** | XML Editor and Visualizer](#nodescope--xml-editor-and-visualizer)
  - [**Table of Contents**](#table-of-contents)
  - [**Introduction**](#introduction)
  - [**Features**](#features)
  - [**Setup**](#setup)
    - [**Prerequisites**](#prerequisites)
    - [**Installation**](#installation)
  - [**Usage**](#usage)
    - [**Command Line Interface (CLI)**](#command-line-interface-cli)
    - [**Graphical User Interface (GUI)**](#graphical-user-interface-gui)
  - [**Commands Overview**](#commands-overview)
  - [**Testing**](#testing)
  - [**Contributing**](#contributing)

---

## **Introduction**
The XML Editor and Visualizer is a project developed for the Data Structures and Algorithms (DSA) course. It provides tools for processing, analyzing, and visualizing XML files, either via a **Command Line Interface (CLI)** or a **Graphical User Interface (GUI)**. It is designed to work with XML data representing social networks, enabling features like validation, formatting, and conversion.

---

## **Features**
- **XML Validation**: Detect and fix issues like mismatched or missing tags.
- **Formatting**: Prettify XML with proper indentation for readability.
- **XML to JSON Conversion**: Transform XML data into JSON for web applications.
- **Minification**: Reduce XML file size by removing unnecessary spaces and newlines.
- **Compression**: Compress XML files into a custom format to save space.
- **Decompression**: Restore compressed XML files to their original format.
- **Visualization**: (Coming Soon) Represent social networks as graphs.
- **Network Analysis**: (Coming Soon) Identify influencers, mutual connections, and follow suggestions.

---

## **Setup**

### **Prerequisites**
- Python 3.8 or higher
- Libraries listed in `requirements.txt`

### **Installation**
1. Clone the repository:
   ```bash
   git clone https://github.com/dizzydroid/ASU_SeniorProject_DSA/
   ```
2. Navigate to the project folder:
   ```bash
   cd ASU_SeniorProject_DSA
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## **Usage**

### **Command Line Interface (CLI)**
Perform quick and efficient operations on XML files via the CLI:
```bash
xml_editor [command] -i input_file [-o output_file]
```
> [!TIP]
> Replace `[command]` with one of the available commands listed [below](#commands-overview).

### **Graphical User Interface (GUI)**
Interact with XML files visually:
1. Launch the GUI:
   ```bash
   python main.py --gui
   ```
2. Select an XML file or paste content.
3. Use the buttons to perform operations and view results.

---

## **Commands Overview**

| Command      | Description                                | Example Command                                     |
|--------------|--------------------------------------------|----------------------------------------------------|
| `verify`     | Validate an XML file and optionally fix it.| `xml_editor verify -i input.xml -f -o fixed.xml`   |
| `format`     | Prettify an XML file for readability.      | `xml_editor format -i input.xml -o formatted.xml`  |
| `json`       | Convert XML to JSON format.                | `xml_editor json -i input.xml -o output.json`      |
| `mini`       | Minify XML by removing unnecessary spaces. | `xml_editor mini -i input.xml -o minified.xml`     |
| `compress`   | Compress an XML file into a custom format. | `xml_editor compress -i input.xml -o compressed.comp` |
| `decompress` | Restore compressed XML to its original form.| `xml_editor decompress -i compressed.comp -o output.xml` |

---

## **Testing**
Run tests to ensure functionality and correctness:
```bash
pytest tests/
```
Tests are located in the `tests/` directory and cover all major functionalities.

---

## **Contributing**
We welcome contributions to improve this tool! Here's how to get started:
1. Fork the repository and create a branch for your changes.
2. Follow consistent coding practices and provide meaningful commit messages.
3. Submit a pull request after running all tests.
