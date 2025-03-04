# Ollie: (Oll)ama Interative Entity

Ollie is an AI personal assistant that runs entirely on your device. It supports text and voice interactions and features a plugin architecture to extend its functionality.

# Features
- **On-Device Processing:** Ollie uses Ollama for all language processing, so everything runs on-device.
- **Text & Voice Interaction:** Interact with Ollie in either voice assistant mode or CLI text mode.
- **Plugin Architecture:** Easily add or customize functionality.
- **Library of pre-existing plugins:** Ollie already has an existing library of plugins that links into OpenWeatherMap, Philips Hue, and Spotify in addition to utilities like math and time.

# Installation

1. ### **[Install Ollama](https://ollama.com/download)**

2. Pull the llama3.1 model or [any other model that supports tools](https://ollama.com/search?c=tools):
    ```bash
    ollama pull llama3.1
    ```

3. **Clone the repository:**
    ```bash
    git clone https://github.com/bentheperson1/ollie.git
    cd OnDeviceAI
    ```

4. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
# Usage

### Basic Usage

```bash
python main.py
```

This command will start the script in voice mode using the default settings.

## Command-Line Arguments

The following arguments are available:

- **`--mode`**  
  **Description:** Sets the interaction mode.  
  **Options:**  
  - `text`: Enables text-based interaction.
  - `voice`: Enables voice-based interaction.  
  **Default:** `voice`

- **`--trigger`**  
  **Description:** The keyword used to trigger voice command capture.  
  **Default:** `curse`

- **`--model`**  
  **Description:** Specifies the chat model to use.  
  **Default:** `llama3.1`

- **`--voice_config`**  
  **Description:** Specifies the Piper voice configuration.  
  **Default:** `HFC_MALE`

## Examples

### Voice Interaction Mode

To run the script in voice mode with a custom trigger and voice configuration:

```bash
python main.py --mode voice --trigger "activate" --voice_config CUSTOM_CONFIG
```

### Text Interaction Mode

To run the script in text mode:

```bash
python main.py --mode text
```

## Additional Notes

**Environment Variables:**  
  The script uses `dotenv` to load sensitive environment variables. Make sure you have a `.env` file configured based on the example file provided.
