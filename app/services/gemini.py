import google.generativeai as genai
from dotenv import load_dotenv
import os
from typing import Dict, Optional

load_dotenv()
_api_key = os.environ['GEMINI_API_KEY']
_model_name = os.getenv('GEMIN_MODEL', 'gemini-1.5-flash')

class GeminiClient:
    """
    A client class for interacting with the Google Gemini API.
    
    This class manages the configuration and usage of the Gemini generative model.
    """

    def __init__(
        self, 
        api_key: Optional[str] = None,
        config: Dict[str, any] = None
    ) -> None:
        """
        Initialize the GeminiClient.

        Args:
            config (Dict[str, any], optional): A dictionary containing configuration parameters.
                Possible keys:
                - model_name: str
                - safety_settings: safety_types.SafetySettingOptions
                - generation_config: generation_types.GenerationConfigType
                - tools: content_types.FunctionLibraryType
                - tool_config: content_types.ToolConfigType
                - system_instruction: content_types.ContentType
        
        Raises:
            ValueError: If no API key is provided or found in environment variables.
        """
        self.config = config or {}
        
        self.api_key = api_key or _api_key
        if not self.api_key:
            raise ValueError("No API key provided. Set GEMINI_API_KEY environment variable or pass it in the config.")

        self.config.setdefault('model_name', _model_name)
        print(self.config)
        genai.configure(api_key=self.api_key)
        self._update_gemini_instance()

    def _update_gemini_instance(self) -> None:
        """Update the Gemini model instance with current configuration."""
        # Filter out None values and 'api_key' from config
        model_params = {k: v for k, v in self.config.items() if v is not None and k != 'api_key'}
        self.gemini = genai.GenerativeModel(**model_params)

    def update_gemini_config(self, new_config: Dict[str, any]) -> None:
        """
        Update the Gemini configuration.

        Args:
            new_config (Dict[str, any]): A dictionary containing new configuration parameters.
        """
        self.config.update(new_config)
        self._update_gemini_instance()

    def use_gemini(self) -> genai.GenerativeModel:
        """
        Get the current Gemini model instance.

        Returns:
            genai.GenerativeModel: The current Gemini model instance.
        """
        return self.gemini

    def get_current_config(self) -> Dict[str, any]:
        """
        Get the current configuration of the Gemini client.

        Returns:
            Dict[str, any]: A dictionary containing the current configuration.
        """
        config_copy = self.config.copy()
        if 'api_key' in config_copy:
            config_copy['api_key'] = 'hidden'
        return config_copy