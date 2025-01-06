# **nodescope** | XML Editor and Visualizer

<div id="header" align="center">
 <img src="assets/nodescope_asu.png">
</div>


## **Table of Contents**
- [**Introduction**](#introduction)
  - [**Features**](#features)
  - [**Setup**](#setup)
    - [**Prerequisites**](#prerequisites)
    - [**Installation**](#installation)
  - [**Usage**](#usage)
    - [**Release Versions**](#release-versions)
    - [**From App.py**](#from-apppy)
    - [**Directly from Main**](#directly-from-main)
    - [**Command Line Interface (CLI)**](#command-line-interface-cli)
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
- **Visualization**: Represent social networks as graphs.
- **Network Analysis**: Identify influencers, mutual connections, and follow suggestions.
- **Post Search**: Search posts by word or topic.

---

## **Setup**

### **Prerequisites**
- Python 3.8 or higher
- Libraries listed in [`requirements.txt`](requirements.txt)

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

### **Release Versions**
You can download the executable from the [**latest release**](https://github.com/dizzydroid/ASU_SeniorProject_DSA/releases) to run the application without needing Python installed.

> [!NOTE]
> - The executable is available only for Windows OS, for other platforms you can run using Python by following the instructions below.
> 
> - The executable has a few [**known issues**](https://github.com/dizzydroid/ASU_SeniorProject_DSA/releases#:~:text=files%20and%20graphs.-,Known%20Issues,-The%20application%20may), please be patient on the first run.

### **From App.py**
This is the main script that launches the application, you can run it directly from root, on any platform:
```bash
python app.py
```

### **Directly from Main**
The main script allows you to choose either interface, you can run it directly from root:
```bash
python main.py
```
> Displays a help message with available options.
> Choose either `--cli` or `--gui` to launch the respective interface.

```bash
python main.py --gui
```
> Launches the GUI for visual interaction with XML files.

```bash
python main.py --cli
```
> Launches the CLI for quick operations on XML files, in a shell-like environment. 
> Simply type the [command](#commands-overview) followed by the required arguments.
> For example:
> ```bash
> >> verify -i input.xml -f -o fixed.xml
> ```
> To exit the CLI, type `exit` or `quit`.

### **Command Line Interface (CLI)**
Perform quick and efficient operations on XML files via the CLI using the `.bat` script provided, `xml_editor`:
```bash
./xml_editor [command] -i [input_file] -o [output_file]
```
> [!TIP]
> Replace `[command]` with one of the available commands listed [below](#commands-overview).

---

## **Commands Overview**
The following is a comprehensive list of commands available in the XML Editor and example usage for each:

| Command        | Description                                       | Example Command                                              |
|----------------|---------------------------------------------------|--------------------------------------------------------------|
| `verify`       | Validate an XML file and optionally fix it.       | `./xml_editor verify -i input.xml -f -o fixed.xml`  |
| `format`       | Prettify an XML file for readability.             | `./xml_editor format -i input.xml -o formatted.xml` |
| `json`         | Convert XML to JSON format.                       | `./xml_editor json -i input.xml -o output.json`     |
| `mini`         | Minify XML by removing unnecessary spaces.        | `./xml_editor mini -i input.xml -o minified.xml`    |
| `minify`       | Minify XML by removing unnecessary spaces.        | `./xml_editor minify -i input.xml -o minified.xml`  |
| `compress`     | Compress an XML file into a custom format.        | `./xml_editor compress -i input.xml -o compressed.xml` |
| `decompress`   | Restore compressed XML to its original form.      | `./xml_editor decompress -i compressed.xml -o output.xml` |
| `cascade`      | Perform a sequence of operations on an XML file.  | `./xml_editor cascade -i input.xml -o final.xml -ops verify format minify json` |
| `draw`         | Draw XML data as a graph.                         | `./xml_editor draw -i input.xml -o graph.png`       |
| `most_active`  | Find the most active user in the XML data.        | `./xml_editor most_active -i input.xml`             |
| `most_influencer` | Find the most influential user in the XML data.| `./xml_editor most_influencer -i input.xml`         |
| `mutual`       | Find mutual users for given user IDs.              | `./xml_editor mutual -i input.xml -ids 1,2,3`       |
| `suggest`      | Suggest users for a given user ID.                | `./xml_editor suggest -i input.xml -id 1`           |
| `search`       | Search posts by word or topic.                    | `./xml_editor search -i input.xml -w word -t topic` |


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
