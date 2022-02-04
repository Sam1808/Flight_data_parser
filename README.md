# Flight data parser for [Kiwi.com](https://www.kiwi.com/)

Hello everybody!  
I have a [task](https://github.com/kiwicom/python-weekend-entry-task) from Kiwi.com ([task copy](task.md)).
Let`s solve it just for fun.

As a solution, let me show the script `main.py`.

### How to run.

- You do not need any additional packages, only standard python v3.8 and higher
- Just run `main.py` with required options

#### About options

Please run script with `-h` key for help.
```shell
>> python main.py -h
usage: main.py [-h] [--bags BAGS] [--return] ORG DST PATH

Process options for flight parcer

positional arguments:
  ORG          Origin airport
  DST          Destination airport
  PATH         Input path to data csv file

optional arguments:
  -h, --help   show this help message and exit
  --bags BAGS  Input bags count
  --return     Do you want to return?
```

`ORG`, `DST`, `PATH` - required arguments.
If you input garbage, the script raise an error.

Error examples:
```shell
python main.py gxv lom  wrong_path/example2.csv --bags=1 --return

            Something wrong with filepath: wrong_path/example2.csv
            Please check and try again
```

```shell
python main.py WRONG lom  example/example2.csv --bags=1 --return

                Cannot find origin airport: WRONG
                Please check and try again
```
Successful launch example:
```shell
python main.py gxv lom  example/example2.csv --bags=1 --return
Trip from GXV to LOM
[{'flights'...}]
Trip from LOM to GXV
[{'flights'...}]
```
### My IMHO

 - Script works according task. Thank you Kiwi.com!
 - The task is more difficult than it seems. I had to read about [DFS](https://en.wikipedia.org/wiki/Depth-first_search) and [Itertools](https://docs.python.org/3/library/itertools.html) to solve it.
 - Unfortunately, not the most optimal search algorithm was used (the script falls with big dataset). There are several ideas to improve flight search. But I solve this task just for fun.
 - Not all tests have been written. For example, a script must check the contents of a dataset.
