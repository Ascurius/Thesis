# 0. Template

### Program Code
### Parameters
### Command Executed
### Error Message

# 1. Out of RAM

### Program Code
```py
from Compiler.types import sint
from Compiler.library import print_ln

a = sint.get_input_from(0, size=10)
b = sint.get_input_from(1, size=10)
result = a * b

print_ln("%s", result.reveal())
```

### Parameters

- Working directory: ~/Masterarbeit
- Machine: Locally on Laptop

### Commands Executed

1. `./mp-spdz-0.3.8/Scripts/compile-run.py -E mascot ./code/test.py`

### Error Message

```
Default bit length for compilation: 32
Compiling file ./code/test.py
Writing to Programs/Schedules/test.sch
Writing to Programs/Bytecode/test-0.bc
Hash: 335ed9dd9693b2140ed8cec1b792cc085d65484e3f3982d16b08184a6ff1ea0d
Program requires at most:
          10 integer inputs from player 0
          10 integer inputs from player 1
          10 integer triples
          10 integer opens
           3 virtual machine rounds
Creating binary for virtual machine...
clang++ -o Processor/BaseMachine.o Processor/BaseMachine.cpp -I./local/include -march=native  -g -Wextra -Wall -O3 -I. -I./deps -pthread    -DUSE_GF2N_LONG '-DPREP_DIR="Player-Data/"' '-DSSL_DIR="Player-Data/ssl"'  -std=c++11 -Werror  -std=c++17 -fPIC -MMD -MP -c
make: clang++: Datei oder Verzeichnis nicht gefunden
make: *** [Makefile:83: Processor/BaseMachine.o] Fehler 127
Traceback (most recent call last):
  File "/home/martin/Dokumente/Masterarbeit/mp-spdz-0.3.8/Scripts/../Compiler/compilerLib.py", line 521, in local_execution
    subprocess.run(["make", executable], check=True, cwd=self.root)
  File "/usr/lib64/python3.12/subprocess.py", line 571, in run
    raise CalledProcessError(retcode, process.args,
subprocess.CalledProcessError: Command '['make', 'replicated-bin-party.x']' returned non-zero exit status 2.

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/martin/Dokumente/Masterarbeit/./mp-spdz-0.3.8/Scripts/compile-run.py", line 19, in <module>
    compiler.local_execution()
  File "/home/martin/Dokumente/Masterarbeit/mp-spdz-0.3.8/Scripts/../Compiler/compilerLib.py", line 523, in local_execution
    raise CompilerError(
Compiler.exceptions.CompilerError: Cannot produce replicated-bin-party.x. Note that compilation requires a few GB of RAM.
```

# 2. replicated-bin-party.x not found during execution

### Program Code

```py
from Compiler.types import sint
from Compiler.library import print_ln

a = sint.get_input_from(0, size=10)
b = sint.get_input_from(1, size=10)
result = a * b

print_ln("%s", result.reveal())
```

### Parameters

- Working directory: ~/Masterarbeit
- Machine: Locally on Laptop

### Command Executed

1. `./mp-spdz-0.3.8/compile.py ./code/test.py`
2. `./mp-spdz-0.3.8/Scripts/replicated.sh test`

### Error Message

```
Running /home/martin/Dokumente/Masterarbeit/mp-spdz-0.3.8/Scripts/../replicated-bin-party.x 0 test -pn 12663 -h localhost
Running /home/martin/Dokumente/Masterarbeit/mp-spdz-0.3.8/Scripts/../replicated-bin-party.x 1 test -pn 12663 -h localhost
Running /home/martin/Dokumente/Masterarbeit/mp-spdz-0.3.8/Scripts/../replicated-bin-party.x 2 test -pn 12663 -h localhost
/home/martin/Dokumente/Masterarbeit/mp-spdz-0.3.8/Scripts/run-common.sh: Zeile 74: /home/martin/Dokumente/Masterarbeit/mp-spdz-0.3.8/Scripts/../replicated-bin-party.x: Datei oder Verzeichnis nicht gefunden
=== Party 1
/home/martin/Dokumente/Masterarbeit/mp-spdz-0.3.8/Scripts/run-common.sh: Zeile 74: /home/martin/Dokumente/Masterarbeit/mp-spdz-0.3.8/Scripts/../replicated-bin-party.x: Datei oder Verzeichnis nicht gefunden
=== Party 2
/home/martin/Dokumente/Masterarbeit/mp-spdz-0.3.8/Scripts/run-common.sh: Zeile 74: /home/martin/Dokumente/Masterarbeit/mp-spdz-0.3.8/Scripts/../replicated-bin-party.x: Datei oder Verzeichnis nicht gefunden
```