# Bike Rental Example With Swarm

A demonstration of how to use the [Swarm library](https://github.com/openai/swarm) to manage a bike rental service with specialized agents.

## Environment variables

To run this example, create a `.env` file and set the `OPENAI_API_KEY` variable with your OpenAI API key.

```shell
cp .env.example .env
```

## Requirements

Requires Python 3.10+.
It may be necessary to run the following commands within a Python virtual environment. To create one, use the command below:

```shell
python3.10 -m venv ./.venv
source .venv/bin/activate
```

## Install

```shell
make install
```

## Usage

```shell
make run
```

## Evaluation

```shell
make eval
```
