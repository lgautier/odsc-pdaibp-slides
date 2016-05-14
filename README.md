# Polyglot programming is being pragmatic
([ODSC-Boston](https://www.odsc.com/boston/) 2016)

The conference version of an edible arrangement: a docker container
to reproduce all code in an interactive notebook.

## Setup

### Docker

If you already have docker installed and running, go to the next section.
Otherwise check [https://www.docker.com/]

### Starting

The following two-step process should be all that is needed:

1. Open a terminal and run:

```bash
docker run -p 8888:8888 --rm rpy2/odsc-pdaibp-slides
```

2. Open a web browser and point it to [http://localhost:8888/]

