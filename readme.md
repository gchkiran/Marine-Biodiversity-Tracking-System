# Marine Biodiversity Tracking System

## Overview

The Marine Biodiversity Tracking System is a comprehensive web application designed to manage, track, and analyze various aspects of marine biodiversity. The system allows users to add and manage species data, conservation projects, research studies, pollution sources, and tracking records of marine species. It provides interactive visualizations to help users understand trends and impacts on marine life.

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Automated Data Validation:**
  Ensures accuracy and integrity of species data, project records, and research findings.
  
- **Interactive Visualizations:**
  Graphs and dashboards provide insights into biodiversity trends and pollution impact.

- **Efficient Data Management:**
  Supports CRUD (Create, Read, Update, Delete) operations for:
  - Marine species information
  - Conservation projects
  - Research studies
  - Pollution source tracking

- **User-Friendly Interface:**
  Designed for seamless navigation and data accessibility.

- **Scalability:**
  Suitable for individual researchers, organizations, and governmental agencies.

---

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/gchkiran/marine-biodiversity-tracking-system
   cd Marine-Biodiversity-Tracking-System
   ```

2. **Set Up Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application:**
   ```bash
   streamlit run main.py
   ```

---

## Usage

1. Launch the application:
   ```bash
   streamlit run main.py
   ```
2. Open your web browser and navigate to:
   ```plaintext
   http://localhost:8501/
   ```

3. Use the interface to:
   - Add and manage marine species data
   - Add and manage location data
   - Add and manage observation data
   - Add and manage pollution data
   - Analyze pollution sources
   - Visualize biodiversity trends

---

## Technologies Used

- **Backend:** Python
- **Frontend:** HTML, CSS, Streamlit
- **Database:** MySQL
- **Version Control:** Git
- **Deployment:** Streamlit

---

## Contributing

Contributions are welcome! Follow these steps to contribute:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add a meaningful message"
   ```
4. Push to your branch:
   ```bash
   git push origin feature-name
   ```
5. Open a Pull Request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

---

