// This is a BAML config file, which extends the Jinja2 templating language to write LLM functions.

class Exercises {
  to_do string[] @description("Try not to repeat exercises if possible")
}


function ExtractExercises(prompt: string) -> Resume {
  // see clients.baml
  client GPT4o

  // The prompt uses Jinja syntax. Change the models or this text and watch the prompt preview change!
  prompt #"
   List exercise names for a {{experience_level}} level workout focusing on {{body_part}} with {{exercise_duration}} minutes to complete. 
   Please only list the exercises nothing else. no modifications just the standardized name for the prompt. 
   Also each exercise should take atleast 3 minutes so dont give too many exercises. Also dont list any numbers just the exercises in a list.
    {# special macro to print the output instructions. #}
    {{ ctx.output_format }}

    JSON:
  "#
}
