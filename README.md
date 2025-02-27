# Bike Rental Example With Swarm

An example of using the [Swarm library](https://github.com/openai/swarm) to use specialized agents to manage a bike rental service.

## Environment variables

To run the example, you need to create your `.env` file and set the `OPENAI_API_KEY` environment variable to your OpenAI API key.

```shell
cp .env.example .env
```

## Install

Requires Python 3.10+

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
