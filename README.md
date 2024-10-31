# ai-for-data-wrangling
Practical ways to leverage Azure AI Studio for deploying Open AI and other models. We'll also explore how to seamlessly integrate these models into Python data pipelines

## Setup environment

### Create and activate a new Anaconda Environment:

```` shell
conda create -n ai-for-data-wrangling-talk python=3.11
conda activate ai-for-data-wrangling-talk
````

### Install, required libraries

```` shell
pip install pandas
pip install openai
pip install nest_asyncio
pip install azure-ai-inference
pip install openpyxl
pip install matplotlib
pip install seaborn
````

### Setup environmental variables

#### In Mac

1. Open the ~/.zshrc file to edit the file.

```` shell
code ~/.zshrc
````

2. Add the access keys for the Azure AI endpoints to the env variables to the end of the file.

```` shell
launchctl setenv AZURE_AI_GPT_4O_MINI_API_KEY 'here goes your secret key'
launchctl setenv AZURE_AI_MISTRAL_3B_API_KEY 'here goes your secret key'
launchctl setenv AZURE_AI_PHI_3_5_MINI_INSTRUCT_API_KEY 'here goes your secret key'

export AZURE_AI_GPT_4O_MINI_API_KEY='here goes your secret key'
export AZURE_AI_MISTRAL_3B_API_KEY='here goes your secret key'
export AZURE_AI_PHI_3_5_MINI_INSTRUCT_API_KEY='here goes your secret key'
````

3. Save and close file and Visual Code.

4. Load the file so it is applied in the system.

```` shell
source ~/.zshrc
````

5. Open Visual Code again.

### In Windows

Follow these [instructions](https://phoenixnap.com/kb/windows-set-environment-variable).

That's it! You are ready to rock and roll.
