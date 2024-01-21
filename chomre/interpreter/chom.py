from cst import Root, load_cst_from_file
import click
import os


@click.command()
@click.argument('filename')
#@click.option('--openai-api-key', default=None, help='OpenAI API token')
def chomp(filename: str):               #, openai_api_key: str):
    """Print FILENAME."""
    
    #if openai_api_key is not None:
    #    os.environ["OPENAI_API_KEY"] = openai_api_key
    
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    if OPENAI_API_KEY is None:
        click.echo("Please set OPENAI_API_KEY environment variable to your OpenAI API key.")
        exit (1)

    CST: Root
    if filename.endswith(".json") or filename.endswith(".cst"):
        CST = load_cst_from_file(filename)
        click.echo(f"Loaded CST from file: {filename}")
    elif filename.endswith(".chom") or filename.endswith(".ch") or filename.endswith(".txt"):
        pass
    else:
        click.echo("Invalid file extension, please provide either .chom or .txt file for the program you are trying to create, or a chom syntax tree file ending in .json or .cst.")
        exit (1)

    click.echo(CST)





if __name__ == "__main__":
    chomp()