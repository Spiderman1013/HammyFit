###############################################################################
#
#  Welcome to Baml! To use this generated code, please run the following:
#
#  $ pip install baml
#
###############################################################################

# This file was generated by BAML: please do not edit it. Instead, edit the
# BAML files and re-generate this code.
#
# ruff: noqa: E501,F401
# flake8: noqa: E501,F401
# pylint: disable=unused-import,line-too-long
# fmt: off

file_map = {
    
    "clients.baml": "// Learn more about clients at https://docs.boundaryml.com/docs/snippets/clients/overview\n\nclient<llm> GPT4o {\n  provider openai\n  options {\n    model \"gpt-4o\"\n    api_key env.OPENAI_API_KEY\n  }\n}\n\nclient<llm> GPT4oMini {\n  provider openai\n  options {\n    model \"gpt-4o-mini\"\n    api_key env.OPENAI_API_KEY\n  }\n}\n\nclient<llm> Sonnet {\n  provider anthropic\n  options {\n    model \"claude-3-5-sonnet-20240620\"\n    api_key env.ANTHROPIC_API_KEY\n  }\n}\n\n\nclient<llm> Haiku {\n  provider anthropic\n  options {\n    model \"claude-3-haiku-20240307\"\n    api_key env.ANTHROPIC_API_KEY\n  }\n}\n\nclient<llm> Fast {\n  provider round-robin\n  options {\n    // This will alternate between the two clients\n    strategy [GPT4oMini, Haiku]\n  }\n}\n\nclient<llm> Openai {\n  provider fallback\n  options {\n    // This will try the clients in order until one succeeds\n    strategy [GPT4o, GPT4oMini]\n  }\n}",
    "exer.baml": "// This is a BAML config file, which extends the Jinja2 templating language to write LLM functions.\n\nclass Exercises {\n  to_do string[] @description(\"Try not to repeat exercises if possible\")\n}\n\n\nfunction ExtractExercises(experience_level: string, body_part: string, exercise_duration: string) -> Exercises{\n  // see clients.baml\n  client GPT4o\n\n  // The prompt uses Jinja syntax. Change the models or this text and watch the prompt preview change!\n  prompt #\"\n   List exercise names for a {{experience_level}} level workout focusing on {{body_part}} with {{exercise_duration}} minutes to complete. \n   Please only list the exercises nothing else. no modifications just the standardized name for the prompt. \n   Also each exercise should take atleast 3 minutes so dont give too many exercises. Also dont list any numbers just the exercises in a list.\n    {# special macro to print the output instructions. #}\n    {{ ctx.output_format }}\n\n    JSON:\n  \"#\n}\n",
    "generators.baml": "// This helps use auto generate libraries you can use in the language of\n// your choice. You can have multiple generators if you use multiple languages.\n// Just ensure that the output_dir is different for each generator.\ngenerator target {\n    // Valid values: \"python/pydantic\", \"typescript\", \"ruby/sorbet\", \"rest/openapi\"\n    output_type \"python/pydantic\"\n\n    // Where the generated code will be saved (relative to baml_src/)\n    output_dir \"\"\n\n    // The version of the BAML package you have installed (e.g. same version as your baml-py or @boundaryml/baml).\n    // The BAML VSCode extension version should also match this version.\n    version \"0.57.0\"\n\n    // Valid values: \"sync\", \"async\"\n    // This controls what `b.FunctionName()` will be (sync or async).\n    default_client_mode sync\n}\n",
}

def get_baml_files():
    return file_map