# github-network-analysis
Network analysis of contributors for all public repos under santhosh600
# Setup Mode: GitHub Network Analysis for santhosh600

This project offers "setup mode" for easy installation and use.
Simply run the Python script to:
- Install all required dependencies, if missing
- Prompt you for your GitHub Personal Access Token (if not set)
- Fetch and visualize your contributor-repo network

## Quick Start

1. **Clone/download this repository.**
2. **Run in your terminal:**

   ```bash
   python github_network_analysis_setup.py
   ```

3. **When prompted, paste your GitHub token.**  
   (Get it from [GitHub Settings → Developer Settings → Tokens](https://github.com/settings/tokens). Only "public_repo" scope is required.)
4. **See results:** Top contributors/repos listed, plus network graph pop up.

## Technical Notes

- If you want to avoid manual token input, set an environment variable before running:
    ```bash
    export GITHUB_TOKEN=your_token_here
    ```
- Works with Python 3.7+

## License

MIT
