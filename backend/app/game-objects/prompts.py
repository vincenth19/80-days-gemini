import yaml
import re
import copy

class Prompts():
    def __init__(self, prompt_yaml, logger):
        with open(prompt_yaml, 'r') as f:
            self.collections = yaml.safe_load(f)
        self.logger = logger

    def insert_data_blocks(self, prompt_key:str, data_block_dict:dict):
        updated_prompt = copy.copy(self.collections[prompt_key])

        for block_tag, block_value in data_block_dict.items():
            self.logger.debug(f'inserting data between {block_tag} tags in {prompt_key}')
            data_block_regex = re.compile(rf'<{block_tag}>.*?</{block_tag}>', re.DOTALL)
            updated_prompt = re.sub(data_block_regex, 
                                    f'<{block_tag}>{block_value}</{block_tag}>', 
                                    updated_prompt)
        
        return updated_prompt