# Stable-Diffusion
Inference backend pipeline for diffusion models.
## Setup
1. Set the [Huggingface](https://huggingface.co/settings/tokens) environment variable in your `.bashrc` file as the following:
   ```bash
   export HUGGINGFACE_API=<your-token>
   ```
2. Run the deploy script
    ```bash
    cd scripts
    bash deploy
    ```
 * The deploy script will complete the following tasks:
   * Installing relevant GPU drivers 
   * Downloading and setting up [Anaconda](https://docs.anaconda.com/anaconda/install/linux/)
   * download model weights
   * setup an Nginx server with a reverse proxy
   * start a gunicorn server

