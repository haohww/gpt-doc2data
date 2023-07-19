import argparse
from config import load_config
from model_driver import generate_questions
import asyncio
import json


def main(context):
    data = asyncio.run(generate_questions(context))

    with open("data.json", "w") as output_file:
        json.dump(data, output_file, indent=4)


if __name__ == "__main__":
    # Call the load_config function to apply the configuration
    context = load_config()

    # Create an argument parser
    parser = argparse.ArgumentParser(
        description="GPD-doc2data: Generate question/answer pairs from documentation"
    )

    # Add command-line flags
    parser.add_argument(
        "-n",
        dest="num_data",
        type=int,
        default=context["num_data_default"],
        help="Number of question/answer pairs to generate",
    )
    parser.add_argument(
        "-m",
        dest="model",
        choices=["gpt-3.5-turbo-16k"],
        default="gpt-3.5-turbo-16k",
        help="Model to use for generation",
    )

    # Parse the command-line arguments
    args = parser.parse_args()

    context["num_data"] = args.num_data
    context["model"] = args.model

    print(
        f"Generating {args.num_data} question/answer pairs using the {args.model} model"
    )

    # Call the main function with the provided arguments
    main(context)
