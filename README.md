# DUPChecker: 

## What can DUPChecker do:

### Serialization Library Compatibility Checker
DUPChecker analyzes data syntax defined using standard serialization libraries and detect incompatibility across versions, which can lead to upgrade failures. 
It focuses on two widely adopted serialization libraries, [Portocol Buffer](https://developers.google.com/protocol-buffers/docs/proto.) and [Apache Thrift](https://diwakergupta.github.io/thrift-missing-guide/).

Protocols evolve over time. Developers can update any protocol to meet the program’s need. However, certain rules have to be followed to avoid data-syntax incompatibility across versions. Particularly, the manuals of Protocol Buffer and Apache Thrift both state the following rules:

    (1). Add/delete required field. 

    (2). The tag number of a field has been changed.

    (3).  A  required field has been changed to non-required. 
    
    (4). Added or deleted an enum with no 0 value.

Violating the first two rules will definitely lead to upgrade failures caused by syntax incompatibility, which will be referred to as `ERROR` by DUPChecker; violating the third rule may lead to failures, which will be referred to as `WARNING` by DUPChecker, if the new version generates data that does not contain its no-longer-required data member. For other type of changes such as changing field type,
DUPChecker will output `INFO` level information. 

### Checker of enum whose order is used in serialization


## Installation

Prerequiste: In Python3, install javalang, numpy, pyparsing with: 

    $pip3 install javalang, numpy, pyparsing
    
Checkout DUPChecker to your local machine.

    $git clone https://github.com/jwjwyoung/DUPChecker.git

## Usage

### Proto Checker
1. Prepare the application that you would like to check the consistentcy on the same machine, suppose its path is `path_app`. 

2. Run Script

    `python3 checker.py  --app path_app --filetype --v1 old_version_tag --v2 new_version_tag`

    e.g. check for proto file:

    `python3 checker.py  --app hbase --proto --v1 rel/2.2.6 --v2 rel/2.3.3`
    
    e.g. check for thrift file:

    `python3 checker.py  --app hbase --thrift --v1 rel/2.2.6 --v2 rel/2.3.3`
### Enum Checker

    $java -jar EnumChecker.jar > output.log

    $grep "============start enum================" -A 5 output.log
    

## Reproduce Experiments in the Paper Section 6.2.2

1. Checkout the required applications in the DUPChecker/ directory.. 

      (1). hbase `git clone https://github.com/apache/hbase.git`
      
      (2). hdfs, yarn `git clone https://github.com/apache/hadoop.git`
      
      (3). mesos `git clone https://github.com/apache/mesos.git`

      (4). hive `git clone https://github.com/apache/hive.git`

      (5). impala `git clone https://github.com/apache/impala.git`
      
      (6). accumulo `git clone https://github.com/apache/accumulo.git`
      
      
2. Create a log folder
    ` mkdir log`

3. Run scripts:

    `python3 run_experiment.py` 

    The results will be output to files under log folder with application's name as prefix.
4. Generate Table 6 in the paper:
    `python3 export.py`

##  Evaluation requirement: 

1. server config: virtualbox ubnutu 18, 4G RAM, 20G disk. 
2. time distribution: 

    1). setup new ubuntu vm - 15~30 min
    2)install dependencies and download required git repos - 15 min
    3) run experiements - ~60 min.
    
## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## LICENSE

[MIT](https://github.com/jwjwyoung/DUPChecker/blob/master/LICENSE)
