import google.generativeai as genai
from pathlib import Path
from prompts import Prompts
import os
import logging


class JourneyPath():
    def __init__(self,
                 generator: genai.GenerativeModel,
                 prompt_yaml: Path,
                 logger:logging.Logger,
                 current_city: str = "London"):
        self.generator = generator
        self.logger = logger
        self.prompts = Prompts(prompt_yaml, logger=self.logger)
        self.options = self.generate_options(current_city)

    def generate_options(self, current_city:str, critic:bool = True) -> str:
        """
        Generate options based on the current city with LLM
        
        :param current_city: The name of the current city. Defaults to "London".
        :type current_city: str
        :param critic: A boolean value indicating whether or not to run LLM to evaluate/update options. Defaults to True.
        :type critic: bool, optional
        
        :return: The generated options as a JSON-formatted string.
        :rtype: str
        """
        self.logger.info(f'generating next paths from {current_city}')
        # insert current city into option_generator prompt and generate options with LLM
        option_generator_prompt = self.prompts.insert_data_blocks(
            'option_generator', 
            data_block_dict={'LOCATION': current_city})
        options = self.generator.generate_content(
            option_generator_prompt, 
              generation_config={"response_mime_type": "application/json"})
        
        if critic:
            self.logger.info(f'running critic llm')
            # insert generated option JSON between DATA tag in option_generator prompt
            option_critic_prompt = self.prompts.insert_data_blocks(
                'option_generator', 
                data_block_dict={'DATA': options.text})
            options = self.generator.generate_content(
                option_critic_prompt, 
                generation_config={"response_mime_type": "application/json"})
        
        return options.text

## FOR DEBUGGING
# if __name__=="__main__":
#     genai.configure(api_key=os.environ["GEMINI_API_KEY"])
#     logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     logger = logging.getLogger(__name__)

#     # Using `response_mime_type` requires one of the Gemini 1.5 Pro or 1.5 Flash models
#     model = genai.GenerativeModel('gemini-1.5-flash',
#                                 # Set the `response_mime_type` to output JSON
#                                 generation_config={"response_mime_type": "application/json"})
    
#     path = JourneyPath(model, 'backend/config/prompts.yaml', logger)
#     print(path.options)
