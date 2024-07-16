import re
import copy
from app.utils.file import read_yaml_file
class Prompts():
    """Class to handle prompts.yaml"""

    def __init__(self, prompt_yaml, logger):
        self.collections = read_yaml_file(prompt_yaml)
        self.logger = logger

    def insert_data_blocks(self, prompt_key:str, data_block_dict:dict) -> str:
        """
        Function to insert data in between XML tags in the prompt string
        This will replace anything in between <data_block_dict.keys></data_block_dict.keys>
        
        :param prompt_key: The key of the prompt to be modified.
        :type prompt_key: str
        
        :param data_block_dict: A dictionary containing the new data block.
        :type data_block_dict: dict

        :returns: The updated string with inserted data blocks.
        :rtype: str
        """
        updated_prompt = copy.copy(self.collections[prompt_key])
        for block_tag, block_value in data_block_dict.items():
            self.logger.debug(f'inserting data between {block_tag} tags in {prompt_key}')
            # compile regex to find data block based on block_tag
            data_block_regex = re.compile(rf'<{block_tag}>.*?</{block_tag}>', re.DOTALL)
            # insert block_value in between block tags
            updated_prompt = re.sub(data_block_regex, 
                                    f'<{block_tag}>{block_value}</{block_tag}>', 
                                    updated_prompt)
        return updated_prompt