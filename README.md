# cha
Chinese version of Python that compiles into Python.

## Usage
Run cha2.py using a valid .cha file as the first argument
```bash
./cha2.py bin.example.cha
```

This will generate an equivalent .py file which can be run with Python 3.5
(ideally). Note that cha_base.py must also be accessible to all files.

## Language Features

### Number Support

#### Scientific Notation

#### Verbose Number

#### Shorthand

#### Different Bases

### Variable Support

### Equivalent Values in Python

.py  | example            | .cha | example
---- | ------------------ | ---- | -------
all  | all([True, False]) | 都    | 都（【真，假】）
any  | any([True, False]) | 任何   | 任何（【真，假】）
