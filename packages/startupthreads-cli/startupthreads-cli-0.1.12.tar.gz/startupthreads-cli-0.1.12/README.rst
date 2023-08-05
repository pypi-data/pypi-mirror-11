# Startup Threads CLI

Send t-shirts from the command line.

## Installation

```
$ git clone git@github.com:soulshake/startup-threads-cli.git
$ cd startup-threads-cli/
$ pip install .
```


# Setup

Export your API key as an environment variable in your bash profile and source it:

```
$ echo "export STARTUP_THREADS_API_KEY abc123def456" >> ~/.bashrc && source ~/.bashrc
```

You can check that it's set up correctly by running:

```
echo $STARTUPTHREADS_API_KEY
```

...which should display your API key.


## Commands

```
$ swag  --help
Usage: swag [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  giveaway   Create a new StartupThreads giveaway (i.e.
  inventory  Call a function to display our StartupThreads...
  send       create a new StartupThreads order
  status     show the status of a StartupThreads order
```

```
$ swag inventory

name                 id        status    description      MS  MM    ML    MXL    M2XL      WS    WM    WL  WXL    W2XL  
-------------------  --------  --------  -------------  ----  ----  ----  -----  ------  ----  ----  ----  -----  ------
Motherboard Glow     3xyhor59  approved                    7  19    31    41     10         9     0     0              
No Bullshit Hashtag  jsi4_xay  approved                    5  13    26    16     9          6     0     2             
Invaders             rn2qjafd  approved                    9                                4     6     8            
Scribble (AA)        86dix_xv  approved                   15  0     6     3                10    10    20           
Scribble (Canvas)    zif5xjib  approved                   16  1     23    15               15    13    17          
Lotus                lzunev7m  approved                    4  7     21    23     6          3     0     2         

```



