# PIAWeb - a graphical web interface for PIA

**PIA** - short for **Protein Interaction Analyzer** - is a tool for automatic identification of important interactions and interaction-frequency-based scoring in protein-ligand complexes. **PIAWeb** offers a web-app-based graphical user interface to run workflows in PIA.

Requirements, installation and usage are thoroughly documented in the [PIA Wiki](https://github.com/michabirklbauer/PIA/wiki).

For general help, questions, suggestions or any other feedback please refer to the [PIA GitHub repository](https://github.com/michabirklbauer/PIA).

## Quick Setup

- Install [Docker](https://docs.docker.com/engine/install/).
- To run PIAWeb on your own server:
  ```bash
  docker run -d --restart always -p 80:8501 michabirklbauer/piaweb:latest
  ```
- To run PIAWeb locally:
  ```bash
  docker run -p 8501:8501 michabirklbauer/piaweb:latest
  ```

## Troubleshooting

Please refer to the [PIA Wiki](https://github.com/michabirklbauer/PIA/wiki) as well as [Issues](https://github.com/michabirklbauer/PIA/issues) and [Discussions](https://github.com/michabirklbauer/PIA/discussions) in [PIA](https://github.com/michabirklbauer/PIA).

## Contact

- Mail: [micha.birklbauer@gmail.com](mailto:micha.birklbauer@gmail.com)
- Telegram: [https://telegram.me/micha_birklbauer](https://telegram.me/micha_birklbauer)
